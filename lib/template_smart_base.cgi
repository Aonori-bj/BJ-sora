#================================================
# 携帯ｹﾞｰﾑ画面 Created by Merino
#================================================

#================================================
# ﾒｲﾝ
#================================================
print qq|資金 $m{money} G<br>| if $m{lib} =~ /^shopping/ || $m{lib_r} =~ /^shopping/;
#if (!$mes && ($m{wt} > 1 || $m{lib} eq '') ) {
if ($m{lib_r} eq '' && ($mes && $m{wt} > 1) || (!$mes && $m{lib} eq '') ) {
#if (!$mes && ($is_battle ne 1 && $is_battle ne 2) ) {
	# 最新情報
	open my $fh, "< $logdir/world_news.cgi" or &error("$logdir/world_news.cgiﾌｧｲﾙが読み込めません");
	my $line = <$fh>;
	close $fh;
	print qq|<hr>|;
	print qq|◎最新情報◎<br>$line|;
	# ﾁｭｰﾄﾘｱﾙﾓｰﾄﾞ時のｸｴｽﾄ情報
=pod
	if ($m{tutorial_switch}) {
		require './lib/tutorial.cgi';
		if ($m{country} == 0) { # ﾈﾊﾞﾗﾝでは仕官催促固定
			print qq|<hr>◎ﾁｭｰﾄﾘｱﾙ◎<br>|;
			print qq|「国情報」→「仕官」から国を選ぶことで仕官できます|;
		}
		elsif ($m{tutorial_quest_stamp_c} < $tutorial_quest_stamps) {
			print qq|<hr>◎ｸｴｽﾄ情報◎<br>|;
			my $quest = &show_quest;
			print qq|$quest$tutorial_mes|;
		}
	}
=cut
	print qq|<hr>|;
}
#print qq|<a name="menu">$menu_cmd</a><br>$mes<br>|;
print qq|$menu_cmd|;
print qq|<br>| unless $menu_cmd;
print qq|$mes$tutorial_mes| if $mes;

