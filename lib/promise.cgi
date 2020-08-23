my $u = &union($m{country}, $y{country});
#================================================
# ŠOŒğ Created by Merino
#================================================

#=================================================
# —˜—pğŒ
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '‘‚É‘®‚µ‚Ä‚È‚¢‚Æs‚¤‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ”æ˜J‚µ‚Ä‚¢‚éê‡‚Ís‚¦‚È‚¢
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "‘¼‚É‰½‚©s‚¢‚Ü‚·‚©?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "‘¼‘‚ÆŠOŒğ‚ğ‚µ‚Ü‚·($GWT•ª)<br>‰½‚ğs‚¢‚Ü‚·‚©?<br>";
	}

	my @menus = ('‚â‚ß‚é','—FDğ–ñ','’âí‹¦’è');

	if (&is_daihyo) {
		push @menus, 'éí•z','‹¦í“¯–¿','“¯–¿”jŠü';
		push @menus, 'H—¿—A‘—','‘‹à’ñ‹Ÿ','•ºm”hŒ­' if $union;
	}
	&menu(@menus);
}

sub tp_1 {
	return if &is_ng_cmd(1..8);

	if    ($cmd eq '1') { $mes .= '—FDğ–ñ‚ğŒ‹‚Ñ—FD“x‚ğã‚°‚Ü‚·<br>'; }
	elsif ($cmd eq '2') {
		if (($w{world} eq '8' || ($w{world} eq '19' && $w{world_sub} eq '8'))) {
#		if ($w{world} eq '9') {
			$mes .= "¢ŠEî¨‚ª$world_states[$w{world}]‚È‚Ì‚ÅA’âíğ–ñ‚ğŒ‹‚Ô‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>";
			$m{tp} = 2;
			&begin;
			return;
		}
		$mes .= '’âíğ–ñ‚ğŒ‹‚ÑŒğíó‘Ô‚ğ‰ğœ‚µ‚Ü‚·<br>';
	}
	elsif ( &is_daihyo ) {
		if    ($cmd eq '3') { $mes .= 'éí•z‚ğ‚µAŒğíó‘Ô‚É‚µ‚Ü‚·<br>'; }
		elsif ($cmd eq '4') { $mes .= '‹¦í“¯–¿‚ğŒ‹‚Ñ‚Ü‚·<br>'; }
		elsif ($cmd eq '5') { $mes .= '“¯–¿‚ğ”jŠü‚µ‚Ü‚·<br>'; }

		elsif ($cmd eq '6') { $mes .= "“¯–¿‘$cs{name}[$union]‚É©‘‚Ì$e2j{food}‚ğ—A‘—‚µ‚Ü‚·<br>"; }
		elsif ($cmd eq '7') { $mes .= "“¯–¿‘$cs{name}[$union]‚É©‘‚Ì$e2j{money}‚ğŠñ•t‚µ‚Ü‚·<br>"; }
		elsif ($cmd eq '8') { $mes .= "“¯–¿‘$cs{name}[$union]‚É©‘‚Ì•ºm‚ğ”hŒ­‚µ‚Ü‚·<br>"; }
	}
	else {
		$mes .= "‚»‚ÌºÏİÄŞ‚ÍA‘‚Ì‘ã•\\Ò‚µ‚©‚Å‚«‚Ü‚¹‚ñ<br>";
		$m{tp} = 2;
		&begin;
		return;
	}

	$m{tp} = $cmd * 100;

	if ($cmd >= 6) {
		$mes .= qq|‚Ç‚ê‚­‚ç‚¢‘—‚è‚Ü‚·‚©?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="text" name="value" value="0" class="text_box1" style="text-align: right">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="‘—‚é"></p></form>|;
		&n_menu;
	}
	else {
		$mes .= '‚Ç‚Ì‘‚ÉŒü‚©‚¢‚Ü‚·‚©?<br>';
		&menu('‚â‚ß‚é', @countries);
	}
}


#=================================================
# ŠOŒğ¾¯Ä
#=================================================
sub tp_100 { &exe1("—FDğ–ñ‚ğŒğÂ‚µ‚É") }
sub tp_200 { &exe1("’âíğ–ñ‚ğŒğÂ‚µ‚É") }
sub tp_300 { &exe1("éí•z‚ğ‚µ‚É") }
sub tp_400 { &exe1("“¯–¿‚ğŒğÂ‚µ‚É") }
sub tp_500 { &exe1("“¯–¿‚ğ”jŠü‚µ‚É") }
sub exe1 {
	return if &is_ng_cmd(1..$w{country});

	if ($m{tp} >= 300 && !&is_daihyo) {
		$mes .= "‚»‚ÌºÏİÄŞ‚ÍA‘‚Ì‘ã•\\Ò‚µ‚©‚Å‚«‚Ü‚¹‚ñ<br>";
		&begin;
	}
	elsif ($m{country} eq $cmd) {
		$mes .= '©‘‚Í‘I‚×‚Ü‚¹‚ñ<br>';
		&begin;
	}
	else {
		$m{tp} += 10;
		$y{country} = $cmd;
		$mes .= "$_[0]$cs{name}[$y{country}]‚ÉŒü‚©‚¢‚Ü‚µ‚½<br>";
		$mes .= "Œ‹‰Ê‚Í$GWT•ªŒã‚Å‚·<br>";
		&wait;
	}
}


