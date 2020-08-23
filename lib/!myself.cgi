require "$datadir/skill.cgi";
require "$datadir/pet.cgi";
#=================================================
# ½Ã°À½‰æ–Ê Created by Merino
#=================================================

# ÒÆ­° ’Ç‰Á/•ÏX/íœ/•À‚×‘Ö‚¦‰Â”\
my @menus = (
	['‚â‚ß‚é',		'main'],
	['ºÚ¸¼®İÙ°Ñ',	'myself_collection'],
	['½·ÙŒp³',		'myself_skill'],
	['Ì†‚ğ•ÏX',	'myself_shogo'],
	['¾ØÌ‚ğ•ÏX',	'myself_mes'],
	['©ŒÈĞ‰î',	'myself_profile'],
	['¤l‚Ì‚¨“X',	'myself_shop'],
	['Ï²Ëß¸Á¬',		'myself_picture'],
	['Ï²ÌŞ¯¸',		'myself_book'],
	['¤l‚Ì‹âs',	'myself_bank'],
	['ŒÂlİ’è',	'myself_config'],
);


#================================================
sub begin {
	$layout = 2;
	$is_mobile ? &my_status_mobile : &my_status_pc;
	&menu(map{ $_->[0] }@menus);
}
sub tp_1 {
	# Íß¯Äg—p
	if ($in{mode} eq 'use_pet' && $m{pet} && $pets[$m{pet}][2] eq 'myself') {
		&refresh;
		&n_menu;

		# ÏÓÉÉÀÈ‚Ìê‡
		if ($m{pet} >= 128 && $m{pet} <= 130) {
			$mes .= "$pets[$m{pet}][1]‚ÍA$m{name}‚Ì‚±‚Æ‚ğ‚¶‚Á‚ÆŒ©‚Ä‚¢‚éc<br>";
			$m{lib} = 'add_monster';
			$m{tp}  = 100;
		}
		else {
			&{ $pets[$m{pet}][3] };
			$mes .= "–ğ–Ú‚ğI‚¦‚½ $pets[$m{pet}][1] ‚ÍŒõ‚Ì”Ş•û‚ÖÁ‚¦‚Ä‚¢‚Á‚½c<br>";
			$m{pet} = 0;
		}
	}
	else {
		&b_menu(@menus);
	}
}


