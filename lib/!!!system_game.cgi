#================================================
# ｹﾞｰﾑ(bj.cgi)でよく使う処理 Created by Merino
#================================================

#================================================
# 国 + 世界 データ書き込み ./log/countries.cgiに書き込み
#================================================
sub write_cs {
	&error("国ﾃﾞｰﾀの書き込みに失敗しました") if $cs{name}[1] eq '';

	# 変数追加する場合は半角ｽﾍﾟｰｽか改行を入れて追加(順不同、並べ替え可)
	my @keys = (qw/
		name bbs_name prison_name strong barrier tax food money soldier state is_die member capacity color
		win_c old_ceo ceo war dom mil pro war_c dom_c mil_c pro_c ceo_continue
		modify_war modify_dom modify_mil modify_pro
		extra extra_limit disaster disaster_limit
		new_commer
	/);
	# 国名　総国力　城壁値　税率　総兵糧　国家予算　総兵士数　状態　滅亡ﾌﾗｸﾞ　所属人数　定員　国色
	# 統一数　旧代表者　代表者　参謀　内政官　策士　外交官　参謀ﾎﾟｲﾝﾄ　内政官ﾎﾟｲﾝﾄ　策士ﾎﾟｲﾝﾄ　外交官ﾎﾟｲﾝﾄ　代表年期
	# 各国設定戦争　内政　軍事　外交
	# 追加効果　追加効果期限　国別災害　国別災害有効期間
	# 新規数
	# -------------------
	# 物資の最大値
	my $max_resource = $w{world} eq '15' ? 300000 : 999999; # 世界情勢[大殺界なら500000まで]
	$cs{food}[$m{country}]    = $max_resource if $cs{food}[$m{country}]    > $max_resource;
	$cs{money}[$m{country}]   = $max_resource if $cs{money}[$m{country}]   > $max_resource;
	$cs{soldier}[$m{country}] = $max_resource if $cs{soldier}[$m{country}] > $max_resource;

	# 拙速
	if ($w{world} eq $#world_states - 5) {
		$cs{state}[$m{country}] = 0;
	}


	my $world_line = &_get_world_line; # 世界情報
	my @lines = ($world_line);
	for my $i (1 .. $w{country}) {
		my $line;
		for my $k (@keys) {
			$line .= "$k;$cs{$k}[$i]<>";
		}
		push @lines, "$line\n";
	}

	open my $fh, "> $logdir/countries.cgi" or &error("国データが開けません");
	print $fh @lines;
	close $fh;
}

#================================================
# 世界情報
#================================================
sub _get_world_line { # Get %w line
	# 変数追加する場合は半角ｽﾍﾟｰｽか改行を入れて追加(順不同、並べ替え可)
	my @keys = (qw/
		country year game_lv limit_time reset_time win_countries player world playing world_sub sub_time twitter_bot half_hour_time
	/);
	# 国の数　年　難易度　統一期限　ﾘｾｯﾄされた時間　前回の統一国(複数)　ﾌﾟﾚｲﾔｰ人数　世界情勢　ﾌﾟﾚｲ中人数　サブ情勢　サブ時間　twitter用カウント　サブ時間の0.5時間版

	my $line = '';
	for my $k (@keys) {
		$line .= "$k;$w{$k}<>";
	}

	# -------------------
	# 友好度/条約
	for my $i (1 .. $w{country}) {
		for my $j ($i+1 .. $w{country}) {
			my $f_c_c  = "f_${i}_${j}";
			my $p_c_c = "p_${i}_${j}";
			$line .= "$f_c_c;$w{$f_c_c}<>";
			$line .= "$p_c_c;$w{$p_c_c}<>";
		}
	}
	$line .= "\n";

	return $line;
}