#=================================================
# —FDğ–ñ
#=================================================
sub tp_110 {
	if ( rand($w{"f_$u"}) > 5 || rand(4) > 1  ) {
		&mes_and_world_news("$c_y‚Æ—FDğ–ñ‚ğŒ‹‚Ñ‚Ü‚µ‚½");
		$w{"f_$u"} += int( rand(5)+7 );
		$w{"f_$u"} = 100 if $w{"f_$u"} > 100;
		&success;
	}
	else {
		$mes .= "$c_y‚Æ‚Ì—FDğ–ñ‚É¸”s‚µ‚Ü‚µ‚½<br>";
		&failed;
	}
}
#=================================================
# ’âí
#=================================================
sub tp_210 {
#	if ($w{world} eq '9') {
	if (($w{world} eq '8' || ($w{world} eq '19' && $w{world_sub} eq '8'))) {
		$mes .= "¢ŠEî¨‚ª$world_states[$w{world}]‚È‚Ì‚ÅA’âí‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
		&failed;
	}
	elsif ($w{"p_$u"} eq '2') {
		&mes_and_world_news("<b>$c_y‚Æ’âíğ–ñ‚ğŒ‹‚Ñ‚Ü‚µ‚½</b>");
		$w{"f_$u"} = int( rand(20)+40 );
		$w{"p_$u"} = 0;

		&success;
	}
	else {
		$mes .= "$c_y‚Æ‚Ì’âíğ–ñ‚É¸”s‚µ‚Ü‚µ‚½<br>";
		&failed;
	}
}
#=================================================
# éí•z
#=================================================
sub tp_310 {
	if ($w{"p_$u"} eq '1') {
		$mes .= "‚Ü‚¸A$c_y‚Æ‚Ì“¯–¿‚ğ”jŠü‚µ‚Ä‚­‚¾‚³‚¢<br>";
		&failed;
	}
	elsif ($cs{is_die}[$m{country}]) {
		$mes .= "–Å–S‚µ‚Ä‚¢‚é‘‚ÍAéí•z‚ğ‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
		&failed;
	}
	elsif ($cs{is_die}[$y{country}]) {
		$mes .= "–Å–S‚µ‚Ä‚¢‚é‘‚Ééí•z‚ğ‚·‚é‚±‚Æ‚Í‚Å‚«‚Ü‚¹‚ñ<br>";
		&failed;
	}
	else {
		&mes_and_world_news("<b>$c_y‚Ééí•z‚ğ‚µ‚Ü‚µ‚½</b>");
		$w{"p_$u"} = 2;
		$w{"f_$u"} = int( rand(20) );
		&success;
	}
}
#=================================================
# “¯–¿
#=================================================
sub tp_410 {
	if ( $w{world} eq '8'|| $w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '8' || $w{world_sub} eq '13')) || $w{world} == $#world_states-5 || $w{world} == $#world_states-2 || $w{world} == $#world_states-3 ) {
	#if ( $w{world} eq '9' || $w{world} eq '14' || $w{world} == $#world_states-5 || $w{world} == $#world_states-2 || $w{world} == $#world_states-3 ) {
		$mes .= "¢ŠEî¨‚ª$world_states[$w{world}]‚È‚Ì‚ÅA“¯–¿‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
		&failed;
	}
	elsif ( !$union && $w{"p_$u"} eq '0' && $w{"f_$u"} >= 80 && !&is_other_union($y{country}) ) {
		&mes_and_world_news("<b>$c_y‚Æ‹¦í“¯–¿‚ğŒ‹‚Ñ‚Ü‚µ‚½</b>");
		$w{"p_$u"} = 1;
		&success;
	}
	else {
		$mes .= "$c_y‚Æ‚Ì“¯–¿‚É¸”s‚µ‚Ü‚µ‚½<br>";
		&failed;
	}
}
#=================================================
# “¯–¿”jŠü
#=================================================
sub tp_510 {
	if (($w{world} eq '6' || ($w{world} eq '19' && $w{world_sub} eq '6'))) {
#	if ($w{world} eq '7') {
		$mes .= "¢ŠEî¨‚ª$world_states[$w{world}]‚È‚Ì‚ÅA“¯–¿‚ğ”jŠü‚·‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
		&failed;
	}
	elsif ( $union && $w{"p_$u"} eq '1') {
		&mes_and_world_news("<b>$c_y‚Æ‚Ì“¯–¿‚ğ”jŠü‚µ‚Ü‚µ‚½</b>");
		$w{"p_$u"} = 0;
		&success;
	}
	else {
		$mes .= "$c_y‚Æ‚Í“¯–¿‚ğ‘g‚ñ‚Å‚¢‚Ü‚¹‚ñ<br>";
		&failed;
	}
}