#================================================
# Œg‘Ñ—p½Ã°À½•\¦
#================================================
sub my_status_mobile {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;

	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= "[$skills[$m_skill][2]]$skills[$m_skill][1] Á”ï$e2j{mp} $skills[$m_skill][3]<br>";
	}

	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_ag  = '';
	if ($m{wea}) {
		$mes .= qq|<hr>y•Šíî•ñz<br><ul>|;
		$mes .= qq|<li>–¼‘O:$weas[$m{wea}][1]|;
		$mes .= qq|<li>‘®«:$weas[$m{wea}][2]|;
		$mes .= qq|<li>‹­‚³:$weas[$m{wea}][3]|;
		$mes .= qq|<li>‘Ï‹v:$weas[$m{wea}][4]|;
		$mes .= qq|<li>d‚³:$weas[$m{wea}][5]</ul><hr>|;
		if    ($weas[$m{wea}][2] =~ /–³|Œ•|•€|‘„/) { $sub_at  = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /•—|‰Š|—‹/)    { $sub_mat = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }
	}

	if ($m{pet}) {
		$mes .= qq|yÍß¯Äî•ñz<br><ul>|;
		$mes .= qq|<li>–¼‘O:$pets[$m{pet}][1]|;
		$mes .= qq|<li>Œø‰Ê:$pet_effects[$m{pet}]</ul>|;
		if ($pets[$m{pet}][2] eq 'myself') {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="Íß¯Ä‚ğg—p‚·‚é" class="button1"></form>|;
		}
		$mes .= qq|<hr>|;
	}

	my $m_st = &m_st;
	$mes .=<<"EOM";
		<b>$m{sedai}</b>¢‘ã–Ú<br>
		$sexes[ $m{sex} ] [$jobs[$m{job}][1]]<br>
		ŒMÍ <b>$m{medal}</b>ŒÂ<br>
		¶¼ŞÉº²İ <b>$m{coin}</b>–‡<br>
		•ó¸¼Şy$m{lot}z<br>
		<hr>
		y½Ã°À½z‹­‚³:$m_st<br>
		$e2j{max_hp} [<b>$m{max_hp}</b>]/$e2j{max_mp} [<b>$m{max_mp}</b>]/<br>
		$e2j{at} [<b>$m{at}</b>$sub_at]/$e2j{df} [<b>$m{df}</b>]/<br>
		$e2j{mat} [<b>$m{mat}</b>$sub_mat]/$e2j{mdf} [<b>$m{mdf}</b>]/<br>
		$e2j{ag} [<b>$m{ag}</b>$sub_ag]/$e2j{cha} [<b>$m{cha}</b>]/<br>
		$e2j{lea} [<b>$m{lea}</b>]<br>
		<hr>
		yŠo‚¦‚Ä‚¢‚é‹Zz<br>
		 $skill_info
		<hr>
		yn—û“xz<br>
		”_‹Æ <b>$m{nou_c}</b>/¤‹Æ <b>$m{sho_c}</b>/’¥•º <b>$m{hei_c}</b>/ŠOŒğ <b>$m{gai_c}</b>/‘Ò•š <b>$m{mat_c}</b>/<br>
		‹­’D <b>$m{gou_c}</b>/’³•ñ <b>$m{cho_c}</b>/ô”] <b>$m{sen_c}</b>/‹UŒv <b>$m{gik_c}</b>/’ã@ <b>$m{tei_c}</b>/<br>
		Cs <b>$m{shu_c}</b>/“¢”° <b>$m{tou_c}</b>/“¬‹Z <b>$m{col_c}</b>/¶¼ŞÉ <b>$m{cas_c}</b>/<br>
		“ˆê <b>$m{hero_c}</b>/•œ‹» <b>$m{huk_c}</b>/–Å–S <b>$m{met_c}</b>/<br>
		<hr>
		y‘ã•\\ÒÎß²İÄz<br>
		í‘ˆ <b>$m{war_c}</b>/“à­ <b>$m{dom_c}</b>/ŒR– <b>$m{mil_c}</b>/ŠOŒğ <b>$m{pro_c}</b>/
		<hr>
		yí—ğz<br>
		<b>$war_c</b>í <b>$m{win_c}</b>Ÿ <b>$m{lose_c}</b>•‰ <b>$m{draw_c}</b>ˆø<br>
		Ÿ—¦ <b>$win_par</b>%
EOM
}