if ($is_battle eq '1') {
	&battle_html;
}
elsif ($is_battle eq '2') {
	&war_html;
}
elsif ($m{lib} eq '' || $m{lib} eq 'prison') {
	&check_flag;
	&status_html;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
	&promise_table_html;
}
elsif ($m{wt} > 0) {
	&check_flag;
	&my_country_info if $m{country};
	&top_menu_html;
	&countries_info;
	&promise_table_html;
}
elsif ($m{lib} =~ /(domestic|hunting|military|promise|training|war_form)/ && $m{tp} eq '1') {
	print qq|<hr>|;
	if ($m{pet} > 0) { print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1]★$m{pet_c}</font><br>|; }
	elsif ($m{pet} < 0) { print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1](<b>$m{pet_c}</b>/<b>$pets[$m{pet}][5]</b>)</font><br>|; }
	print qq|<font color="#99CC99">ﾀﾏｺﾞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
}
#================================================
# ﾄｯﾌﾟﾒﾆｭｰ
#================================================
sub top_menu_html {
	print qq|<hr>|;
	my $country_menu = '';
	$country_menu .= qq|<tr><td><form method="$method" action="chat_prison.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="牢獄" class="button1s"></form></td>|;
	$country_menu .= qq|<td><form method="$method" action="bbs_country.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="作戦会議室" class="button1s"></form></td>|;

	# 同盟国があるなら
	if ($union) {
		$country_menu .= qq|<td><form method="$method" action="bbs_union.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="同盟会議室" class="button1s"></form></td>|;
	}
	$country_menu .= qq|</tr>|;

	$country_menu .= qq|<tr>|;

	# 世界情勢暗黒のみ
	if (($w{world} eq $#world_states) && $m{country} ne $w{country}) {
		$country_menu .= qq|<td><form method="$method" action="bbs_vs_npc.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="＋ 封 印 会 議 ＋" class="button1s"></form></td>|;
	}

	# ギルド加盟なら
#	if ($m{akindo_guild}) {
#		$country_menu .= qq|<td><form method="$method" action="bbs_akindo.cgi">|;
#		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#		$country_menu .= qq|<input type="submit" value="ギルド" class="button1s"></form></td>|;
#	}

	$country_menu .= qq|<td><form method="$method" action="chat_casino.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="対人ｶｼﾞﾉ" class="button1s"></form></td>|;

	unless ($m{disp_daihyo} eq '0'){
		$country_menu .= qq|<td><form method="$method" action="bbs_daihyo.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="代表\評議会" class="button1s"></form></td>|;
	}
	if($m{disp_casino}){
		#require "$datadir/casino.cgi";
		#my $a_line = &all_member_n;
		#$country_menu .= qq|</tr><tr><td colspan=3>$a_line</td>|;
	}

	if (&is_sabakan){
		$country_menu .= qq|<td>|;
		$country_menu .= qq|<form method="$method" action="chat_admin.cgi">|;
		$country_menu .= qq|<input type="submit" value="運営討論場" class="button1s">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|</form>|;
		$country_menu .= qq|</td>|;
	}

	$country_menu .= qq|</tr>|;

	print qq|<table boder=0 cols=5 width=90 height=90>|;
	print qq|<tr>|;
	print qq|<td>|;
	print qq|<form action="$script_index">|;
	print qq|<input type="submit" value="Ｔ Ｏ Ｐ" class="button1s">|;
	print qq|</form>|;
	print qq|</td>|;
	unless ($m{disp_news} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="news.cgi">|;
		print qq|<input type="submit" value="過去の栄光" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}
	print qq|<td>|;
	print qq|<form method="$method" action="bbs_public.cgi">|;
	print qq|<input type="submit" value="掲 示 板" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;
	print qq|</td>|;
	print qq|</tr>|;
	print qq|<tr>|;
	unless ($m{disp_chat} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="chat_public.cgi">|;
		print qq|<input type="submit" value="交流広場" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}
	print qq|<td>|;
	print qq|<form method="$method" action="chat_horyu.cgi">|;
	print qq|<input type="submit" value="改造案投票所" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;
	print qq|</td>|;
	unless ($m{disp_ad} eq '0'){
		print qq|<td>|;
		print qq|<form method="$method" action="bbs_ad.cgi">|;
		print qq|<input type="submit" value="宣伝言板" class="button1s">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		print qq|</td>|;
	}
	print qq|<td>|;
	print qq|<form method="$method" action="letter.cgi">|;
	print qq|<input type="submit" value="Ｍｙ Ｒｏｏｍ" class="button1s">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|</form>|;
	print qq|</td>|;
	print qq|</tr>|;
	print qq|$country_menu|;
	print qq|</table>|;

	print qq|<hr>|;
}

#================================================
# ｽﾃｰﾀｽ画面
#================================================
sub status_html {
	print qq|<hr><img src="$icondir/$m{icon}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon};
	print qq|<img src="$icondir/pet/$m{icon_pet}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon_pet} && $m{pet_icon_switch};
	print qq|$m{name}|;
	print qq|[$m{shogo}]| if $m{shogo};
	print qq|<br>|;
#	print qq|称号 $m{shogo}<br>| if $m{shogo};
#	print $m{name}, "[$m{shogo}]<br>";

	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		print qq|結婚相手 <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	if ($m{master}){
		if($m{master_c}){
			print qq|師匠 <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
		}else{
			$mid = unpack 'H*', $m{master};
			if (-f "$userdir/$mid/user.cgi") {
				$master = qq|弟子 <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
			} else {
				$master = qq|弟子 <font color="#FF0000">$m{master} 死亡</font><br>|;
			}
		}
	}
	if($m{country} && $m{wt} <= 0){
		my $next_rank = $m{rank} * $m{rank} * 10;
		my $nokori_time = $m{next_salary} - $time;
		$nokori_time = 0 if $nokori_time < 0;
		my $nokori_time_mes = sprintf("<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後", $nokori_time / 3600, $nokori_time % 3600 / 60, $nokori_time % 60);
		my $reset_rest = int($w{reset_time} - $time);
		my $gacha_time = $m{gacha_time} - $time;
		$gacha_time = 0 if $gacha_time < 0;
		my $gacha_time_mes = sprintf("<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後", $gacha_time / 3600, $gacha_time % 3600 / 60, $gacha_time % 60);
		my $gacha_time2 = $m{gacha_time2} - $time;
		$gacha_time2 = 0 if $gacha_time2 < 0;
		my $gacha_time2_mes = sprintf("<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後", $gacha_time2 / 3600, $gacha_time2 % 3600 / 60, $gacha_time2 % 60);
		my $offertory_time = $m{offertory_time} - $time;
		$offertory_time = 0 if $offertory_time < 0;
		my $offertory_time_mes = sprintf("<b>%d</b>時<b>%02d</b>分<b>%02d</b>秒後", $offertory_time / 3600, $offertory_time % 3600 / 60, $ofertory_time % 60);

#		print qq|<hr size="1">|;
		print qq|$units[$m{unit}][1] <b>$rank_sols[$m{rank}]</b>兵<br>|;
		#my $rank_name = &get_rank_name($m{rank}, $m{name});
		if ($m{super_rank}){
			$rank_name = '';
			$rank_name .= '★' for 1 .. $m{super_rank};
			$rank_name .= $m{rank_name};
		}
		print qq|$rank_name $e2j{rank_exp} [ <b>$m{rank_exp}</b> / <b>$next_rank</b> ]<br>|;
		print qq|敵国[前回：<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> 連続<b>$m{renzoku_c}</b>回]<br>| if $m{renzoku_c};
		print qq|<hr size="1">|;
		if ($m{disp_gacha_time}) {
#			print qq|残り時間<br>\n|;
			print qq|<table class="table1s">|;
			print qq|<tr><th>給与</th><th>賽銭</th></tr>\n|;
			print qq|<tr><td><span id="nokori_time">$nokori_time_mes</span></td><td><span id="offertory_time">$offertory_time_mes</span></td></tr>\n|;
			print qq|<tr><th>ガチャ</th><th>ガチャ（高）</th></tr>\n|;
			print qq|<tr><td><span id="gacha_time">$gacha_time_mes</span></td><td><span id="gacha_time2">$gacha_time2_mes</span></td></tr>\n|;
			print qq|</table>|;
		} else {
			print qq|給与まで残り <span id="nokori_time">$nokori_time_mes</span>\n|;
		}
		print qq|<script type="text/javascript"><!--\n nokori_time($nokori_time, $reset_rest, $gacha_time, $gacha_time2, $offertory_time);\n// --></script>\n|;
		print qq|<br>|;
	}
	print qq|<b>$m{sedai}</b>世代目 $sexes[$m{sex}]<br>|;
	print qq|Lv.<b>$m{lv}</b> [$jobs[$m{job}][1]][$seeds{$m{seed}}[0]]<br>|;
	print qq|疲労度 <b>$m{act}</b>%<br>|;
	print qq|経験値 [<b>$m{exp}</b>/<b>100</b>]<br>|;
#	print qq|Lv.<b>$m{lv}</b> Exp[$m{exp}/100]<br>|;
	print qq|資金 <b>$m{money}</b> G<br>|;
	print qq|勲章<b>$m{medal}</b>個<br>|;
	print qq|ｺｲﾝ <b>$m{coin}</b>枚<br>|;
	print qq|宝ｸｼﾞ【$m{lot}】<br>|;
	print qq|<font color="#CC9999">$e2j{hp} [<b>$m{hp}</b>/<b>$m{max_hp}</b>]</font><br>|;
	print qq|<font color="#CC99CC">$e2j{mp} [<b>$m{mp}</b>/<b>$m{max_mp}</b>]</font><br>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	print qq|<font color="#9999CC">武器:[$weas[$m{wea}][2]]$wname★<b>$m{wea_lv}</b>(<b>$m{wea_c}</b>/<b>$weas[$m{wea}][4]</b>)</font><br>| if $m{wea};
	print qq|<font color="#9999CC">防具:[$guas[$m{gua}][2]]$guas[$m{gua}][1]</font><br>| if $m{gua};
	my $icon_pet_lv = " Lv.<b>$m{icon_pet_lv}</b>" if $m{icon_pet} && $m{pet_icon_switch};
	if ($m{pet} > 0) { print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1]★$m{pet_c}$icon_pet_lv</font><br>|; }
	elsif ($m{pet} < 0) { print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1](<b>$m{pet_c}</b>/<b>$pets[$m{pet}][5]</b>)$icon_pet_lv</font><br>|; }
	print qq|<font color="#99CC99">ﾀﾏｺﾞ:$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>| if $m{egg};
	print qq|<font color="#CCCC99">虫  :$m{insect_name}</font><br>| if $m{insect_name};