#=================================================
# “¯–¿‘‚É•¨‘‚ğ’ñ‹Ÿ
#=================================================
sub tp_600 { &exe2('food',    'H—¿') }
sub tp_700 { &exe2('money',   '‘‹à') }
sub tp_800 { &exe2('soldier', '•ºm') }
sub exe2 {
	if ($in{value} > 0 && $in{value} !~ /[^0-9]/) {
		if (!$union) {
			$mes .= '“¯–¿‚µ‚Ä‚Ü‚¹‚ñ<br>';
			&begin;
		}
		elsif ($cs{$_[0]}[$m{country}] <= $in{value}) {
			$mes .= "$c_m‚Ì$_[1]‚ª‚È‚­‚È‚Á‚Ä‚µ‚Ü‚¢‚Ü‚·<br>";
			&begin;
		}
		elsif ($in{value} < 10000) {
			$mes .= "•¨‘‚Ìx‰‡‚ÍÅ’á‚Å‚à 10000 ˆÈã‚É‚·‚é•K—v‚ª‚ ‚è‚Ü‚·<br>";
			&begin;
		}
		else {
			$cs{$_[0]}[$m{country}] -= $in{value};
			&write_cs;

			$m{value} = $in{value};

			$m{tp} += 10;
			$y{country} = $union;

			&mes_and_send_news("“¯–¿‘‚Ì$cs{name}[$union]‚É$_[1]‚ğ $m{value} ‘—‚è‚Ü‚µ‚½");
			$mes .= "$GWT•ª‚É“’…‚·‚é—\\’è‚Å‚·<br>";
			&wait;
		}
	}
	else {
		$mes .= "‚â‚ß‚Ü‚µ‚½<br>";
		&begin;
	}
}
sub tp_610 { # ‘•º—Æ
	if ($union) {
		$cs{food}[$union] += $m{value};
		&exe3('H—¿');
	}
	else {
		$mes .= "‘¼‚Ì‘‚Æ“¯–¿‚ğ‘g‚ñ‚Å‚¢‚Ü‚¹‚ñ<br>";
		&failed;
	}
}
sub tp_710 { # ‘‰Æ—\Z
	if ($union) {
		$cs{money}[$union] += $m{value};
		&exe3('‘‹à');
	}
	else {
		$mes .= "‘¼‚Ì‘‚Æ“¯–¿‚ğ‘g‚ñ‚Å‚¢‚Ü‚¹‚ñ<br>";
		&failed;
	}
}
sub tp_810 { # •ºm
	if ($union) {
		$cs{soldier}[$union] += $m{value};
		&exe3('•ºm');
	}
	else {
		$mes .= "‘¼‚Ì‘‚Æ“¯–¿‚ğ‘g‚ñ‚Å‚¢‚Ü‚¹‚ñ<br>";
		&failed;
	}
}
sub exe3 {
	my $name = shift;

	$w{"f_$u"} += int( rand(10)+20 );
	$w{"f_$u"} = 100 if $w{"f_$u"} > 100;
	&write_cs;
	&write_send_news("$c_m‚Ì$m{name}‚Ì—A‘—•”‘à‚ª“¯–¿‘‚Ì$cs{name}[$union]‚É“’…‚µA$m{value} ‚Ì$name‚ª–³–‚É“Í‚¯‚ç‚ê‚Ü‚µ‚½");
	$mes .= "—A‘—•”‘à‚ª“¯–¿‘‚Ì$cs{name}[$union]‚É“’…‚µA$m{value} ‚Ì$name‚ª–³–‚É“Í‚¯‚ç‚ê‚Ü‚µ‚½<br>";
	&success;
}

#=================================================
# ¬Œ÷
#=================================================
sub success {
	$m{act} += 1;
	&c_up('gai_c');

	my $v = int(rand(11)+10);
	$v = &use_pet('promise', $v);

	$m{exp} += $v;
	$m{egg_c} += int(rand(6)+5) if $m{egg};
	$m{rank_exp} += int(rand(6)+4);

	$mes .= "$m{name}‚É‘Î‚·‚é•]‰¿‚ªã‚ª‚è‚Ü‚µ‚½<br>";
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";

	&daihyo_c_up('pro_c'); # ‘ã•\n—û“x

	&refresh;
	&n_menu;
	&write_cs;
}
#=================================================
# ¸”s
#=================================================
sub failed {
	$m{act} += 1;

	my $v = int(rand(11)+5);
	$m{exp} += $v;
	$m{egg_c} += int(rand(6)+5) if $m{egg};
	$m{rank_exp} -= int(rand(3)+2);

	$mes .= "ŒğÂ‚É¸”s‚µ‚½‚½‚ßA$m{name}‚É‘Î‚·‚é•]‰¿‚ª‰º‚ª‚è‚Ü‚µ‚½<br>";
	$mes .= "$v ‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";

	&refresh;
	&n_menu;
}


#=================================================
# ‘¼‘‚Æ“¯–¿‚ğ‚­‚ñ‚Å‚¢‚é‚©
#=================================================
sub is_other_union {
	my $country = shift;

	for my $i (1 .. $w{country}) {
		next if $country eq $i;
		my $c_c = &union($country, $i);
		return 1 if $w{ "p_$c_c" } eq '1';
	}
	return 0;
}




1; # íœ•s‰Â