#================================================
# ﾌﾟﾚｲﾔｰﾃﾞｰﾀ書き込み
#================================================
# turn value stock y_***** は自分のｽﾃｰﾀｽと関係ないので自由に取り回してよい
sub write_user {
	&error("ﾌﾟﾚｲﾔｰﾃﾞｰﾀの書き込みに失敗しました") if !$id || !$m{name};

	$m{ltime} = $time;
	$m{ldate} = $date;

	# -------------------
	# topのﾛｸﾞｲﾝﾘｽﾄに表示
	if ($time > $m{login_time} + $login_min * 60) {
		$m{login_time} = $time;

		open my $fh2, ">> $logdir/login.cgi";
		print $fh2 "$time<>$m{name}<>$m{country}<>$m{shogo}<>$m{mes}<>$m{icon}<>\n";
		close $fh2;
	}

	# -------------------
	# ｽﾃｰﾀｽの最大値
	for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
		$m{$k} = 999 if $m{$k} > 999;
	}
	$m{money}  = 4999999 if $m{money} > 4999999;
	$m{coin}   = 2500000 if $m{coin}  > 2500000;

	# -------------------
	# 変数追加する場合は半角ｽﾍﾟｰｽか改行を入れて追加(順不同、並べ替え可(login_time以外))
	my @keys = (qw/
		login_time ldate start_time mail_address name pass magic_word lib tp lib_r tp_r wt act sex shogo sedai vote vote_year
		country job seed lv exp rank rank_exp super_rank rank_name unit sol sol_lv medal money coin skills renzoku renzoku_c total_auction skills_sub skills_sub2 skills_sub3 money_limit
		max_hp hp max_mp mp at df mat mdf ag cha lea wea wea_c wea_lv wea_name gua egg egg_c pet pet_c shuffle master master_c boch_pet
		marriage lot is_full next_salary icon icon_pet icon_pet_lv icon_pet_exp mes mes_win mes_lose mes_touitsu ltime gacha_time gacha_time2 offertory_time trick_time breed_time silent_time
		rest_a rest_b rest_c

		turn stock value is_playing bank
		y_max_hp y_hp y_max_mp y_mp y_at y_df y_mat y_mdf y_ag y_cha y_lea y_wea y_wea_name y_skills
		y_name y_country y_rank y_sol y_unit y_sol_lv y_icon y_mes_win y_mes_lose y_pet y_value y_gua
		y_rest_a y_rest_b y_rest_c

		nou_c sho_c hei_c gai_c gou_c cho_c sen_c gik_c kou_c tei_c mat_c cas_c tou_c shu_c col_c mon_c
		win_c lose_c draw_c hero_c huk_c met_c war_c dom_c mil_c pro_c esc_c res_c fes_c war_c_t dom_c_t mil_c_t pro_c_t boch_c storm_c
		shogo_t icon_t breed breed_c depot_bonus akindo_guild silent_kind silent_tail guild_number disp_casino chat_java disp_top disp_news disp_chat disp_ad disp_daihyo salary_switch no_boss incubation_switch disp_gacha_time delete_shield
		valid_blacklist pet_icon_switch tutorial_switch
		c_turn c_stock c_value c_type cataso_ratio
		no1_c money_overflow random_migrate ceo_c tam_c ban_c wt_c wt_c_latest

		sox_kind sox_no exchange_count
	/);
	# ﾛｸﾞｲﾝ時間　更新日時　作成日時　名前　ﾊﾟｽﾜｰﾄﾞ　ﾗｲﾌﾞﾗﾘ　ﾀｰﾆﾝｸﾞﾎﾟｲﾝﾄ　待ち時間　疲労度　性別　称号　世代　投票　
	# 所属国　職業　種族　ﾚﾍﾞﾙ　経験値　ﾗﾝｸ　ﾗﾝｸ経験値　兵種　兵士数　士気　勲章　お金　ｺｲﾝ　技(複数)　連続攻めた国　連続ｶｳﾝﾄ　
	# 最大HP　HP　最大MP　MP　力　守り　魔力　魔防　素早　魅力　統率　武器　武器耐久　武器ﾚﾍﾞﾙ　防具　特殊武器名　ﾀﾏｺﾞ　ﾀﾏｺﾞ成長　ﾍﾟｯﾄ　シャッフルフラグ　
	# 結婚相手　宝ｸｼﾞ　預かり所満杯ﾌﾗｸﾞ　次の給与　ｱｲｺﾝ　ﾒｯｾｰｼﾞ　勝ちｾﾘﾌ　負けｾﾘﾌ　統一ｾﾘﾌ　更新時間　ｶﾞﾁｬ時間 ｶﾞﾁｬ時間2 賽銭時間　いたずら解除時間　発言禁止時間
	# ﾀｰﾝ　ｽﾄｯｸ　ﾊﾞﾘｭｰ　ﾌﾟﾚｲ中ﾌﾗｸﾞ　相手ﾃﾞｰﾀ …
	# 農業　商業　徴兵　外交　強奪　諜報　洗脳　偽計　偵察　待伏　ｶｼﾞﾉ　討伐　修行　闘技場　魔物　脱獄　救出　祭　混乱用　ボッチ
	# 戦争勝ち　戦争負け　戦争引分　統一　復興　滅亡　戦争　内政　軍事　外交　
	# 真称号　真ｱｲｺﾝ　育て屋１　育て屋２　預り所ボーナス　商人ギルド　対人ｶｼﾞﾉ表示　交流JAVA表示
	# ｶｼﾞﾉ用 …
	# 隠蔽熟練度
	# _cはカウント(count)の略, y_は相手(you)の略

	my $line;
	for my $k (@keys) {
		$line .= $k =~ /^y_(.+)$/ ? "$k;$y{$1}<>" : "$k;$m{$k}<>";
	}

	open my $fh, "> $userdir/$id/user.cgi";
	print $fh "$line\n";
	print $fh "$addr<>$host<>$agent<>\n";
	close $fh;
}


