$is_battle = 2;  # ﾊﾞﾄﾙﾌﾗｸﾞ2
sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
#================================================
# 戦争 Created by Merino
#================================================
# $m{value} には 兵士の倍率

# 一騎打ちの時の相手のｾﾘﾌ。一番先頭だけが断り用のｾﾘﾌ(増減可能)
my @answers = ('断る!', '望むところだ!', '返り討ちにしてくれる!', 'いざ勝負!', 'よかろう!', 'いいだろう!', '相手になろう!', 'かかってこい!');

# 陣形名(増減不可。名前の変更可能)
my @war_forms = ('攻撃陣形','防御陣形','突撃陣形');


#================================================
# 利用条件
#================================================
sub is_satisfy {
	if ($time < $w{reset_time}) {
		$mes .= '終戦期間なので戦争を中止します<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (!defined $cs{strong}[$y{country}]) {
		$mes .= '攻めている国は消滅してしまったので、戦争を中止します<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub tp_100 {
	$mes .= "$c_yに着きました<br>";
	
	my $is_ambush = &_get_war_you_data; # 待ち伏せされてた場合戻り値あり
	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};

	# 限界ﾀｰﾝ数決定
	$m{turn} = int( rand(6)+7 );
	if ($m{value} > 1) {
		$m{turn} += 3;
		$y{sol} = int($rank_sols[$y{rank}]);
	}
	else {
		$y{sol} = int($rank_sols[$y{rank}] * $m{value});
	}

	# 兵が足りない
	if ($y{sol} > $cs{soldier}[$y{country}]) {
		$mes .= "$c_yは兵不足のようだ…<br>緊急に寄せ集めの国民が召集された<br>";
		$cs{strong}[$y{country}] -= int(rand(100)+100);
		$cs{strong}[$y{country}] = 1 if $cs{strong}[$y{country}] < 1;
		$y{sol_lv} = int( rand(10) + 45 );
		&write_cs;
	}
	else {
		$cs{soldier}[$y{country}] -= $y{sol};
		$y{sol_lv} = 80;
	}

	# 待ち伏せ
	if ($pets[$m{pet}][2] ne 'no_ambush' && $is_ambush) {
		$mes .= "$c_yの$y{name}率いる$y{sol}の$units[$y{unit}][1]が待ち伏せしていました!<br>";
		if ($y{unit} eq '11') { # 暗殺部隊
			my $v = int( $m{sol} * (rand(0.2)+0.2) );
			$m{sol} -= $v;
			$m{sol_lv} = int( rand(15) + 15 ); # 15 〜 29
			$mes .= "$units[$y{unit}][1]による暗殺で、$vの兵がやられました!<br>";
		}
		elsif ($y{unit} eq '14') { # 幻影部隊
			$m{sol_lv} = int( rand(10) + 5 ); # 5 〜 14
			$mes .= "$units[$y{unit}][1]による幻術で、兵士達は混乱し大きく士気が下がりました!<br>";
		}
		else {
			$m{sol_lv} = int( rand(15) + 10 ); # 10 〜 24
			$mes .= "待ち伏せにより兵士達は混乱し大きく士気が下がりました!<br>";
		}
		&write_world_news("$c_mの$m{name}が$c_yに攻め込み$y{name}の待ち伏せにあいました");

		my $yid = unpack 'H*', $y{name};
		if (-d "$userdir/$yid") {
			open my $fh, ">> $userdir/$yid/ambush.cgi";
			print $fh "$m{name}/$ranks[$m{rank}]/$units[$m{unit}][1]/統率$m{lea}($date)<>";
			close $fh;
		}
	}
	else {
		$m{sol_lv} = 80;
		$mes .= "$c_yから$y{name}率いる$y{sol}の兵が出てきました<br>";
	}

	# 援軍系ﾍﾟｯﾄ
	if ($pets[$m{pet}][2] eq 'war_begin') {
		&use_pet('war_begin');
	}
	# 同盟している国からの援軍
	elsif ($union) {
		my $v = int( $m{sol} * (rand(0.1)+0.1) );
		$m{sol} += $v;
		$mes .= "なんと、$cs{name}[$union]から$v兵の援軍が駆けつけた!<br>";
	}
	
	$m{tp} += 10;
	&n_menu;
}