#	print qq|<hr>|;
}

#================================================
# 手紙、荷物ﾁｪｯｸ
#================================================
sub check_flag {
	if (-f "$userdir/$id/temp_mes.cgi") {
		open my $fh, "< $userdir/$id/temp_mes.cgi";
		my $line = <$fh>;
		close $fh;
		print qq|<hr><font color="#FF0000">$line</font><br>|;
	}
	if ($m{tutorial_switch}) {
		print qq|<hr><font color="#FF0000">ﾁｭｰﾄﾘｱﾙﾓｰﾄﾞ</font><br>|;
	}
	if (-f "$userdir/$id/letter_flag.cgi") {
		#$lettersの処理を追えなかったので応急処置をした
		#open my $fh, "< $userdir/$id/letter_flag.cgi";
		#my $line = <$fh>;
		#my($letters) = split /<>/, $line;
		#close $fh;
		#print qq|<hr><font color="#FFCC66">手紙が $letters 件届いています</font><br>| if $letters;
		print qq|<hr><font color="#FFCC66">手紙が届いています</font><br>|;
		#unlink "$userdir/$id/letter_flag.cgi";
	}
	if (-f "$userdir/$id/depot_flag.cgi") {
		print qq|<hr><font color="#FFCC00">預かり所に荷物が届いています</font><br>|;
		#unlink "$userdir/$id/depot_flag.cgi";
	}
	if (-f "$userdir/$id/goods_flag.cgi") {
		print qq|<font color="#FFCC99">ﾏｲﾙｰﾑに荷物が届いています</font><br>|;
		unlink "$userdir/$id/goods_flag.cgi";
	}
	my $is_breeder_find = 0;
	for my $bi (0 .. 2) {
		if (-f "$userdir/$id/shopping_breeder_$bi.cgi") {
			if ((stat "$userdir/$id/shopping_breeder_$bi.cgi")[9] < $time) {
				$is_breeder_find = 1;
			}
		}
	}
	print qq|<font color="#FF66CC">育て屋の卵が孵化しています</font><br>| if $is_breeder_find;
}

