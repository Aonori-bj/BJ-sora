#=================================================
# 戦争結果 Created by Merino
#=================================================
# war.cgiにあってもいいけどごちゃごちゃになりそうなので分離

# 救出人数
my $max_rescue = 1;

#=================================================
# 引き分け
#=================================================
sub war_draw {
	&c_up('draw_c');
	my $v = int( rand(11) + 10 );
	$m{rank_exp} -= int( (rand(16)+15) * $m{value} );
	$m{exp} += $v;

	$mes .= "$m{name}に対する評価が下がりました<br>";
	$mes .= "$vの$e2j{exp}を手に入れました<br>";
	
	my $is_rewrite = 0;
	if ($m{sol} > 0) {
		$cs{soldier}[$m{country}] += $m{sol};
		$is_rewrite = 1;
	}
	if ($y{sol} > 0) {
		$cs{soldier}[$y{country}] += $y{sol};
		$is_rewrite = 1;
	}

	&down_friendship;
	&refresh;
	&n_menu;
	&write_cs;
}

#=================================================
# 負け
#=================================================
sub war_lose {
	&c_up('lose_c');
	my $v = int( rand(11) + 15 );
	&use_pet('war_result', 0);
	$m{rank_exp} -= int( (rand(21)+20) * $m{value} );
	$m{exp} += $v;

	$mes .= "部隊全滅という不名誉な敗北の為、$m{name}に対する評価が著しく下がりました<br>";
	$mes .= "$vの$e2j{exp}を手に入れました<br>";
	
	$cs{soldier}[$y{country}] += $y{sol} if $y{sol} > 0;
	&down_friendship;

	# 連続で同じ国だと高確率でﾀｲｰﾎ
	&refresh;
	if ( ( $w{world} eq '8' && $cs{strong}[$y{country}] <= 3000 ) || ( $w{world} eq '12' && $m{renzoku_c} > rand(4) ) || $m{renzoku_c} > rand(7) + 2 ) {
		&write_world_news("$c_mの$m{name}が$c_yの牢獄に幽閉されました");
		&add_prisoner;
	}

	&write_cs;
	&n_menu;
}