#================================================
# その他
#================================================
# 待ち時間を秒に変換 + 次へ
sub wait {
	$m{wt} = $GWT * 60;
	$m{wt_c} += $m{wt};
	&n_menu;

	$m{is_playing} = 0;
	--$w{playing};
	$w{playing} = 0 if $w{playing} < 0;
	&write_cs;
}

# 通常時の利用条件
sub is_satisfy { 1 }

# 値をﾘｾｯﾄ
sub refresh {
	$m{lib} = '';
	$m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
}

#================================================
# 疲労状態のときの利用条件
#================================================
sub is_act_satisfy {
	if ($m{act} >= 100) {
		$mes .= '疲労がたまっています。一度内政を行ってください<br>';
		&refresh;
		&n_menu;
		return 1;
	}
	return 0;
}

#================================================
# ｺﾏﾝﾄﾞ汚染ﾁｪｯｸ。期待している値と違う場合は 1(true) が返り&begin(初期ﾒﾆｭｰ表示)
#================================================
sub is_ng_cmd {
	my @check_cmds = @_;

	for $check_cmd (@check_cmds) {
		return 0 if $cmd eq $check_cmd;
	}
	&begin;
	return 1;
}

#================================================
# ﾒｲﾝﾒﾆｭｰなどの処理 main.cgi country.cgi myself.cgi shopping.cgi
#================================================
sub b_menu {
	my @menus = @_;

	if (!$m{is_playing} && $w{playing} >= $max_playing) {
		$mes .= qq|<font color="#FFFF00">ﾌﾟﾚｲ規制中 $w{playing}/$max_playing人</font><br>しばらくお待ちください|;
		&begin;
	}
	elsif (defined $menus[$cmd]) {
		$m{lib} = $menus[$cmd][1];
		$m{tp}   = 1;
		require "./lib/$m{lib}.cgi";

		# lib実行条件okならbeginﾒﾆｭｰ
		&begin if &is_satisfy;

		unless ($m{is_playing}) {
			$m{is_playing} = 1;
			++$w{playing};
			&write_cs;
		}
	}
	else {
		&begin;
	}
}
#================================================
# ﾒﾆｭｰｺﾏﾝﾄﾞ
#================================================
sub menu {
	my @menus = @_;
	my $rest = $m{wt} > 0 ? 1 : 0;
	if ($is_smart) {
		$menu_cmd .= qq|<table boder=0 cols=4 width=110 height=110>|;
		for my $i (0 .. $#menus) {
			if($i % 4 == 0){
				$menu_cmd .= qq|<tr>|;
			}
			next if $menus[$i] eq '';
			my $mline = '';
			my $mpos = 0;
			while (1) {
				my $char_num = 10;
				if ($mpos + $char_num >= length($menus[$i])) {
					$mline .= substr($menus[$i], $mpos);
					last;
				}
				my $last_char = substr($menus[$i], $mpos + $char_num - 1, 2);
				$last_char =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2', $1)/ge;
				my $first1 = substr($last_char, 0, 1);
				my $first2 = substr($last_char, 3, 1);
				if ($first1 eq '%' && $first2 ne '%') {
					$char_num--;
				}
				$mline .= substr($menus[$i], $mpos, $char_num) . "&#13;&#10;";
				$mpos += $char_num;
			}
			$menu_cmd .= qq|<td><form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button1s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#			$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # 拘束中のコマンド入力であることを伝える 飛んだ先で $m{wt} も判定すること
			$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # 多窓させないための一時キー
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|</td>|;
			if($i % 4 == 3){
				$menu_cmd .= qq|</tr>|;
			}
		}
		if($#menus % 4 != 3){
			$menu_cmd .= qq|</tr>|;
		}
		$menu_cmd .= qq|</table>|;

	}
	elsif ($is_appli) {
		$menu_cmd .= qq|<div align="left" id="commands">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			$menu_cmd .= qq|<form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$menus[$i]" class="button2s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#			$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # 拘束中のコマンド入力であることを伝える 飛んだ先で $m{wt} も判定すること
			$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # 多窓させないための一時キー
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|<br class="cmd_br" />| if ($i+1) % 7 == 0;
		}
		$menu_cmd .= qq|<br class="cmd_br" /></div>|;
	}
	else{
		$menu_cmd .= qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			$menu_cmd .= qq|<option value="$i">$menus[$i]</option>|;
		}
		$menu_cmd .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#		$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # 拘束中のコマンド入力であることを伝える 飛んだ先で $m{wt} も判定すること
		$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # 多窓させないための一時キー
		$menu_cmd .= $is_mobile ? qq|<br><input type="submit" value="決 定" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<br><input type="submit" value="決 定" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
	}

