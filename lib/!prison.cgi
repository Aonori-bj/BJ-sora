sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
#=================================================
# ˜S– Created by Merino
#=================================================

#=================================================
# —˜—pğŒ
#=================================================
sub is_satisfy {
	if ($m{act} >= 100) {
		$mes .= "$m{name}‚Í­‚µ‹x‘§‚ğ‚Æ‚é‚±‚Æ‚É‚µ‚½<br>Ÿ‚És“®‚Å‚«‚é‚Ì‚Í $GWT•ªŒã‚Å‚·";
		$m{act} = 0;
		&wait;
		return 0;
	}
	return 1;
}

#=================================================
# ˜S–ÒÆ­°
#=================================================
sub tp_100 {
	if (-f "$userdir/$id/rescue_flag.cgi" # Ú½·­°Ì×¸Ş‚ª‚ ‚é‚©
		|| $time < $w{reset_time} # Ií’†
		|| !defined $cs{name}[$y{country}]) { # ‘íœ

			unlink "$userdir/$id/rescue_flag.cgi" or &error("$userdir/$id/rescue_flag.cgiíœ¸”s") if -f "$userdir/$id/rescue_flag.cgi";
			$mes .= "’‡ŠÔ‚É‹~o‚³‚ê‚Ü‚µ‚½<br>";
			
			&refresh;
			&n_menu;
			&escape;
	}
	else {
		$mes .= "$m{name}‚Í$c_y‚Ì˜S–‚É•Â‚¶‚ß‚ç‚ê‚Ü‚µ‚½<br>";
		$mes .= '‚Ç‚¤‚µ‚Ü‚·‚©?<br>';
		&menu('•‚¯‚ğ‘Ò‚Â','’E‘–‚ğ‚İ‚é','Q•Ô‚é');
		$m{tp} += 10;
	}
}

sub tp_110 {
	# ’Eo
	if ($cmd eq '1') {
		$mes .= "$m{name}‚Í’E‘–‚ª‚Å‚«‚»‚¤‚©FX‚Æ‚µ‚Ä‚İ‚½<br>";
		if ( int(rand(4)) == 0 ) { # ¬Œ÷
			$mes .= '‚È‚ñ‚Æ‚©˜S–‚©‚ç’Eo‚·‚é‚±‚Æ‚É¬Œ÷‚µ‚½!<br>';
			$m{tp} += 10;
		}
		elsif ( $m{cha} > rand(1000)+400 ) {
			$mes .= 'ŠÅç‚ğ—U˜f‚µ‚Ä˜S–‚©‚ç’Eo‚·‚é‚±‚Æ‚É¬Œ÷‚µ‚½!<br>';
			$m{tp} += 10;
		}
		else {
			$mes .= '‚Ç‚¤‚â‚ç–³—‚È‚æ‚¤‚¾c<br>';
			$m{act} += 10;
			$m{tp} = 100;
		}
		&n_menu;
	}
	# Q•Ô‚é
	elsif ($cmd eq '2') {
		$mes .= "Q•Ô‚é‚ÆŠK‹‰‚Æ‘ã•\\ÒÎß²İÄ‚ª‰º‚ª‚èAè‘±‚«‚É$GWT•ª‚©‚©‚è‚Ü‚·<br>";
		$mes .= "$c_m ‚ğ— Ø‚èA$c_y‚ÉQ•Ô‚è‚Ü‚·‚©?<br>";
		&menu('‚â‚ß‚é','Q•Ô‚é');
		$m{tp} = 200;
	}
	else {
		$m{tp} = 100;
		&tp_100;
	}
}

#=================================================
# ˜S–’Eo
#=================================================
sub tp_120 {
	$m{tp} += 10;
	$m{value} = int(rand(40))+40;
	$m{turn}  = int(rand(4)+4);
	$mes .= "˜S–‚©‚ç’Eo‚µ‚Ü‚µ‚½! <br>";
	$mes .= "$c_y’Eo‚Ü‚Åc‚èy$m{turn}À°İz“G•º‚Ì‹C”zy$m{value}%z<br>";
	$mes .= '‚Ç‚¿‚ç‚Éi‚İ‚Ü‚·‚©?<br>';
	&menu('¶','‰E');
	$m{value} += int( 10 - rand(21) ); # }10
	$m{value} = int(rand(30)) if $m{value} < 10;
}