#================================================
sub tp_110 {
	$is_battle = 2;
	$m{act} += int(rand($m{turn})+$m{turn});
	
	$mes .= "今回の作戦の限界ﾀｰﾝは $m{turn} ﾀｰﾝです<br>";
	$mes .= "$m{name}軍 $m{sol}人 VS $y{name}軍 $y{sol}人<br>";
	$mes .= '攻め込む陣形を選んでください<br>';
	&menu(@war_forms,'退却');
	
	$m{tp} += 10;
	&write_cs;
}

#================================================
sub tp_120 { &tp_190; } # tp120だと退却可
sub tp_130 { &tp_190; } # tp130だと一騎打ち可
sub tp_140 { # 一騎打ち
	require './lib/battle.cgi';

	if ($m{hp} <= 0) {
		$mes .= "一騎打ちに敗れ指揮官を失った$m{name}の部隊は戦意を喪失し、敵軍からの追撃をうけ全滅しました…<br>";
		&write_world_news("$c_mの$m{name}が$c_yに侵攻、$y{name}と一騎討ちを演じるが敗北し部隊は敗走したようです");
		&war_lose;
	}
	elsif ($y{hp} <= 0) {
		$mes .= "敵軍は$y{name}の敗北に戦意を喪失しました！将を欠いた部隊など敵ではありません<br>敵軍を追撃し、かなりの被害を与えました！<br>";
		&war_win(1);
	}
}

#================================================
# ﾙｰﾌﾟﾒﾆｭｰ ﾀｰﾝ終了か勝つか負けるかまで
#================================================
sub loop_menu {
	$is_battle = 2;
	$mes .= "残り$m{turn} ﾀｰﾝ<br>";
	$mes .= "$m{name}軍 $m{sol}人 VS $y{name}軍 $y{sol}人<br>";
	$mes .= '攻め込む陣形を選んでください<br>';
	&menu(@war_forms);
}