#	return $menu_cmd if $rest; # 拘束中は $menu_cmd が表示されないルートを通るので、とりあえず拘束中のコマンドはここで返る文字列を $mes に足して表示する
=pod
	if($is_smart){
		$menu_cmd .= qq|<div>|;
#		$menu_cmd .= qq|<div style="float:right;">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			my $mline = '';
			my $mpos = 0;
			while (1) {
				my $char_num = 10;
				if ($mpos + $char_num >= length($menus[$i])) {
					$mline .= substr($menus[$i], $mpos);
					last;
				}
				my $last_char = substr($menus[$i], $mpos + $char_num - 1, 2);
				$last_char =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2', $1)/ge;
				my $first1 = substr($last_char, 0, 1);
				my $first2 = substr($last_char, 3, 1);
				if ($first1 eq '%' && $first2 ne '%') {
					$char_num--;
				}
				$mline .= substr($menus[$i], $mpos, $char_num) . "&#13;&#10;";
				$mpos += $char_num;
			}
			$menu_cmd .= qq|<form method="$method" action="$script" class="cmd_form">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button2s"><input type="hidden" name="cmd" value="$i">|;
#			$menu_cmd .= qq|<input type="submit" value="$menus[$i]" class="button2s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
#			print "$i ", ($i+1) % 4, " " , ($i+1) % 6, "<br>";

#			$menu_cmd .= qq|</div>| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
			$menu_cmd .= qq|<br class="smart_br" />| if ($i+1) % 4 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr" />| if ($i+1) % 4 == 0;
			$menu_cmd .= qq|<br class="tablet_br" />| if ($i+1) % 7 == 0;
#			$menu_cmd .= qq|<hr class="tablet_hr" />| if ($i+1) % 7 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr">| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
		}
		$menu_cmd .= qq|</div>|;
#		$menu_cmd .= qq|<br style="display:none;">|;
	}
=cut

}
#================================================
# Nextﾒﾆｭｰ
#================================================
sub n_menu {
	$menu_cmd  = qq|<form method="$method" action="$script">|;
	$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= $is_mobile ? qq|<input type="submit" value="Next" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="Next" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
}
#================================================
# 携帯用Pager 次へ前へ shopping_hospital.cgi
#================================================
sub pager_next {
	my $page = shift;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="cmd" value="$cmd"><input type="hidden" name="page" value="$page">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="次のﾍﾟｰｼﾞ" class="button1"></form>|;
}
sub pager_back {
	my $page = shift;
	$page = 0 if $page < 0;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="cmd" value="$cmd"><input type="hidden" name="page" value="$page">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="前のﾍﾟｰｼﾞ" class="button1"></form>|;
}

#================================================
# 熟練度ｱｯﾌﾟ
#================================================
sub c_up { # count up
	my $c = shift;
	++$m{$c};

	# 連続でc_upされる用としてｸﾞﾛｰﾊﾞﾙな退避変数と判定に必要な配列作成
	if ($cash_c ne $c) {
		$cash_c = $c;
		@cash_shogos = ();
		for my $shogo (@shogos) {
			my($k) = keys %{ $shogo->[1] }; # なせかeachだと2回目がとれない…
			push @cash_shogos, [$shogo->[0], $shogo->[1]->{$k}, $shogo->[2]] if $c eq $k;
		}
	}

	for my $cash_shogo (@cash_shogos) {
		if ($cash_shogo->[1] eq $m{$c}) {
			&mes_and_world_news("$cash_shogo->[0]の称号を与えられました", 1);
			$m{money} += $cash_shogo->[2];
			$mes .= "$cash_shogo->[2]Gの報奨金を受け取りました<br>";
		}
	}
}

#================================================
# 代表者ﾎﾟｲﾝﾄｱｯﾌﾟ
#================================================
sub daihyo_c_up {
	my $c = shift;
	++$m{$c};

	my($k) = $c =~ /^(.+)_c$/;
	if ($cs{$k}[$m{country}] eq $m{name}) {
		$cs{$c}[$m{country}] = $m{$c};
	}
	elsif (!&is_daihyo && $m{$c} > $cs{$c}[$m{country}] && $m{$c} >= 10) {
		&mes_and_world_news(qq|<font color="#FF9999">★日頃の国への貢献が認められ$cs{name}[$m{country}]代表\の$e2j{$k}に任命されました★</font>|,1);
		$cs{$k}[$m{country}] = $m{name};
		$cs{$c}[$m{country}] = $m{$c};
	}
}



#================================================
# 国にいるプレイヤー名取得
#================================================
sub get_country_members {
	my $country = shift;
	&error("国No[ $country ] その国が存在しないよ") unless -d "$logdir/$country";

	my @lines = ();
	open my $fh, "< $logdir/$country/member.cgi" or &error("国$countryプレイヤーデータが開けません");
	push @lines, $_ while <$fh>;
	close $fh;

	return @lines;
}