#=================================================
# 退却
#=================================================
sub war_escape {
	$mes .= "$m{name}に対する評価が下がりました<br>";
	$m{rank_exp} -= int( (rand(6)+5) * $m{value} );

	$cs{soldier}[$m{country}] += $m{sol};
	$cs{soldier}[$y{country}] += $y{sol};

	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# 勝ち
#=================================================
sub war_win {
	my $is_single = shift;

	# 奪国力ﾍﾞｰｽ:階級が高いほどﾌﾟﾗｽ。下克上、革命の時は階級が低いほどﾌﾟﾗｽ
	my $v = $w{world} eq '2' || $w{world} eq '3' ? (@ranks - $m{rank}) * 10 + 10 : $m{rank} * 8 + 10;

	# 定員が少ない分ﾌﾟﾗｽ多い分ﾏｲﾅｽ
	$v += ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 10;

	# 国情勢により奪国力増加
	if ($w{world} eq '5' || $w{world} eq '6') { # 暴君、混沌
		$v *= 2.5;
	}
	elsif ($w{world} eq '3') { # 革命:弱国有利
		my $sum = 0;
		for my $i (1 .. $w{country}) {
			$sum += $cs{win_c}[$i];
		}
		$v *= 2.5 if $cs{win_c}[$m{country}] <= $sum / $w{country};
	}
	elsif ($w{world} eq '2') { # 下克上:世代低い人有利
		if ($m{sedai} < 5) {
			$v *= 3;
		}
		elsif ($m{sedai} < 10) {
			$v *= 2.5;
		}
	}
	else {
		$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
	}
	
	# 交戦中なら2倍
	my $p_c_c = 'p_' . &union($m{country}, $y{country});
	$v *= 2 if $w{$p_c_c} eq '2';
	
	$v = $v * $m{value} * (rand(0.4)+0.8);
	$v = &use_pet('war_result', $v);
	
	# 奪国力上限
	if ($v !~ /^(\d)\1+$/) { # ｿﾞﾛ目(ｳﾛﾎﾞﾛｽ使用時など)
		if ($m{value} < 1) { # 少数精鋭
			$v = $v > 200 ? int(rand(100)+100) : int($v);
		}
		else { # 通常・長期
			if ($time + 2 * 24 * 3600 > $w{limit_time}) { # 統一期限残り１日
				$v = $v > 1500 ? int(rand(500)+1000) : int($v);
			}
			else {
				$v = $v > 600  ? int(rand(200)+400) : int($v);
			}
			
			# 統一期限が近づいてきたらﾌﾟﾗｽ
			$v += $time + 4 * 24 * 3600 > $w{limit_time} ? 40
			    : $time + 8 * 24 * 3600 > $w{limit_time} ? 20
			    :                                          5
			    ;
		}
	}
	
	# 滅亡国の場合罰則
	if ($cs{is_die}[$y{country}]) {
		$v = int($v * 0.5);
		&_penalty
	}
	else {
		$cs{soldier}[$m{country}] += $m{sol};
	}
	# 国力データ±
	$cs{strong}[$m{country}] += $v;
	$cs{strong}[$y{country}] -= $v;
	$cs{strong}[$y{country}] = 0  if $cs{strong}[$y{country}] < 0;
	
	$mes .= "$c_yから$vの$e2j{strong}を奪いました<br>";
	
	if ($is_single) {
		&write_world_news(qq|$c_mの$m{name}が$c_yに侵攻、$y{name}と一騎討ちの末これを下し <font color="#FF00FF"><b>$v</b> の$e2j{strong}を奪う事に成功</font>したようです|);
	}
	else {
		$m{value} < 1
			? &write_world_news(qq|何者かが$c_yに侵攻、$y{name}の部隊を撃破し <font color="#FF00FF"><b>$v</b> の$e2j{strong}を奪うことに成功</font>したようです|)
			: &write_world_news(qq|$c_mの$m{name}が$c_yに侵攻、$y{name}の部隊を撃破し <font color="#FF00FF"><b>$v</b> の$e2j{strong}を奪うことに成功</font>したようです|)
			;
	}

	&down_friendship;
	&c_up('win_c');
	++$m{medal};
	my $vv = int( (rand(21)+20) * $m{value} );
	$vv = &use_pet('war_win', $vv);
	$m{exp}      += $vv;
	$m{rank_exp} += int( (rand(11)+20) * $m{value} );
	$m{egg_c}    += int(rand(6)+5) if $m{egg};

	$mes .= "$m{name}に対する評価が大きく上がりました<br>";
	$mes .= "$vvの$e2j{exp}を手に入れました<br>";
	
	# ﾚｽｷｭｰ
	&_rescue if -s "$logdir/$y{country}/prisoner.cgi";

	&refresh;

	# 暗黒
	if ($w{world} eq $#world_states) {
		if ($cs{strong}[$m{country}] >= $touitu_strong || $cs{strong}[$w{country}] <= 0) {
			&_touitu;
		}
		elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
		elsif ( rand(4) < 1  || ($cs{strong}[$w{country}] < 30000 && rand(3) < 1) ) {
			require './lib/vs_npc.cgi';
			&npc_war;
		}
	}
	# 終焉
	elsif ($w{world} eq '14') {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1) {
			&_touitu;
		}
	}
	# 統一
	elsif ($cs{strong}[$m{country}] >= $touitu_strong) {
		&_touitu;
	}
	# 滅亡
	elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
		&_metubou;
	}
	# 復興
	elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 && !($w{world} eq '10' || $w{world} eq '14') ) {
		&_hukkou;
	}
	# 鉄壁
	elsif ($w{world} eq '8' && $cs{strong}[$y{country}] <= 3000 && rand(3) < 1) {
		my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 100  );
		&write_world_news("<b>ﾘｳﾞｧｲｱｻﾝの大嵐！$cs{name}[$m{country}]は$cs{name}[$y{country}]の$e2j{$kkk}を $vvv 奪いました</b>");
	}

	&daihyo_c_up('war_c'); # 代表熟練度
	&write_cs;

	&n_menu;
}