#================================================
# 戦闘画面
#================================================
sub battle_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';

	my $m_hp_par = $m{max_hp} <= 0 ? 0 :
				$m{hp} > $m{max_hp} ? 100 : int($m{hp} / $m{max_hp} * 100);
	my $y_hp_par = $y{max_hp} <= 0 ? 0 :
				$y{hp} > $y{max_hp} ? 100 :int($y{hp} / $y{max_hp} * 100);
	my $m_mp_par = $m{max_mp} <= 0 ? 0 :
				$m{mp} > $m{max_mp} ? 100 : int($m{mp} / $m{max_mp} * 100);
	my $y_mp_par = $y{max_mp} <= 0 ? 0 :
				$y{mp} > $y{max_mp} ? 100 : int($y{mp} / $y{max_mp} * 100);
	my $fuka = !$m{egg} ? 0 :
				int($m{egg_c} / $eggs[$m{egg}][2] * 100) > 100 ? 100 : int($m{egg_c} / $eggs[$m{egg}][2] * 100);
	my $exp = $m{exp} > 100 ? 100 : $m{exp};

	$m_mes = qq|｢$m_mes｣| if $m_mes;
	$y_mes = qq|｢$y_mes｣| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00">★</font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00">★</font>' : '';
	my $m_tokkou2 = $is_m_tokkou2 ? '<font color="#FFFF00">★</font>' : '';
	my $y_tokkou2 = $is_y_tokkou2 ? '<font color="#FFFF00">★</font>' : '';

	print qq|$m_icon $m{name} $m_mes<br>|;
	print qq|<table border="0">|;
	print qq|<tr><td>$e2j{max_hp}：</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $m_hp_par%"></div></td><td> (<b>$m{hp}</b>/<b>$m{max_hp}</b>)<br></td></tr>|;
	print qq|<tr><td>$e2j{max_mp}：</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $m_mp_par%"></div></td><td> (<b>$m{mp}</b>/<b>$m{max_mp}</b>)<br></td></tr>|;
	print qq|<tr><td colspan="3">攻撃力 [ <b>$m_at</b> ] / 防御力 [ <b>$m_df</b> ] / 素早さ[ <b>$m_ag</b> ]<br></td></tr>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	print qq|<tr><td colspan="3">$m_tokkou武器：[$weas[$m{wea}][2]] $wname★$m{wea_lv} ($m{wea_c})<br></td></tr>| if $m{wea};
	print qq|<tr><td colspan="3">$m_tokkou2防具：[$guas[$m{gua}][2]] $guas[$m{gua}][1]<br></td></tr>| if $m{gua};
	print qq|<tr><td colspan="3">ﾍﾟｯﾄ：$pets[$m{pet}][1]★$m{pet_c}<br></td></tr>| if $pets[$m{pet}][2] eq 'battle';
	print qq|<tr><td>$e2j{exp}：</td><td><div class="bar4"><img src="$htmldir/space.gif" style="width: $exp%"></div></td><td> (<b>$m{exp}</b>/<b>100</b>)<br></td></tr>|;
	print qq|<tr><td>$eggs[$m{egg}][1]：</td><td><div class="bar5"><img src="$htmldir/space.gif" style="width: $fuka%"></div></td><td> (<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)<br></td></tr>|;
	print qq|<tr><td>疲労度：</td><td><div class="bar3" width="140px"><img src="$htmldir/space.gif" style="width: $m{act}%"></div></td><td> (<b>$m{act}</b>/<b>100</b>)<br></td></tr>|;
	print qq|</table>　 VS<br>|;

	print qq|$y_icon $y{name} $y_mes<br>|;
	print qq|<table border="0">|;
	print qq|<tr><td>$e2j{max_hp}：</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $y_hp_par%"></div></td><td> (<b>$y{hp}</b>/<b>$y{max_hp}</b>)<br></td></tr>|;
	print qq|<tr><td>$e2j{max_mp}：</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $y_mp_par%"></div></td><td> (<b>$y{mp}</b>/<b>$y{max_mp}</b>)<br></td></tr>|;
	print qq|<tr><td colspan="3">攻撃力 [ <b>$y_at</b> ] / 防御力 [ <b>$y_df</b> ] / 素早さ[ <b>$y_ag</b> ]<br></td></tr>|;
	my $ywname = $y{wea_name} ? $y{wea_name} : $weas[$y{wea}][1];
	print qq|<tr><td colspan="3">$y_tokkou武器：[$weas[$y{wea}][2]] $ywname<br></td></tr>| if $y{wea};
	print qq|<tr><td colspan="3">$y_tokkou2防具：[$guas[$y{gua}][2]] $guas[$y{gua}][1]<br></td></tr>| if $y{gua};
	print qq|</table>|;
}