sub tp_190 {
	if ($cmd >= 0 && $cmd <= 2) {
		--$m{turn};
		$mes .= "残り$m{turn}ﾀｰﾝ<br>";
		&_crash;
		
		if ($m{sol} <= 0 && $y{sol} <= 0) {
			$mes .= "両軍ともに壊滅的損害を受け戦闘継続が不可能\となりました<br>$e2j{strong}は両陣営とも変化なし<br>";
			$m{value} < 1
				? &write_world_news("何者かが$c_yに侵攻、$y{name}の部隊に阻まれ激戦の末、両軍壊滅したようです")
				: &write_world_news("$c_mの$m{name}が$c_yに侵攻、$y{name}の部隊に阻まれ激戦の末、両軍壊滅したようです")
				;

			&war_draw;
		}
		elsif ($m{sol} <= 0) {
			$mes .= '我が軍は全滅しました。撤退します…<br>';
			$m{value} < 1
				? &write_world_news("何者かが$c_yに侵攻、$y{name}の部隊の前に敗退したようです")
				: &write_world_news("$c_mの$m{name}が$c_yに侵攻、$y{name}の部隊の前に敗退したようです")
				;

			&war_lose;
		}
		elsif ($y{sol} <= 0) {
			$mes .= '敵部隊を撃破しました!!我が軍の勝利です!<br>';
			&war_win;
		}
		elsif ($m{turn} <= 0) {
			$mes .= "戦闘限界ﾀｰﾝを超えてしまった…これ以上は戦えません<br>$e2j{strong}は両陣営とも変化なし<br>";
			$m{value} < 1
				? &write_world_news("何者かが$c_yに侵攻し、$y{name}の部隊に阻まれ戦闘限界をｵｰﾊﾞｰしたようです")
				: &write_world_news("$c_mの$m{name}が$c_yに侵攻し、$y{name}の部隊に阻まれ戦闘限界をｵｰﾊﾞｰしたようです")
				;

			&war_draw;
		}
		else {
			$mes .= '攻め込む陣形を選んでください<br>';
			
			# 一騎打ち出現確立
			if ( ($pets[$m{pet}][2] eq 'war_single' && int(rand($m{turn}+3)) == 0) || int(rand($m{turn}+15)) == 0 ) {
				&menu(@war_forms,'一騎打ち');
				$m{tp} = 130;
			}
			elsif ($m{turn} < 4)  {
				&menu(@war_forms);
			}
			else {
				&menu(@war_forms,'退却');
				$m{tp} = 120;
			}
		}
	}
	elsif ($cmd eq '3' && $m{tp} eq '120') {
		$m_mes = '全軍退却!!';
		
		if ($m{turn} < 5) {
			$mes .= '敵軍に逃走退路を塞がれ、もはや撤退は不可能\です<br>';
			$m{tp} = 190;
			&loop_menu;
		}
		# 退却できる確立
		elsif ( int(rand($m{turn})) == 0) {
			$mes .= '残念ですが作戦を中止し退却します<br>';
			$m{value} < 1
				? &write_world_news("何者かが$c_yに侵攻し、$y{name}の部隊と交戦。余儀なく撤退した模様")
				: &write_world_news("$c_mの$m{name}が$c_yに侵攻し、$y{name}の部隊と交戦。余儀なく撤退した模様")
				;

			&war_escape;
		}
		else {
			$mes .= '退却に失敗しました<br>';
			$m{tp} = 190;
			&loop_menu;
		}
	}
	elsif ($cmd eq '3' && $m{tp} eq '130') {
		$m_mes = "$y{name}と一騎打ち願いたい!";

		my $v = int(rand(@answers));

		if ($v <= 0) {
			$y_mes = $answers[$v];
			$mes .= '一騎打ちを断られました<br>';
			&loop_menu;
			$m{tp} = 190;
		}
		else {
			$y_mes = $answers[$v];
			
			$mes .= "$y{name}に一騎打ちを申\し込み、この戦いの勝敗を架けた一騎討ちを行なう事に!<br>";
			$m{tp} = 140;
			&n_menu;
		}
	}
	else {
		&loop_menu;
		$m{tp} = 190;
	}
}