#================================================
# 他ﾌﾟﾚｲﾔｰにｱｲﾃﾑを郵送
#================================================
sub send_item {
	my($send_name, $kind, $item_no, $item_c, $item_lv) = @_;
	my $send_id = unpack 'H*', $send_name;
	$item_c  ||= 0;
	$item_lv ||= 0;

	if (-f "$userdir/$send_id/depot.cgi") {
		open my $fh, ">> $userdir/$send_id/depot.cgi";
		print $fh "$kind<>$item_no<>$item_c<>$item_lv<>\n";
		close $fh;

		open my $fh2, "> $userdir/$send_id/depot_flag.cgi";
		close $fh2;
	}
}

#================================================
# 他ﾌﾟﾚｲﾔｰにお金を送金
#================================================
sub send_money {
	my($send_name, $from_name, $money, $is_shop_sale) = @_;
	my $send_id = unpack 'H*', $send_name;
	$is_shop_sale||= 0;

	if (-f "$userdir/$send_id/money.cgi") {
		open my $fh, ">> $userdir/$send_id/money.cgi";
		print $fh "$from_name<>$money<>$is_shop_sale<>\n";
		close $fh;
	}
}


#================================================
# 表示しつつﾆｭｰｽにも書き込む
#================================================
sub mes_and_world_news {
	my $message = shift;
	$mes .= "$message<br>";
	  $message =~ /^<b>/  ? &write_world_news("<b>$c_mの$m{name}が</b>$message", @_)
	: $message =~ /^<i>/  ? &write_world_news("<i>$c_mの$m{name}が</i>$message", @_)
	: $message =~ /^<em>/ ? &write_world_news("<em>$c_mの$m{name}が</em>$message", @_)
	:					    &write_world_news("$c_mの$m{name}が$message", @_)
	;
}
sub mes_and_send_news {
	my $message = shift;
	$mes .= "$message<br>";
	  $message =~ /^<b>/  ? &write_send_news("<b>$c_mの$m{name}が</b>$message", @_)
	: $message =~ /^<i>/  ? &write_send_news("<i>$c_mの$m{name}が</i>$message", @_)
	: $message =~ /^<em>/ ? &write_send_news("<em>$c_mの$m{name}が</em>$message", @_)
	:					    &write_send_news("$c_mの$m{name}が$message", @_)
	;
}