#================================================
# 戦争画面
#================================================
sub war_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" $mobile_icon_size>| : '';
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" $mobile_icon_size>| : '';

	$m_mes = qq|｢$m_mes｣| if $m_mes;
	$y_mes = qq|｢$y_mes｣| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00"><b>★特攻★</b></font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00"><b>★特攻★</b></font>' : '';

	print qq|$m_icon<font color="$cs{color}[$m{country}]">$m{name}$m_mes</font><br>|;
	print qq|$m_tokkou$units[$m{unit}][1]/<b>$m{sol}</b>兵/士気[<b>$m{sol_lv}</b>%]/統率[<b>$m_lea</b>]<br>|;
	print qq|<hr>|;
	print qq|$y_icon<font color="$cs{color}[$y{country}]">$y{name}$y_mes</font><br>|;
	print qq|$y_tokkou$units[$y{unit}][1]/<b>$y{sol}</b>兵/士気[<b>$y{sol_lv}</b>%]/統率[<b>$y_lea</b>]<br>|;
}

#================================================
# 自国/同盟国の情報
#================================================
sub my_country_info {
	print qq|<hr>| if $m{country};
	print qq|<div class="c_infos">|;

	print qq|<div class="c_info">|;
	print qq|<span style="color: $cs{color}[$m{country}];">$c_m</span>|;
	print qq|<div class="c_info1p">|;
	print qq|<div class="c_info1c">$e2j{strong}:$cs{strong}[$m{country}]</div>|;
	print qq|<div class="c_info1c">城壁:$cs{barrier}[$m{country}]%</div>|;
	print qq|<div class="c_info1c">$e2j{tax}:$cs{tax}[$m{country}]%</div>|;
	print qq|<div class="c_info1c">$e2j{state}:$country_states[ $cs{state}[$m{country}] ]</div>|;
	print qq|</div>|;
	print qq|<div class="c_info2p">|;
	print qq|<div class="c_info2c">$e2j{food}:$cs{food}[$m{country}]</div>|;
	print qq|<div class="c_info2c">$e2j{money}:$cs{money}[$m{country}]</div>|;
	print qq|<div class="c_info2c">$e2j{soldier}:$cs{soldier}[$m{country}]</div>|;
	print qq|</div>|;
	print qq|</div>|;

	if ($union) {
#		print qq|<br>|;
		print qq|<div class="u_info">|;
		print qq|<span style="color: $cs{color}[$union];">$cs{name}[$union]</span>|;
		print qq|<div class="c_info1p">|;
		print qq|<div class="c_info1c">$e2j{strong}:$cs{strong}[$union]</div>|;
		print qq|<div class="c_info1c">城壁:$cs{barrier}[$union]%</div>|;
		print qq|<div class="c_info1c">$e2j{tax}:$cs{tax}[$union]%</div>|;
		print qq|<div class="c_info1c">$e2j{state}:$country_states[ $cs{state}[$union] ]</div>|;
		print qq|</div>|;
		print qq|<div class="c_info2p">|;
		print qq|<div class="c_info2c">$e2j{food}:$cs{food}[$union]</div>|;
		print qq|<div class="c_info2c">$e2j{money}:$cs{money}[$union]</div>|;
		print qq|<div class="c_info2c">$e2j{soldier}:$cs{soldier}[$union]</div>|;
		print qq|</div>|;
		print qq|</div>|;
	}
	print qq|</div>|;

=pod
	print qq|<hr>|;
	print qq|<dl>$c_m|;
	print qq|<dt>$e2j{strong}</dt><dd>$cs{strong}[$m{country}]</dd>|;
	print qq|<dt>$e2j{tax}</dt><dd>$cs{tax}[$m{country}]%</dd>|;
	print qq|<dt>$e2j{state}</dt><dd>$country_states[ $cs{state}[$m{country}] ]</dd>|;
	print qq|<dt>$e2j{food}</dt><dd>$cs{food}[$m{country}]</dd>|;
	print qq|<dt>$e2j{money}</dt><dd>$cs{money}[$m{country}]</dd>|;
	print qq|<dt>$e2j{soldier}</dt><dd>$cs{soldier}[$m{country}]</dd>|;
	print qq|</dl>|;

	print qq|<hr><table class="table1s">|;
	print qq|<tr><th colspan="3" style="color: #333; background-color: $cs{color}[$m{country}]; text-align: center;">$c_m</th></tr>\n|;
	print qq|<tr><th>$e2j{strong}</th><th>$e2j{tax}</th><th>$e2j{state}</th></tr>\n|;
	print qq|<tr><td align="right">$cs{strong}[$m{country}]</td><td align="right">$cs{tax}[$m{country}]%</td><td align="center">$country_states[ $cs{state}[$m{country}] ]</td></tr>\n|;
	print qq|<tr><th>$e2j{food}</th><th>$e2j{money}</th><th>$e2j{soldier}</th></tr>\n|;
	print qq|<tr><td align="right">$cs{food}[$m{country}]</td><td align="right">$cs{money}[$m{country}]</td><td align="right">$cs{soldier}[$m{country}]</td></tr>\n|;
	print qq|</table>|;

	if ($union) {
		print qq|<br>|;
		print qq|<table class="table1s">|;
		print qq|<tr><th colspan="3" style="color: #333; background-color: $cs{color}[$union]; text-align: center;">$cs{name}[$union]</th></tr>\n|;
		print qq|<tr><th>$e2j{strong}</th><th>$e2j{tax}</th><th>$e2j{state}</th></tr>\n|;
		print qq|<tr><td align="right">$cs{strong}[$union]</td><td align="right">$cs{tax}[$union]%</td><td align="center">$country_states[ $cs{state}[$union] ]</td></tr>\n|;
		print qq|<tr><th>$e2j{food}</th><th>$e2j{money}</th><th>$e2j{soldier}</th></tr>\n|;
		print qq|<tr><td align="right">$cs{food}[$union]</td><td align="right">$cs{money}[$union]</td><td align="right">$cs{soldier}[$union]</td></tr>\n|;
		print qq|</table>|;
	}
	print qq|<br>|;
=cut
=pod
	print qq|<hr><font color="$cs{color}[$m{country}]">$c_m</font><br>|;
	print qq|$e2j{strong}:$cs{strong}[$m{country}]<br>|;
	print qq|$e2j{tax}:$cs{tax}[$m{country}]%<br>|;
	print qq|$e2j{state}:$country_states[ $cs{state}[$m{country}] ]<br>|;
	print qq|$e2j{food}:$cs{food}[$m{country}]<br>|;
	print qq|$e2j{money}:$cs{money}[$m{country}]<br>|;
	print qq|$e2j{soldier}:$cs{soldier}[$m{country}]<br>|;

	if ($union) {
		print qq|<hr><font color="$cs{color}[$union]">$cs{name}[$union]</font><br>|;
		print qq|$e2j{strong}:$cs{strong}[$union]<br>|;
		print qq|$e2j{tax}:$cs{tax}[$union]%<br>|;
		print qq|$e2j{state}:$country_states[ $cs{state}[$union] ]<br>|;
		print qq|$e2j{food}:$cs{food}[$union]<br>|;
		print qq|$e2j{money}:$cs{money}[$union]<br>|;
		print qq|$e2j{soldier}:$cs{soldier}[$union]<br>|;
	}
=cut
}