#================================================
# 陣形戦結果
#================================================
sub _crash {
	my $y_cmd = int(rand(3));
	
	$m_mes = $war_forms[$cmd];
	$y_mes = $war_forms[$y_cmd];
	
	my $result = 'draw';
	if ($cmd eq '0') {
		$result = $y_cmd eq '1' ? 'win'
				: $y_cmd eq '2' ? 'lose'
				:				  'draw'
				;
	}
	elsif ($cmd eq '1') {
		$result = $y_cmd eq '2' ? 'win'
				: $y_cmd eq '0' ? 'lose'
				:				  'draw'
				;
	}
	elsif ($cmd eq '2') {
		$result = $y_cmd eq '0' ? 'win'
				: $y_cmd eq '1' ? 'lose'
				:				  'draw'
				;
	}
	
	my $m_attack = ($m{sol}*0.1 + $m{lea}*2) * $m{sol_lv} * 0.01 * $units[$m{unit}][4] * $units[$y{unit}][5];
	my $y_attack = ($y{sol}*0.1 + $y{lea}*2) * $y{sol_lv} * 0.01 * $units[$y{unit}][4] * $units[$m{unit}][5];

	if (&is_tokkou($m{unit}, $y{unit})) {
		$is_m_tokkou = 1;
		$m_attack *= 1.3;
		$y_attack *= 0.5;
	}
	if (&is_tokkou($y{unit}, $m{unit})) {
		$is_y_tokkou = 1;
		$m_attack *= 0.5;
		$y_attack *= 1.3;
	}
	$m_attack = $m_attack < 150 ? int( rand(50)+100 ) : int( $m_attack * (rand(0.3) +0.9) );
	$y_attack = $y_attack < 150 ? int( rand(50)+100 ) : int( $y_attack * (rand(0.3) +0.9) );
	
	if ($result eq 'win') {
		$m_attack = int($m_attack * 1.3);
		$y_attack = int($y_attack * 0.5);
		
		$m{sol_lv} += int(rand(5)+10);
		$y{sol_lv} -= int(rand(5)+10);

		$mes .= qq|○自軍被害$y_attack <font color="#FF0000">●敵軍被害$m_attack</font><br><br>|;
	}
	elsif ($result eq 'lose') {
		$m_attack = int($m_attack * 0.5);
		$y_attack = int($y_attack * 1.3);
		$m{sol_lv} -= int(rand(5)+10);
		$y{sol_lv} += int(rand(5)+10);
	
		$mes .= qq|<font color="#FF0000">○自軍被害$y_attack</font> ●敵軍被害$m_attack<br><br>|;
	}
	else {
		$m{sol_lv} += int(rand(3)+5);
		$y{sol_lv} += int(rand(3)+5);
	
		$mes .= qq|○自軍被害$y_attack ●敵軍被害$m_attack<br><br>|;
	}
	
	$m{sol} -= $y_attack;
	$y{sol} -= $m_attack;
	$m{sol} = 0 if $m{sol} < 0;
	$y{sol} = 0 if $y{sol} < 0;

	$m{sol_lv} = $m{sol_lv} < 10  ? int( rand(11) )
			   : $m{sol_lv} > 100 ? 100
			   :					$m{sol_lv}
			   ;
	$y{sol_lv} = $y{sol_lv} < 10  ? int( rand(11) )
			   : $y{sol_lv} > 100 ? 100
			   :					$y{sol_lv}
			   ;
}


#================================================
# 階級と統率が同じくらいの相手をランダムで探す。見つからない場合は用意されたNPC
#================================================
sub _get_war_you_data {
	my @lines = &get_country_members($y{country});
	
	if (@lines >= 1) {
		my $retry = $w{world} eq '8' && $cs{strong}[$y{country}] <= 3000      ? 0 # 世界情勢【鉄壁】攻めた国の国力が3000以下の場合は強制NPC
				  : $w{world} eq $#world_states && $y{country} eq $w{country} ? 1 # 世界情勢【暗黒】攻めた国がNPC国ならﾌﾟﾚｲﾔｰﾏｯﾁﾝｸﾞは１回
				  :																5 # その他ﾌﾟﾚｲﾔｰﾏｯﾁﾝｸﾞを最高５回ほどﾘﾄﾗｲする
				  ;
		my %sames = ();
		for my $i (1 .. $retry) {
			my $c = int(rand(@lines));
			next if $sames{$c}++; # 同じ人なら次
			
			$lines[$c] =~ tr/\x0D\x0A//d; # = chomp 余分な改行削除
			
			my $y_id = unpack 'H*', $lines[$c];
			
			# いない場合はﾘｽﾄから削除
			unless (-f "$userdir/$y_id/user.cgi") {
				require "./lib/move_player.cgi";
				&move_player($lines[$c], $y{country},'del');
				next;
			}
			
			my %you_datas = &get_you_datas($y_id, 1);
			
			next if $you_datas{lib} eq 'prison'; # 牢獄の人は除く
			next if $you_datas{lib} eq 'war'; # 戦争に出ている人は除く
			
			# 待ち伏せしている人がいたら
			if ( $you_datas{value} eq 'ambush' && $max_ambush_hour * 3600 + $you_datas{ltime} > $time) {
				# set %y
				while (my($k,$v) = each %you_datas) {
					next if $k =~ /^y_/;
					$y{$k} = $v;
				}
				$y_mes = $you_datas{mes};
				return 1;
			}
			# 階級と統率が近い人。左の数字を0にすればより強さの近い相手大きくすれば色々な相手
			elsif ( 2 >= rand(abs($m{rank}-$you_datas{rank})+2) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
				# set %y
				while (my($k,$v) = each %you_datas) {
					next if $k =~ /^y_/;
					$y{$k} = $v;
				}
				$y_mes = $you_datas{mes};
				return 0;
			}
		}
	}
	
	# ｼﾞｬﾄﾞｳ or NPC
	$pets[$m{pet}][2] eq 'no_shadow' || int(rand(3)) == 0 || $w{world} eq '8'
		? &_get_war_npc_data : &_get_war_shadow_data;
}