#================================================
# 過去の栄光、物流情報ログ書き込み処理
#================================================
#sub write_world_news     { &_write_news('world_news', @_) }
sub write_world_news     {
	my($message, $is_memory, $memory_name) = @_;
	if ($w{world} ne '17' || $message =~ /^</) { # ”世界情勢【沈黙】以外”または大きな出来事
		&_write_news('world_news', @_);
	}
	elsif ($is_memory) { # 世界情勢【沈黙】で戦歴フラグがあった場合
		$message = &coloration_country($message);
		&write_memory($message, $memory_name);
	}
}
sub write_send_news      { &_write_news('send_news',  @_) }
sub write_blog_news      { &_write_news('blog_news',  @_) }
sub write_colosseum_news { &_write_news('colosseum_news',  @_) }
sub write_picture_news   { &_write_news('picture_news',  @_) }
sub write_book_news      { &_write_news('book_news',  @_) }
sub _write_news {
	my($file_name, $message, $is_memory, $memory_name) = @_;

	&write_world_big_news($message) if $message =~ /^</;
	$message = &coloration_country($message);

	my @lines = ();
	open my $fh, "+< $logdir/$file_name.cgi" or &error("$file_name.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	&write_memory($message, $memory_name) if $is_memory;
}
#================================================
# 世界の流れ
#================================================
sub write_world_big_news {
	my $message = shift;

	$message = &coloration_country($message);
	my @lines = ();
	open my $fh, "+< $logdir/world_big_news.cgi" or &error("$logdir/world_big_news.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

# ------------------
# 国名があれば色付け
sub coloration_country {
	my $message = shift;
	return $message if $w{country} < 1;
	for my $i (0 .. $w{country}) {
		my $add_color_country = qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font>|;
		$message =~ s/\Q$cs{name}[$i]\E/$add_color_country/g;
	}
	return $message;
}

#================================================
# 石碑
#================================================
sub write_legend {
	my($file_name, $message, $is_memory, $memory_name) = @_;

	my @lines = ();
	open my $fh, "+< $logdir/legend/$file_name.cgi" or &error("$logdir/legend/$file_name.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	$message = &coloration_country($message);
	unshift @lines, qq|$world_name暦$w{year}年【$world_states[$w{world}]】：$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	&write_memory($message, $memory_name) if $is_memory;
}

#================================================
# 思い出ログ書き込み処理
#================================================
# 引数に名前がある場合は、その人の戦歴に、ない場合は自分の戦歴に書き込まれる
sub write_memory {
	my($message, $memory_name) = @_;
	$m_id = $memory_name ? unpack 'H*', $memory_name : $id;

	return unless -f "$userdir/$m_id/memory.cgi";

	my @lines = ();
	open my $fh, "+< $userdir/$m_id/memory.cgi" or &error("Memoryﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


#================================================
# 自分と相手の強さ判別  2:強い 1:普通 0:弱い
#================================================
sub st_lv {
	my $y_st = shift || &y_st;
	my $m_st =          &m_st;

	return $y_st > $m_st * 1.5 ? 2
		:  $y_st < $m_st * 0.5 ? 0
		:                        1
		;
}
sub y_st { int($y{max_hp} + $y{max_mp} + $y{at} + $y{df} + $y{mat} + $y{mdf} + $y{ag} + $y{cha}*0.5) }
sub m_st { int($m{max_hp} + $m{max_mp} + $m{at} + $m{df} + $m{mat} + $m{mdf} + $m{ag} + $m{cha}*0.5) }

#================================================
# 災害 滅亡時低確率、ﾛﾌﾟﾄ使用時
#================================================
sub disaster {
	my $more = shift;
	my @disasters = (
		['自然災害','food'],
		['経済破綻','money'],
		['大地震','soldier'],
	);
	if ($more) {
		push @disasters, ['一定時間国防が脆弱化','paper'];
		push @disasters, ['一定時間指揮系統が混乱','mismatch'];
		push @disasters, ['大泥棒が出現','concentrate'];
		unless ($w{world} eq $#world_states || $w{world} eq $#world_states-1 || $w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-4 || $w{world} eq $#world_states-5) {
			push @disasters, ['魔人復活','strong'];
		}
		if ($w{world} eq '12') {
			push @disasters, ['大飢饉', 'big_food'];
			push @disasters, ['大恐慌', 'big_money'];
			push @disasters, ['大津波', 'big_soldier'];
		}
	}
	my $v = int(rand(@disasters));
	if ($disasters[$v][1] eq 'food' || $disasters[$v][1] eq 'money' || $disasters[$v][1] eq 'soldier') {
		for my $i (1 .. $w{country}) {
			next if $cs{ is_die }[$i];
			$cs{ $disasters[$v][1] }[$i] = int($cs{ $disasters[$v][1] }[$i] * 0.5);
		}
		&write_world_news("<b>世界中に $disasters[$v][0] が起こりました</b>");
	} elsif ($disasters[$v][1] eq 'strong' && $m{country}) {
		my $target = &get_most_strong_country(1);
		$cs{ $disasters[$v][1] }[$target] -= int(rand(10)+5) * 100;
		&write_world_news("<b>$cs{name}[$target]に $disasters[$v][0] が起こりました</b>");
	} elsif (($disasters[$v][1] eq 'paper' || $disasters[$v][1] eq 'mismatch') && $m{country}) {
		my $target = &get_most_strong_country(1);
		$cs{disaster}[$target] = $disasters[$v][1];
		$cs{disaster_limit}[$target] = $time + 1 * 60 * 60;
		&write_world_news("<b>$cs{name}[$target]で $disasters[$v][0] しました</b>");
	} elsif ($disasters[$v][1] eq 'concentrate') {
		my @rlist = ('food', 'money', 'soldier');
		my $r = $rlist[int(rand(@rlist))];
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i];
			next if $i eq $m{country};
			$cs{$r}[$i] = int($cs{$r}[$i] * 0.5);
			$cs{$r}[$m{country}] += $cs{$r}[$i];
		}
		&write_world_news("<b>世界中に $disasters[$v][0] しました</b>");
	} elsif ($disasters[$v][1] =~ 'big_(.*)') {
		$r = $1;
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i];
			$cs{$r}[$i] = int($cs{$r}[$i] * 0.1);
		}
		&write_world_news("<b>世界中に $disasters[$v][0] が起こりました</b>");
	}
}

#================================================
# 相手ﾃﾞｰﾀがあるかチェック
#================================================
sub you_exists {
	my($name, $is_unpack) = @_;

	my $y_id = $is_unpack ? $name : unpack 'H*', $name;

	if (-f "$userdir/$y_id/user.cgi") {
		return 1;
	}
	return 0;
}
#================================================
# 相手ﾃﾞｰﾀをGet 戻り値はハッシュ
#================================================
# 使い方: &get_you_datas('相手の名前');
sub get_you_datas {
	my($name, $is_unpack) = @_;

	my $y_id = $is_unpack ? $name : unpack 'H*', $name;

	open my $fh, "< $userdir/$y_id/user.cgi" or &error("そのようなﾌﾟﾚｲﾔｰは存在しません");
	my $line_data = <$fh>;
	my $line_info = <$fh>;
	close $fh;

	my($paddr, $phost, $pagent) = split /<>/, $line_info;

	my %you_datas = (
		addr	=> $paddr,
		host	=> $phost,
		agent	=> $pagent,
	);
	for my $hash (split /<>/, $line_data) {
		my($k, $v) = split /;/, $hash;
		next if $k =~ /^y_/;

		$you_datas{$k} = $v;
	}

	return %you_datas;
}

#================================================
# 相手ﾃﾞｰﾀ変更  結婚時と闘技場の熟練度UP時に使用
#================================================
# 使い方: &regist_you_data('相手の名前', '変更したい変数', '値');
sub regist_you_data {
	my($name, $k, $v) = @_;
	return if $name eq '' || $k eq '';

	my $y_id = unpack 'H*', $name;
	return unless -f "$userdir/$y_id/user.cgi";

	open my $fh, "+< $userdir/$y_id/user.cgi" or &error("$userdir/$y_id/user.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my $line_info = <$fh>;
	$line =~ s/<>($k;).*?<>/<>$1$v<>/;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	print $fh $line_info;
	close $fh;
}
#================================================
# 相手ﾃﾞｰﾀ変更  結婚時と闘技場の熟練度UP時に使用
#================================================
# my @array = (['変更したい変数1', '値1'], ['変更したい変数2', '値2']);
# &regist_you_array('相手の名前', @array);
sub regist_you_array {
	my $name = shift;
	my @data = @_;
	return if $name eq '' || !@data;

	my $y_id = unpack 'H*', $name;
	return unless -f "$userdir/$y_id/user.cgi";

	# 書き換え対象によっては待ち伏せを解除 1度やれば済むので2回目以降はなし
	my $bool = 0;
	for my $i (0 .. $#data) {
		last if $bool;
		my $k = $data[$i][0];
		my $v = $data[$i][1];

		if ($k eq 'lib' || $k eq 'value') {
			my %you_datas = &get_you_datas($y_id,1);
			if(($k eq 'lib' && $you_datas{lib} eq 'military' && $you_datas{tp} eq '610') || ($k eq 'value' && $you_datas{value} eq 'military_ambush')){
				$bool = 1;
				my @lines = ();
				open my $fh, "+< $logdir/$you_datas{country}/patrol.cgi" or &error("$logdir/$you_datas{country}/patrol.cgiﾌｧｲﾙが開けません");
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					my($pat_time,$p_name) = split /<>/, $line;
					next if $p_name eq $name;
					push @lines, $line;
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
			}
		}
	}

	open my $fh, "+< $userdir/$y_id/user.cgi" or &error("$userdir/$y_id/user.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my $line_info = <$fh>;
	for my $i (0 .. $#data) {
		my $k = $data[$i][0];
		my $v = $data[$i][1];

		if(index($line, "<>$k;") >= 0){
			$line =~ s/<>($k;).*?<>/<>$1$v<>/;
		}else{
			$line = "$k;$v<>" . $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	print $fh $line_info;
	close $fh;
}

#================================================
# 牢獄に追加
#================================================
sub add_prisoner {
	$mes .= "$m{name}は、敵国兵に取り囲まれ捕まってしまった!<br>";
	$mes .= "牢獄へ連行されます。次に行動できるのは$GWT分後です<br>";

	$m{lib} = 'prison';
	$m{renzoku_c} = $m{act} = 0;
	$m{tp} = 100;
	&wait;

	# 牢獄ﾘｽﾄに追加
	open my $fh, ">> $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi が開けません");
	print $fh "$m{name}<>$m{country}<>\n";
	close $fh;

	require './lib/_bbs_chat.cgi';
	$this_file = "$logdir/$y{country}/bbs";
	$in{comment} = "$m{mes_lose}【朗報】$m{name}が牢獄に連行されました";
	$bad_time = 0;
	&write_comment;
}

#================================================
# 国力が一番高い国
#================================================
=pod
sub get_most_strong_country {
	my $country = 0;
	my $max_value = 0;
	for my $i (1 .. $w{country}) {
		next if $i eq $m{country};
		next if $i eq $union;
		if ($cs{strong}[$i] > $max_value) {
			$country = $i;
			$max_value = $cs{strong}[$i];
		}
	}
	return $country;
}
=cut
sub get_most_strong_country {
	my $skip_my_country = shift;
	my $country = 0;
	my $max_value = 0;
	for my $i (1 .. $w{country}) {
		if (!$skip_my_country) {
			next if $i eq $m{country};
			next if $i eq $union;
		}
		if ($cs{strong}[$i] > $max_value) {
			$country = $i;
			$max_value = $cs{strong}[$i];
		}
	}
	return $country;
}
# NPCデータ作成
sub add_npc_data {
	my $country = shift;

	my %npc_statuss = (
		max_hp => [999, 600, 400, 300, 99],
		max_mp => [999, 500, 200, 100, 99],
		at     => [999, 400, 300, 200, 99],
		df     => [999, 300, 200, 100, 99],
		mat    => [999, 400, 300, 200, 99],
		mdf    => [999, 300, 200, 100, 99],
		ag     => [999, 500, 300, 200, 99],
		cha    => [999, 400, 300, 200, 99],
		lea    => [666, 400, 250, 150, 99],
		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
	);
	my @npc_weas = (
	#	[0]属性[1]武器No	[2]必殺技
		['無', [0],			[61..65],],
		['剣', [1 .. 5],	[1 .. 5],],
		['槍', [6 ..10],	[11..15],],
		['斧', [11..15],	[21..25],],
		['炎', [16..20],	[31..35],],
		['風', [21..25],	[41..45],],
		['雷', [26..30],	[51..55],],
	);
	my $line = qq|\@npcs = (\n|;
	my @npc_names = (qw/vipqiv(NPC) kirito(NPC) 亀の家庭医学(NPC) pigure(NPC) ウェル(NPC) vipqiv(NPC) DT(NPC) ハル(NPC) アシュレイ(NPC) ゴミクズ(NPC)/);

	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;

		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}

		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;

		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	$line .= qq|);\n\n1;\n|;

	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}
#================================================
# データ修正
#================================================
sub cs_data_repair{
	&read_cs;
	my %members = ();

	my $count = 0;
	opendir my $dh, "$userdir" or &error("ﾕｰｻﾞｰﾃﾞｨﾚｸﾄﾘが開けません");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %p = &get_you_datas($pid, 1);

		if ($p{country} > $w{country}) {
			if ($p{name} ne $m{name}) {
				&regist_you_data($p{name}, 'country', 0);
			} else {
				$m{country} = 0;
			}
			$p{country} = 0;
		}

		push @{ $members{$p{country}} }, "$p{name}\n";
		++$count;
	}
	closedir $dh;
	$w{player} = $count;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	my $ave_c = int($w{player} / $country);

	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgiﾌｧｲﾙが開けません");
		print $fh @{ $members{$i} };
		close $fh;

		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $w{country} - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $w{country} - 2 ? 0:$ave_c;

		for my $k (qw/dom war mil pro/) {
			if ($cs{$k}[$i] eq '') {
				$cs{$k . '_c'}[$i] = 0;
			}
		}
	}
	&write_cs;
}
#================================================
# 階級名取得
#================================================
sub get_rank_name {
	my($rank, $name) = @_;
	my $is_ceo = 0;
	if ($name) {
		for my $i (1..$w{country}) {
			if ($name eq $cs{ceo}[$i]) {
				$is_ceo = 1;
			}
		}
	}
	if ($rank == $#ranks && $is_ceo) {
		return '皇帝';
	}
	return $ranks[$rank];
}

#================================================
# アイテム名取得
# 第１引数と第２引数だけで名前
# 第３引数まででﾍﾟｯﾄだけ★情報追加 ｼﾞｬﾝｸでﾍﾟｯﾄだけ★情報使うので
# 第４引数まで指定すると全アイテム情報追加
# 第５引数はアイテムの種類を非表示 ショップなど一部では種類が非表示なので
# $kind アイテムの種類(1武器 2卵 3ﾍﾟｯﾄ 4防具)
# $item_no アイテムの番号
# $item_c アイテムが持つ数値(耐久値 孵化値 ★ なし)
# $item_lv アイテムのレベル(★ なし なし なし)
# $flag 1 で種類表示オフ
# 新しいアイテム種を追加したらここを変更すること
#================================================
sub get_item_name {
	my($kind, $item_no, $item_c, $item_lv, $flag) = @_;

	my $result;
	if (defined($item_lv)) { # 全引数有効ならアイテム情報
		$result = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])"
				  : $kind eq '2' ? "[卵]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
				  : $kind eq '3' ? "[ぺ]$pets[$item_no][1]★$item_c"
				  :                "[$guas[$item_no][2]]$guas[$item_no][1]"
			  ;
		$result = substr($result, 4) if $flag; # $flag が有効ならアイテム種を非表示
	}
	else { # 全引数有効じゃないならアイテム名
		$result = $kind eq '1' ? "$weas[$item_no][1]"
				  : $kind eq '2' ? "$eggs[$item_no][1]"
				  : $kind eq '3' ? (defined($item_c) ? "$pets[$item_no][1]★$item_c" : "$pets[$item_no][1]") # 第３引数有効かつﾍﾟｯﾄならレベル付加
				  :                "$guas[$item_no][1]"
				  ;
	}
	return $result;
}
sub after_success_action { # 行動の成功後の共通処理
	my $action = shift; # 行動種
	my $v = shift; # 行動に伴う何らかのデータ

	#if ($w{world} eq $#world_states-4) {
		#require './lib/fate.cgi';
		#&super_attack($action);
		#&super_attack('single') if ($action eq 'war') && $v;
	#}
}
sub remove_pet { # ﾍﾟｯﾄ外す処理
	$m{pet} = 0;
	$m{icon_pet} = '';
	$m{icon_pet_lv} = 0;
	$m{icon_pet_exp} = 0;
}

1; # 削除不可