#================================================
# 各国国力の情報
#================================================
sub countries_info {
	my($c1, $c2) = split /,/, $w{win_countries};
#	print qq|<table style="border: 2px solid #999; border-collapse: collapse; border-spacing: 0; empty-cells: show; width:320;">|;
	print qq|<table style="border: 2px solid #999; border-collapse: collapse; border-spacing: 0; empty-cells: show; width:100%;">|;
	print qq|<tr><th style="border: 2px solid #999; background: #336; white-space: nowrap;">$e2j{name}</th>|;
#	print qq|<tr><th style="border: 2px solid #999; background: #336;">$e2j{name}</th>|;
	print qq|<td align="center" style="color: #333; background-color: $cs{color}[$_]">$cs{name}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	unless ($w{world} eq '10') {
		print qq|<tr><th style="border: 2px solid #999; background: #336; white-space: nowrap;">$e2j{strong}</th>|;
#		print qq|<tr><th style="border: 2px solid #999; background: #336;">$e2j{strong}</th>|;
		for my $i (1 .. $w{country}) {
			my $status = $cs{strong}[$i];
			if ($cs{is_die}[$i] == 1) {
				$status = "滅 亡";
			}
			elsif ($cs{is_die}[$i] == 2) {
				$status = "鎖 国";
			}
			elsif ($cs{is_die}[$i] == 3) {
				$status = "崩 壊";
			}
			print qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">$status</td>|;
#			print qq|<td align="center" style="border: 1px solid #999; background: #333;">$status</td>|;
#			print $cs{is_die}[$i] ? qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">滅 亡</td>| : qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">$cs{strong}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}

	if ($m{name} eq 'nanamie' || $m{name} eq 'vavaa') {
		print qq|<tr><th style="border: 2px solid #999; background: #336;">城壁</th>|;
		print qq|<td align="center" style="border: 1px solid #999; background: #333;word-break:break-all;">$cs{barrier}[$_]%</td>| for (1 .. $w{country});
		print qq|</tr>\n|;
	}

	for my $k (qw/ceo war dom pro mil/) {
		print qq|<tr><th style="border: 2px solid #999; background: #336;">$e2j{$k}</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="center" style="border: 1px solid #999; background: #333;word-break:break-all;">$cs{$k}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}
	print qq|<tr><th style="border: 2px solid #999; background: #336; white-space: nowrap;">人数</th>|;
	print qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">$cs{member}[$_]/$cs{capacity}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	print qq|</table><br>|;

	my($c1, $c2) = split /,/, $w{win_countries};
	my $limit_hour = int( ($w{limit_time} - $time) / 3600 );
	my $limit_day  = $limit_hour <= 24 ? $limit_hour . '時間' : int($limit_hour / 24) . '日';
	my $reset_rest = int($w{reset_time} - $time);
	my $reset_time_mes = sprintf("<b>%d</b>時間<b>%02d</b>分<b>%02d</b>秒後", $reset_rest / 3600, $reset_rest % 3600 / 60, $reset_rest % 60);

	print $w{playing} >= $max_playing ? qq|<hr><font color="#FF0000">●</font>| : qq|<font color="#00FF00">●</font>|;
	print qq|ﾌﾟﾚｲ中 $w{playing}/$max_playing人<br>|;
	print qq|統一期限 残り$limit_day<br>|;
	if ($reset_rest > 0){
		print qq|終戦期間【残り$reset_time_mes】<br>|;
	}
	print qq|難易度 Lv.$w{game_lv}<br>統一$e2j{strong} $touitu_strong<br>| unless $w{world} eq '10';
	print $c2 ? qq|統一国 <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>同盟<br>|
		: $c1 ? qq|統一国 <font color="$cs{color}[$c1]">$cs{name}[$c1]</font><br>|
		:       ''
		;
	print qq|世界情勢 <a href="world_summaries.cgi?id=$id&pass=$pass&world=$w{world}" class="clickable_name">$world_states[$w{world}]</a><br>|;
	print qq|$world_name暦$w{year}年<br>|;
}

#================================================
# 友好度/状態(table版)
#================================================
sub promise_table_html {
	my @promise_js = (
		'<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">−</td>',
		'<td align="center" style="background-color: #090">同盟</td>',
		'<td align="center" style="background-color: #C00">交戦中</td>',
	);

#	print qq|<table style="border: 2px solid #999; border-collapse: collapse; border-spacing: 0; empty-cells: show; width:320;"><tr><td style="border: 1px solid #999; background: #333; white-space: nowrap;">状態/友好度</td>|;
	print qq|<table style="border: 2px solid #999; border-collapse: collapse; border-spacing: 0; empty-cells: show; width:100%;"><tr><td style="border: 1px solid #999; background: #333; white-space: nowrap;">状態/友好度</td>|;
	print qq|<td align="center" style="color: #333; background-color: $cs{color}[$_]">$cs{name}[$_]</td>| for 1 .. $w{country};
	print qq|</tr>|;

	for my $i (1 .. $w{country}) {
		print qq|<tr><td style="color: #333; background-color: $cs{color}[$i]">$cs{name}[$i]</td>|;
		for my $j (1 .. $w{country}) {
			if ($i eq $j) {
				print qq|<td align="center" style="border: 1px solid #999; background: #333; white-space: nowrap;">　</td>|;
			}
			elsif ($i > $j) {
				my $p_c_c = "p_${j}_${i}";
				print $promise_js[ $w{$p_c_c} ];
			}
			else {
				my $f_c_c = "f_${i}_${j}";
				print qq|<td align="right" style="border: 1px solid #999; background: #333; white-space: nowrap;">$w{$f_c_c}%</td>|;
			}
		}
		print qq|</tr>|;
	}
	print qq|</table>|;
}

sub countries_infos_table {
}

#================================================
# ｶｼﾞﾉの人数
#================================================
sub all_member_n {
	my $ret_str = '';
	my $ret_str2 = '';
	my $casino_n_file = "$logdir/casino_n.cgi";
	my $lastmodified = (stat $casino_n_file)[9];

	if (($lastmodified + 180) < $time) { # 3分毎に対人ｶｼﾞﾉの人数更新
		for my $i (0 .. $#files) {
			my $member_c  = 0;
			my %sames = ();
			my $tf_name = "$logdir/chat_casino$files[$i][2]_member.cgi";
			open my $fh, "< $tf_name" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
			my $head_line = <$fh>;
			while (my $line = <$fh>) {
				my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
				next if ($time - 180) > $mtime;
				next if $sames{$mname}++; # 同じ人なら次
				$member_c++;
			}
			close $fh;
			$ret_str2 .= substr($files[$i][0], 0, 2) . "/$member_c <>";
		}
		open my $fh, "> $casino_n_file" or &error('対人ｶｼﾞﾉの人数ﾌｧｲﾙが開けません');
		print $fh $ret_str2;
		close $fh;
	}
	else {
		open my $fh, "< $casino_n_file" or &error('対人ｶｼﾞﾉの人数ﾌｧｲﾙが開けません');
		$ret_str2 = <$fh>;
		close $fh;
	}
	my @casinos_n = split /<>/, $ret_str2;
	for my $i (0 .. $#casinos_n) {
		$ret_str .= $casinos_n[$i];
		$ret_str .= "<br>" if $i % 7 == 6;
	}

	return $ret_str;
}

sub show_world_news {
	open my $fh, "< $logdir/world_news.cgi" or &error("$logdir/world_news.cgiﾌｧｲﾙが読み込めません");
	my $line = <$fh>;
	close $fh;
	print "<hr>$line";
}

1; # 削除不可