#================================================
# NPC [0] 〜 [4] の 5人([0]強い >>> [4]弱い)
#================================================
sub _get_war_npc_data {
	&error("相手国($y{country})のNPCデータがありません") unless -f "$datadir/npc_war_$y{country}.cgi";
	
	require "$datadir/npc_war_$y{country}.cgi";
	
	my $v = $m{lea} > 600 ? 0
		  : $m{lea} > 400 ? int(rand(2))
		  : $m{lea} > 250 ? int(rand(2)+1)
		  : $m{lea} > 120 ? int(rand(2)+2)
		  :                 int(rand(2)+3)
		  ;

	# 統一国の場合はNPC弱体
	my($c1, $c2) = split /,/, $w{win_countries};
	# 国力低い場合は強いNPC
	if ($cs{strong}[$y{country}] <= 3000) {
		$v = 0;
	}
	elsif ($c1 eq $y{country} || $c2 eq $y{country}) {
		$v += 1;
	}
	$v = $#npcs if $v > $#npcs;
	
	while ( my($k, $v) = each %{ $npcs[$v] }) {
		$y{$k} = $v;
	}
	$y{unit} = int(rand(@units));
	$y{icon} ||= $default_icon;
	$y{mes_win} = $y{mes_lose} = '';

	return 0;
}

#================================================
# ｼｬﾄﾞｳ
#================================================
sub _get_war_shadow_data {
	# 国力低い場合は1.5倍
	my $pinch = $cs{strong}[$y{country}] <= 3000 ? 1.5 : 1;
	
	for my $k (qw/max_hp max_mp at df mat mdf ag cha lea/) {
		$y{$k} = int($m{$k} * $pinch);
	}
	for my $k (qw/wea skills mes_win mes_lose icon rank unit/) {
		$y{$k} = $m{$k};
	}
	$y{rank} += 2;
	$y{rank} = $#ranks if $y{rank} > $#ranks;

	# 統一国の場合はNPC弱体
	my($c1, $c2) = split /,/, $w{win_countries};
	$y{rank} -= 2 if $c1 eq $y{country} || $c2 eq $y{country};

	$y{name}  = 'ｼｬﾄﾞｳ騎士(NPC)';
	
	return 0;
}


#================================================
# 兵種が特攻(有利)かどうか
#================================================
sub is_tokkou {
	my($m_unit, $y_unit) = @_;
	
	for my $tokkou (@{ $units[$m_unit][6] }) {
		return 1 if $tokkou eq $y_unit;
	}
	return 0;
}


#================================================
# _war_result.cgiに処理結果を渡す
#================================================
sub war_win {
	my $is_single = shift;
	require "./lib/_war_result.cgi";
	&war_win($is_single);
}
sub war_lose {
	require "./lib/_war_result.cgi";
	&war_lose;
}
sub war_draw {
	require "./lib/_war_result.cgi";
	&war_draw;
}
sub war_escape {
	require "./lib/_war_result.cgi";
	&war_escape;
}


1; # 削除不可