#=================================================
# Ù°ÌßÒÆ­° •ß‚Ü‚é‚©’Eo‚·‚é‚Ü‚Å
#=================================================
sub loop_menu {
	$mes .= "$c_y’Eo‚Ü‚Åc‚èy$m{turn}À°İz“G•º‚Ì‹C”zy$m{value}%z<br>";
	$mes .= '‚Ç‚¿‚ç‚Éi‚İ‚Ü‚·‚©?<br>';
	int(rand(3)) == 0 ? &menu('¶','‰E') : &menu('¶','’¼i','‰E');
}
sub tp_130 {
	# Œ©‚Â‚©‚é
	if ( $m{value} > rand(110)+30 ) {
		$mes .= '“G•º‚ÉŒ©‚Â‚©‚Á‚Ä‚µ‚Ü‚Á‚½!!<br>';
		$m{tp} += 10;
		&n_menu;
	}
	# ’Eo¬Œ÷
	elsif (--$m{turn} <= 0) {
		&mes_and_world_news("–³–‚É$c_y‚©‚ç‚Ì©—Í’Eo‚É¬Œ÷‚µ‚Ü‚µ‚½!");
		&refresh;
		&n_menu;
		&escape;
	}
	else {
		&loop_menu;
	}
	$m{value} += int( 10 - rand(21) ); # }10
	$m{value} = int(rand(30)) if $m{value} < 10;
}
# Œ©‚Â‚©‚Á‚½:“¦‚°Ø‚ê‚é or •ß‚Ü‚é
sub tp_140 {
	if ( rand(6) < 1 ) {
		$mes .= '‚È‚ñ‚Æ‚©“G•º‚ğU‚èØ‚è‚Ü‚µ‚½<br>';
		$m{tp} -= 10;
		&loop_menu;
	}
	else {
		$mes .= '“G•º‚ÉˆÍ‚Ü‚ê˜S–‚Ö‚Æ˜A‚ê–ß‚³‚ê‚Ü‚µ‚½<br>';
		$m{tp} = 100;
		$m{act} += 20;
		&n_menu;
	}
}


#=================================================
# Q•Ô‚é
#=================================================
sub tp_200 {
	if ($cmd eq '1') {
		if ($cs{ceo}[$m{country}] eq $m{name}) {
			$mes .= "$e2j{ceo}‚ÍQ•Ô‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
			$m{tp} = 100;
			&n_menu;
		}
#		if ($m{name} eq $m{vote} || &is_daihyo) {
#			$mes .= "‘‚Ì‘ã•\\Ò‚â$e2j{ceo}‚É—§Œó•â‚µ‚Ä‚¢‚éê‡‚ÍQ•Ô‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
#			$m{tp} = 100;
#			&n_menu;
#		}
		elsif ($m{shogo} eq $shogos[1][0]) {
			$mes .= "$shogos[1][0]‚ÍQ•Ô‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($cs{member}[$y{country}] >= $cs{capacity}[$y{country}]) {
			$mes .= "$c_y‚Í’èˆõ‚ª‚¢‚Á‚Ï‚¢‚Å‚·<br>";
			$m{tp} = 100;
			&n_menu;
		}
		else {
			require './lib/move_player.cgi';
			&move_player($m{name}, $m{country}, $y{country});
			&escape;
			
			$m{shogo} = $shogos[1][0];

			$m{rank} -= $m{rank} > 10 ? 2 : 1;
			$m{rank} = 1 if $m{rank} < 1;
			$mes .= "ŠK‹‰‚ª$ranks[$m{rank}]‚É‚È‚è‚Ü‚µ‚½<br>";

			&mes_and_world_news("$cs{name}[$y{country}]‚ÉQ•Ô‚è‚Ü‚µ‚½", 1);
			$m{country} = $y{country};
			$m{vote} = '';
			
			# ‘ã•\Îß²İÄDown
			for my $key (qw/war dom mil pro/) {
				$m{$key.'_c'} = int($m{$key.'_c'} * 0.4);
			}

			&refresh;
			&wait;
			&n_menu;
		}
	}
	else {
		$mes .= '‚â‚ß‚Ü‚µ‚½<br>';
		$m{tp} = 100;
		&n_menu;
	}
}

#=================================================
# ˜S–Ì§²Ù‚©‚ç©•ª‚Ì–¼‘O‚ğœ‚­
#=================================================
sub escape {
	my @lines = ();
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country) = split /<>/, $line;
		push @lines, $line unless $name eq $m{name};
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # íœ•s‰Â
