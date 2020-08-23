require "$datadir/skill.cgi";
$is_battle = 1; # ÊŞÄÙÌ×¸Ş1
#================================================
# í“¬ Created by Merino
#================================================

# •Ší‚É‚æ‚é—D—ò
my %tokkous = (
# '‹­‚¢‘®«' => qr/ã‚¢‘®«/,
	'Œ•' => qr/•€/,
	'•€' => qr/‘„/,
	'‘„' => qr/Œ•/,
	'‰Š' => qr/•—|–³/,
	'•—' => qr/—‹|–³/,
	'—‹' => qr/‰Š|–³/,
	'–³' => qr/Œ•|•€|‘„/,
);

#================================================
# g‚¤’l‚ğ Set
#================================================
my @m_skills = split /,/, $m{skills};
my @y_skills = split /,/, $y{skills};

# ‰æ–Ê•\¦‚â½·Ù‚Åg‚¤‚Ì‚Å¸ŞÛ°ÊŞÙ•Ï”
$m_at = $m{at};
$y_at = $y{at};
$m_df = $m{df};
$y_df = $y{df};
$m_ag = $m{ag};
$y_ag = $y{ag};

# g—p‚·‚é‚Ì‚Í AT or MAT, DF or MDF ‚Ì‚Ç‚¿‚ç‚©
if    ($weas[$m{wea}][2] =~ /–³|Œ•|•€|‘„/) { $m_at = $m{at}  + $weas[$m{wea}][3]; }
elsif ($weas[$m{wea}][2] =~ /‰Š|•—|—‹/)    { $m_at = $m{mat} + $weas[$m{wea}][3]; $y_df = $y{mdf}; }
if    ($weas[$y{wea}][2] =~ /–³|Œ•|•€|‘„/) { $y_at = $y{at}  + $weas[$y{wea}][3]; }
elsif ($weas[$y{wea}][2] =~ /‰Š|•—|—‹/)    { $y_at = $y{mat} + $weas[$y{wea}][3]; $m_df = $m{mdf}; }

$m_ag -= $weas[$m{wea}][5];
$m_ag = int(rand(5)) if $m_ag < 1;
$y_ag -= $weas[$y{wea}][5];
$y_ag = int(rand(5)) if $y_ag < 1;

$m_at = int($m_at * 0.5) if $m{wea} && $m{wea_c} <= 0;

if ($m{wea} && $y{wea}) {
	if (&is_tokkou($m{wea},$y{wea})){
		$m_at = int(1.5 *$m_at);
		$y_at = int(0.75*$y_at);
		$is_m_tokkou = 1;
	}
	elsif (&is_tokkou($y{wea},$m{wea})) {
		$y_at = int(1.5 *$y_at);
		$m_at = int(0.75*$m_at);
		$is_y_tokkou = 1;
	}
}

#================================================
# Ò²İ“®ì
#================================================
&run_battle;
&battle_menu if $m{hp} > 0 && $y{hp} > 0;