#================================================
# PC—p½Ã°À½•\¦
#================================================
sub my_status_pc {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;

	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= qq|<tr><td align="center">$skills[$m_skill][2]</td><td>$skills[$m_skill][1]</td><td align="right">$skills[$m_skill][3]<br></td></tr>|;
	}

	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_ah  = '';
	if ($m{wea}) {
		$mes .= qq|<hr>y•Šíî•ñz<br>|;
		$mes .= qq|<table class="table1" cellpadding="3"><tr>|;
		$mes .= qq|<th>–¼‘O</th><td>$weas[$m{wea}][1]</td>|;
		$mes .= qq|<th>‘®«</th><td>$weas[$m{wea}][2]</td>|;
		$mes .= qq|<th>‹­‚³</th><td>$weas[$m{wea}][3]</td>|;
		$mes .= qq|<th>‘Ï‹v</th><td>$weas[$m{wea}][4]</td>|;
		$mes .= qq|<th>d‚³</th><td>$weas[$m{wea}][5]</td>|;
		$mes .= qq|</tr></table><hr size="1">|;
		if    ($weas[$m{wea}][2] =~ /–³|Œ•|•€|‘„/) { $sub_at  = "£$weas[$m{wea}][3]"; $sub_ag = "¥$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /•—|‰Š|—‹/)    { $sub_mat = "£$weas[$m{wea}][3]"; $sub_ag = "¥$weas[$m{wea}][5]"; }
	}

	if ($m{pet}) {
		$mes .= qq|yÍß¯Äî•ñz<br>|;
		$mes .= qq|<table class="table1" cellpadding="3">|;
		$mes .= qq|<tr><th>–¼‘O</th><td>$pets[$m{pet}][1]</td>|;
		$mes .= qq|<th>Œø‰Ê</th><td>$pet_effects[$m{pet}]</td></tr>|;
		$mes .= qq|</table>|;
		if ($pets[$m{pet}][2] eq 'myself') {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="Íß¯Ä‚ğg—p‚·‚é" class="button1"></form>|;
		}
		$mes .= qq|<hr size="1">|;
	}

	my $m_st = &m_st;
	$mes .= <<"EOM";
		y½Ã°À½z‹­‚³F$m_st<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>$e2j{max_hp}</th><td align="right">$m{max_hp}</td>
			<th>$e2j{at}</th><td align="right">$m{at}$sub_at</td>
			<th>$e2j{df}</th><td align="right">$m{df}</td>
		</tr><tr>
			<th>$e2j{max_mp}</th><td align="right">$m{max_mp}</td>
			<th>$e2j{mat}</th><td align="right">$m{mat}$sub_mat</td>
			<th>$e2j{mdf}</th><td align="right">$m{mdf}</td>
		</tr><tr>
			<th>$e2j{lea}</th><td align="right">$m{lea}</td>
			<th>$e2j{ag}</th><td align="right">$m{ag}$sub_ag</td>
			<th>$e2j{cha}</th><td align="right">$m{cha}</td>
		</tr>
		</table>
		<hr size="1">
		yŠo‚¦‚Ä‚¢‚é‹Zz<br>
		<table class="table1" cellpadding="3">
		<tr><th>‘®«</th><th>‹Z–¼</th><th>Á”ï$e2j{mp}</th></tr>
		$skill_info
		</table>

		<hr size="1">
		yn—û“xz<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>”_‹Æ</th><td align="right">$m{nou_c}</td>
			<th>¤‹Æ</th><td align="right">$m{sho_c}</td>
			<th>’¥•º</th><td align="right">$m{hei_c}</td>
			<th>ŠOŒğ</th><td align="right">$m{gai_c}</td>
			<th>‘Ò•š</th><td align="right">$m{mat_c}</td>
		</tr>
		<tr>
			<th>‹­’D</th><td align="right">$m{gou_c}</td>
			<th>’³•ñ</th><td align="right">$m{cho_c}</td>
			<th>ô”]</th><td align="right">$m{sen_c}</td>
			<th>‹UŒv</th><td align="right">$m{gik_c}</td>
			<th>’ã@</th><td align="right">$m{tei_c}</td>
		</tr>
		<tr>
			<th>Cs</th><td align="right">$m{shu_c}</td>
			<th>“¢”°</th><td align="right">$m{tou_c}</td>
			<th>“¬‹Z</th><td align="right">$m{col_c}</td>
			<th>¶¼ŞÉ</th><td align="right">$m{cas_c}</td>
			<th>–‚•¨</th><td align="right">$m{mon_c}</td></tr>
		<tr>
			<th>“ˆê</th><td align="right">$m{hero_c}</td>
			<th>•œ‹»</th><td align="right">$m{huk_c}</td>
			<th>–Å–S</th><td align="right">$m{met_c}</td>
			<th>@</th><td align="right">@</td>
			<th>@</th><td align="right">@</td>
		</tr>
		</table>

		<hr size="1">
		y‘ã•\\ÒÎß²İÄz<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>í‘ˆ</th><td align="right">$m{war_c}</td>
			<th>“à­</th><td align="right">$m{dom_c}</td>
			<th>ŒR–</th><td align="right">$m{mil_c}</td>
			<th>ŠOŒğ</th><td align="right">$m{pro_c}</td>
		</tr>
		</table>

		<hr size="1">
		yí—ğz<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>í‰ñ</th><td align="right">$war_c</td>
			<th>Ÿ‚¿</th><td align="right">$m{win_c}</td>
			<th>•‰‚¯</th><td align="right">$m{lose_c}</td>
			<th>ˆø•ª</th><td align="right">$m{draw_c}</td>
			<th>Ÿ—¦</th><td align="right">$win_par %</td>
		</tr>
		</table>
EOM
}


1; # íœ•s‰Â