#=================================================
# 牢獄に仲間がいるなら救出
#=================================================
sub _rescue {
	my $is_rescue = 0;
	my @lines = ();
	my $count = 0;
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi が開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country) = split /<>/, $line;
		if ($count < $max_rescue && ($country eq $m{country} || $union eq $country) ) {
			$mes .= "$c_yに捕らえられていた$nameを救出しました<br>";
			$is_rescue = 1;
			&write_world_news("$c_mの$m{name}が$c_yに捕らえられていた$nameの救出に成功しました");
			
			# ﾚｽｷｭｰﾌﾗｸﾞ作成
			my $y_id = unpack 'H*', $name;
			if (-d "$userdir/$y_id") {
				open my $fh2, "> $userdir/$y_id/rescue_flag.cgi" or &error("$userdir/$y_id/rescue_flag.cgiﾌｧｲﾙが作れません");
				close $fh2;
			}
			++$count;
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rescue) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
}

#=================================================
# 統一
#=================================================
sub _touitu {
	&c_up('hero_c');
	if ($union) {
		$w{win_countries} = "$m{country},$union";
		++$cs{win_c}[$union];
	}
	else {
		$w{win_countries} = $m{country};
	}
	++$cs{win_c}[$m{country}];
	
	if ($w{world} eq $#world_states) {
		if ($m{country} eq $w{country} || $union eq $w{country}) { # NPC国側の勝利
			&mes_and_world_news("<em>悪魔達の率先者として$world_name大陸を支配することに成功しました</em>",1);
			&write_legend('touitu', "深き闇より目覚めた$cs{name}[$w{country}]の猛者達が$m{name}を筆頭とし$world_name大陸を支配する");
			$is_npc_win = 1;
		}
		else {
			&mes_and_world_news("<em>魔界を再び封印し、$world_name大陸にひとときの安らぎがおとずれました</em>",1);
			&write_legend('touitu', "$c_mの$m{name}とその仲間達が魔界を再び封印し、$world_name大陸にひとときの安らぎがおとずれる");
		}
	}
	else {
		if ($union) {
			$mes .= "<em>$world_name大陸を統一しました</em>";
			&write_world_news("<em>$c_m$cs{name}[$union]同盟の$m{name}が$world_name大陸を統一しました</em>",1);
			&write_legend('touitu', "$c_m$cs{name}[$union]同盟の$m{name}が$world_name大陸を統一する")
		}
		else {
			&mes_and_world_news("<em>$world_name大陸を統一しました</em>",1);
			&write_legend('touitu', "$c_mの$m{name}が$world_name大陸を統一する");
		}
	}

	require "./lib/reset.cgi";
	&reset;

	$m{lib} = 'world';
	$m{tp}  = 100;
	
}

#=================================================
# 復興
#=================================================
sub _hukkou {
	&c_up('huk_c');
	$cs{is_die}[$m{country}] = 0;
	&mes_and_world_news("<b>$c_mを復興させることに成功しました</b>", 1);
	
	--$w{game_lv};
#	--$w{game_lv} if $time + 7 * 24 * 3600 > $w{limit_time};
}

#=================================================
# 滅亡
#=================================================
sub _metubou {
	&c_up('met_c');
	$cs{strong}[$y{country}] = 0;
	$cs{is_die}[$y{country}] = 1;
	&mes_and_world_news("<b>$c_yを滅ぼしました</b>", 1);

	# 物資Down
	for my $k (qw/food money soldier/) {
		$cs{$k}[$y{country}] = int( $cs{$k}[$y{country}] * ( rand(0.3)+0.3 ) );
	}
	
	# 国状態変化
	for my $i (1 .. $w{country}) {
		$cs{state}[$i] = int(rand(@country_states));
	}
}
#=================================================
# 滅亡国から国力を奪取した時の罰則
#=================================================
sub _penalty {
	# 災害
	if ( ($w{world} eq '13' && rand(3) < 1) || rand(12) < 1 ) {
		&disaster;
	}
}

#=================================================
# 友好度Down
#=================================================
sub down_friendship {
	my $c_c = &union($m{country}, $y{country});
	$w{'f_'.$c_c} -= 1;
	if ($w{'p_'.$c_c} ne '2' && $w{'f_'.$c_c} < 10) {
		$w{'p_'.$c_c} = 2;
		&write_world_news("<b>$c_mの$m{name}の進軍により$c_yと交戦状態になりました</b>");
	}
	$w{'f_'.$c_c} = int(rand(20)) if $w{'f_'.$c_c} < 1;
}


1; # 削除不可