#================================================
# Àsˆ—
#================================================
sub run_battle {
	if ($cmd eq '') {
		$mes .= 'í“¬ºÏİÄŞ‚ğ‘I‘ğ‚µ‚Ä‚­‚¾‚³‚¢<br>';
	}
	elsif ($m{turn} >= 20) { # ‚È‚©‚È‚©Œˆ’…‚Â‚©‚È‚¢ê‡
		$mes .= 'í“¬ŒÀŠEÀ°İ‚ğ’´‚¦‚Ä‚µ‚Ü‚Á‚½c‚±‚êˆÈã‚Íí‚¦‚Ü‚¹‚ñ<br>';
		&lose;
	}
	elsif ( rand($m_ag * 3) >= rand($y_ag * 3) ) {
		my $v = &m_attack;
		if ($y{hp} <= 0 && $m{hp} > 0) {
			&win;
		}
		else {
			&y_attack;
			if    ($m{hp} <= 0) { &lose; }
			elsif ($y{hp} <= 0) { &win;  }
			elsif ($m{pet}) {
				&use_pet('battle', $v);
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	else {
		&y_attack;
		if ($m{hp} <= 0) {
			&lose;
		}
		else {
			my $v = &m_attack;
			if    ($m{hp} <= 0) { &lose;  }
			elsif ($y{hp} <= 0) { &win; }
			elsif ($m{pet}) {
				&use_pet('battle', $v);
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	
	$m{mp} = 0 if $m{mp} <= 0;
	$y{mp} = 0 if $y{mp} <= 0;
}


#=================================================
# ©•ª‚ÌUŒ‚
#=================================================
sub m_attack {
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	# •KE‹Z ³í‚ÈºÏİÄŞ‚© # ‘®«‚ª‘•”õ‚µ‚Ä‚¢‚é‚à‚Ì‚Æ“¯‚¶‚© # MP‚ª‚ ‚é‚©
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && $m{mp} >= $m_s->[3] ) {
		$m{mp} -= $m_s->[3];
		$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
		$mes .= "$m{name}‚Ì$m_s->[1]!!<br>";
		local $who = 'm';
		&{ $m_s->[4] }($m_at);
	}
	# ËßºØİ! K“¾‹Z5–¢– ‚©‚Â •ŠíÚÍŞÙ ‚©‚Â ‘Šè‚Ì‹­‚³•’ÊˆÈãª 
	elsif (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0) {
		local $who = 'm';
		&_pikorin;
	}
	else { # UŒ‚
		$mes .= "$m{name}‚ÌUŒ‚!!";
		my $v = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0
			? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
		
		if ($is_counter) {
			$mes .= "<br>UŒ‚‚ğ•Ô‚³‚ê $v ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½<br>";
			$m{hp} -= $v;
		}
		elsif ($is_stanch) {
			$mes .= "<br>½Àİ‚Å“®‚¯‚È‚¢!<br>";
		}
		else {
			$mes .= "<br>$v ‚ÌÀŞÒ°¼Ş‚ğ‚ ‚½‚¦‚Ü‚µ‚½<br>";
			if ($m{wea_c} > 0) {
				--$m{wea_c};
				$mes .= "$weas[$m{wea}][1]‚Í‰ó‚ê‚Ä‚µ‚Ü‚Á‚½<br>" if $m{wea_c} == 0;
			}
			$y{hp} -= $v;
		}
	}
}
#=================================================
# ‘Šè‚ÌUŒ‚
#=================================================
sub y_attack {
	my $y_s = $skills[ $y_skills[ int(rand(6))-1 ] ];
	
	# •KE‹Z ³í‚ÈºÏİÄŞ‚© # ‘®«‚ª‘•”õ‚µ‚Ä‚¢‚é‚à‚Ì‚Æ“¯‚¶‚© # MP‚ª‚ ‚é‚©
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && $y{mp} >= $y_s->[3] ) {
		$y{mp} -= $y_s->[3];
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}‚Ì$y_s->[1]!!<br>";

		local $who = 'y';
		&{ $y_s->[4] }($y_at);
	}
	else {
		$mes .= "$y{name}‚ÌUŒ‚!!";
		my $v = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0
			? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);

		if ($is_counter) {
			$mes .= "<br>UŒ‚‚ğ•Ô‚µ $v ‚ÌÀŞÒ°¼Ş‚ğ‚ ‚½‚¦‚Ü‚µ‚½<br>";
			$y{hp} -= $v;
		}
		elsif ($is_stanch) {
			$mes .= "<br>½Àİ‚Å“®‚¯‚È‚¢!<br>";
		}
		else {
			$mes .= "<br>$v ‚ÌÀŞÒ°¼Ş‚ğ‚¤‚¯‚Ü‚µ‚½<br>";
			$m{hp} -= $v;
		}
	}
}

#=================================================
# ‰ïSA’ÊíUŒ‚
#=================================================
sub _attack_kaishin {
	my $at = shift;
	$mes .= '<b>‰ïS‚ÌˆêŒ‚!!</b>';
	return int($at * (rand(0.4)+0.8) );
}
sub _attack_normal {
	my($at, $df) = @_;
	my $v = int( ($at * 0.5 - $df * 0.3) * (rand(0.3)+ 0.9) );
	   $v = int(rand(5)+1) if $v < 5;
	return $v;
}
#=================================================
# V‹ZK“¾(‚·‚Å‚ÉŠo‚¦‚Ä‚¢‚é‹Z‚Å‚à”­“®)
#=================================================
sub _pikorin {
	# Šo‚¦‚ç‚ê‚é‘®«‚Ì‚à‚Ì‚ğ‘S‚Ä@lines‚É“ü‚ê‚é
	my @lines = ();
	for my $i (1 .. $#skills) {
		push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
	}
	
	if (@lines) {
		my $no = $lines[int(rand(@lines))];
		$m_mes = "‘M‚¢‚½!! $skills[$no][1]!";
		# Šo‚¦‚Ä‚¢‚È‚¢‹Z‚È‚ç’Ç‰Á
		my $is_learning = 1;
		for my $m_skill (@m_skills) {
			if ($m_skill eq $no) {
				$is_learning = 0;
				last;
			}
		}
		$m{skills} .= "$no," if $is_learning;
		$mes .= qq|<font color="#CCFF00">™‘M‚«!!$m{name}‚Ì$skills[ $no ][1]!!</font><br>|;
		$skills[ $no ][4]->($m_at);
	}
	else { # —áŠOˆ—FŠo‚¦‚ç‚ê‚é‚à‚Ì‚ª‚È‚¢
		$m_mes = '‘M‚ß‚«‚»‚¤‚Å‘M‚¯‚È‚¢c';
	}
}


#=================================================
# í“¬—pƒƒjƒ…[
#=================================================
sub battle_menu {
	$menu_cmd  = qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
	$menu_cmd .= qq|<option value="0">UŒ‚</option>|;
	for my $i (1 .. $#m_skills+1) {
		next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
		next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
		$menu_cmd .= qq|<option value="$i"> $skills[ $m_skills[$i-1] ][1]</option>|;
	}
	$menu_cmd .= qq|</select><br><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= qq|<input type="submit" value="Œˆ ’è" class="button1"></form>|;
}


#=================================================
# Ÿ—˜
#=================================================
sub win {
	$m{hp} = 0 if $m{hp} < 0;
	$y{hp} = 0;
	$m{turn} = 0;
	$mes .= "$y{name}‚ğ“|‚µ‚Ü‚µ‚½<br>";

	$m_mes = $m{mes_win}  unless $m_mes;
	$y_mes = $y{mes_lose} unless $y_mes;
}

#=================================================
# ”s–k
#=================================================
sub lose {
	$m{hp} = 0;
	$y{hp} = 0 if $y{hp} < 0;
	$m{turn} = 0;
	$mes .= "$m{name}‚Í‚â‚ç‚ê‚Ä‚µ‚Ü‚Á‚½c<br>";

	$m_mes = $m{mes_lose} unless $m_mes;
	$y_mes = $y{mes_win}  unless $y_mes;
}


#=================================================
# •Ší‚É‚æ‚è“ÁU‚ª‚Â‚­‚©‚Ç‚¤‚©
#=================================================
sub is_tokkou {
	my($wea1, $wea2) = @_;
	return defined $tokkous{ $weas[$wea1][2] } && $weas[$wea2][2] =~ /$tokkous{ $weas[$wea1][2] }/ ? 1 : 0;
}



1; # íœ•s‰Â
