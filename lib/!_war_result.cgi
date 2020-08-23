#=================================================
# í‘ˆŒ‹‰Ê Created by Merino
#=================================================
# war.cgi‚É‚ ‚Á‚Ä‚à‚¢‚¢‚¯‚Ç‚²‚¿‚á‚²‚¿‚á‚É‚È‚è‚»‚¤‚È‚Ì‚Å•ª—£

# ‹~ol”
my $max_rescue = 1;

#=================================================
# ˆø‚«•ª‚¯
#=================================================
sub war_draw {
	&c_up('draw_c');
	my $v = int( rand(11) + 10 );
	$m{rank_exp} -= int( (rand(16)+15) * $m{value} );
	$m{exp} += $v;

	$mes .= "$m{name}‚É‘Î‚·‚é•]‰¿‚ª‰º‚ª‚è‚Ü‚µ‚½<br>";
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	
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
# •‰‚¯
#=================================================
sub war_lose {
	&c_up('lose_c');
	my $v = int( rand(11) + 15 );
	&use_pet('war_result', 0);
	$m{rank_exp} -= int( (rand(21)+20) * $m{value} );
	$m{exp} += $v;

	$mes .= "•”‘à‘S–Å‚Æ‚¢‚¤•s–¼—_‚È”s–k‚Ìˆ×A$m{name}‚É‘Î‚·‚é•]‰¿‚ª’˜‚µ‚­‰º‚ª‚è‚Ü‚µ‚½<br>";
	$mes .= "$v‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	
	$cs{soldier}[$y{country}] += $y{sol} if $y{sol} > 0;
	&down_friendship;

	# ˜A‘±‚Å“¯‚¶‘‚¾‚Æ‚Šm—¦‚ÅÀ²°Î
	&refresh;
	if ( ( $w{world} eq '8' && $cs{strong}[$y{country}] <= 3000 ) || ( $w{world} eq '12' && $m{renzoku_c} > rand(4) ) || $m{renzoku_c} > rand(7) + 2 ) {
		&write_world_news("$c_m‚Ì$m{name}‚ª$c_y‚Ì˜S–‚É—H•Â‚³‚ê‚Ü‚µ‚½");
		&add_prisoner;
	}

	&write_cs;
	&n_menu;
}

#=================================================
# ‘Ş‹p
#=================================================
sub war_escape {
	$mes .= "$m{name}‚É‘Î‚·‚é•]‰¿‚ª‰º‚ª‚è‚Ü‚µ‚½<br>";
	$m{rank_exp} -= int( (rand(6)+5) * $m{value} );

	$cs{soldier}[$m{country}] += $m{sol};
	$cs{soldier}[$y{country}] += $y{sol};

	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# Ÿ‚¿
#=================================================
sub war_win {
	my $is_single = shift;

	# ’D‘—ÍÍŞ°½:ŠK‹‰‚ª‚‚¢‚Ù‚ÇÌß×½B‰ºãAŠv–½‚Ì‚ÍŠK‹‰‚ª’á‚¢‚Ù‚ÇÌß×½
	my $v = $w{world} eq '2' || $w{world} eq '3' ? (@ranks - $m{rank}) * 10 + 10 : $m{rank} * 8 + 10;

	# ’èˆõ‚ª­‚È‚¢•ªÌß×½‘½‚¢•ªÏ²Å½
	$v += ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 10;

	# ‘î¨‚É‚æ‚è’D‘—Í‘‰Á
	if ($w{world} eq '5' || $w{world} eq '6') { # –\ŒNA¬“×
		$v *= 2.5;
	}
	elsif ($w{world} eq '3') { # Šv–½:ã‘—L—˜
		my $sum = 0;
		for my $i (1 .. $w{country}) {
			$sum += $cs{win_c}[$i];
		}
		$v *= 2.5 if $cs{win_c}[$m{country}] <= $sum / $w{country};
	}
	elsif ($w{world} eq '2') { # ‰ºã:¢‘ã’á‚¢l—L—˜
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
	
	# Œğí’†‚È‚ç2”{
	my $p_c_c = 'p_' . &union($m{country}, $y{country});
	$v *= 2 if $w{$p_c_c} eq '2';
	
	$v = $v * $m{value} * (rand(0.4)+0.8);
	$v = &use_pet('war_result', $v);
	
	# ’D‘—ÍãŒÀ
	if ($v !~ /^(\d)\1+$/) { # ¿ŞÛ–Ú(³ÛÎŞÛ½g—p‚È‚Ç)
		if ($m{value} < 1) { # ­”¸‰s
			$v = $v > 200 ? int(rand(100)+100) : int($v);
		}
		else { # ’ÊíE’·Šú
			if ($time + 2 * 24 * 3600 > $w{limit_time}) { # “ˆêŠúŒÀc‚è‚P“ú
				$v = $v > 1500 ? int(rand(500)+1000) : int($v);
			}
			else {
				$v = $v > 600  ? int(rand(200)+400) : int($v);
			}
			
			# “ˆêŠúŒÀ‚ª‹ß‚Ã‚¢‚Ä‚«‚½‚çÌß×½
			$v += $time + 4 * 24 * 3600 > $w{limit_time} ? 40
			    : $time + 8 * 24 * 3600 > $w{limit_time} ? 20
			    :                                          5
			    ;
		}
	}
	
	# –Å–S‘‚Ìê‡”±‘¥
	if ($cs{is_die}[$y{country}]) {
		$v = int($v * 0.5);
		&_penalty
	}
	else {
		$cs{soldier}[$m{country}] += $m{sol};
	}
	# ‘—Íƒf[ƒ^}
	$cs{strong}[$m{country}] += $v;
	$cs{strong}[$y{country}] -= $v;
	$cs{strong}[$y{country}] = 0  if $cs{strong}[$y{country}] < 0;
	
	$mes .= "$c_y‚©‚ç$v‚Ì$e2j{strong}‚ğ’D‚¢‚Ü‚µ‚½<br>";
	
	if ($is_single) {
		&write_world_news(qq|$c_m‚Ì$m{name}‚ª$c_y‚ÉNUA$y{name}‚Æˆê‹R“¢‚¿‚Ì––‚±‚ê‚ğ‰º‚µ <font color="#FF00FF"><b>$v</b> ‚Ì$e2j{strong}‚ğ’D‚¤–‚É¬Œ÷</font>‚µ‚½‚æ‚¤‚Å‚·|);
	}
	else {
		$m{value} < 1
			? &write_world_news(qq|‰½Ò‚©‚ª$c_y‚ÉNUA$y{name}‚Ì•”‘à‚ğŒ‚”j‚µ <font color="#FF00FF"><b>$v</b> ‚Ì$e2j{strong}‚ğ’D‚¤‚±‚Æ‚É¬Œ÷</font>‚µ‚½‚æ‚¤‚Å‚·|)
			: &write_world_news(qq|$c_m‚Ì$m{name}‚ª$c_y‚ÉNUA$y{name}‚Ì•”‘à‚ğŒ‚”j‚µ <font color="#FF00FF"><b>$v</b> ‚Ì$e2j{strong}‚ğ’D‚¤‚±‚Æ‚É¬Œ÷</font>‚µ‚½‚æ‚¤‚Å‚·|)
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

	$mes .= "$m{name}‚É‘Î‚·‚é•]‰¿‚ª‘å‚«‚­ã‚ª‚è‚Ü‚µ‚½<br>";
	$mes .= "$vv‚Ì$e2j{exp}‚ğè‚É“ü‚ê‚Ü‚µ‚½<br>";
	
	# Ú½·­°
	&_rescue if -s "$logdir/$y{country}/prisoner.cgi";

	&refresh;

	# ˆÃ•
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
	# Ià
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
	# “ˆê
	elsif ($cs{strong}[$m{country}] >= $touitu_strong) {
		&_touitu;
	}
	# –Å–S
	elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
		&_metubou;
	}
	# •œ‹»
	elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 && !($w{world} eq '10' || $w{world} eq '14') ) {
		&_hukkou;
	}
	# “S•Ç
	elsif ($w{world} eq '8' && $cs{strong}[$y{country}] <= 3000 && rand(3) < 1) {
		my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 100  );
		&write_world_news("<b>Ø³Ş§²±»İ‚Ì‘å—’I$cs{name}[$m{country}]‚Í$cs{name}[$y{country}]‚Ì$e2j{$kkk}‚ğ $vvv ’D‚¢‚Ü‚µ‚½</b>");
	}

	&daihyo_c_up('war_c'); # ‘ã•\n—û“x
	&write_cs;

	&n_menu;
}

#=================================================
# ˜S–‚É’‡ŠÔ‚ª‚¢‚é‚È‚ç‹~o
#=================================================
sub _rescue {
	my $is_rescue = 0;
	my @lines = ();
	my $count = 0;
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country) = split /<>/, $line;
		if ($count < $max_rescue && ($country eq $m{country} || $union eq $country) ) {
			$mes .= "$c_y‚É•ß‚ç‚¦‚ç‚ê‚Ä‚¢‚½$name‚ğ‹~o‚µ‚Ü‚µ‚½<br>";
			$is_rescue = 1;
			&write_world_news("$c_m‚Ì$m{name}‚ª$c_y‚É•ß‚ç‚¦‚ç‚ê‚Ä‚¢‚½$name‚Ì‹~o‚É¬Œ÷‚µ‚Ü‚µ‚½");
			
			# Ú½·­°Ì×¸Şì¬
			my $y_id = unpack 'H*', $name;
			if (-d "$userdir/$y_id") {
				open my $fh2, "> $userdir/$y_id/rescue_flag.cgi" or &error("$userdir/$y_id/rescue_flag.cgiÌ§²Ù‚ªì‚ê‚Ü‚¹‚ñ");
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
# “ˆê
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
		if ($m{country} eq $w{country} || $union eq $w{country}) { # NPC‘‘¤‚ÌŸ—˜
			&mes_and_world_news("<em>ˆ«–‚’B‚Ì—¦æÒ‚Æ‚µ‚Ä$world_name‘å—¤‚ğx”z‚·‚é‚±‚Æ‚É¬Œ÷‚µ‚Ü‚µ‚½</em>",1);
			&write_legend('touitu', "[‚«ˆÅ‚æ‚è–ÚŠo‚ß‚½$cs{name}[$w{country}]‚Ì–ÒÒ’B‚ª$m{name}‚ğ•M“ª‚Æ‚µ$world_name‘å—¤‚ğx”z‚·‚é");
			$is_npc_win = 1;
		}
		else {
			&mes_and_world_news("<em>–‚ŠE‚ğÄ‚Ñ••ˆó‚µA$world_name‘å—¤‚É‚Ğ‚Æ‚Æ‚«‚ÌˆÀ‚ç‚¬‚ª‚¨‚Æ‚¸‚ê‚Ü‚µ‚½</em>",1);
			&write_legend('touitu', "$c_m‚Ì$m{name}‚Æ‚»‚Ì’‡ŠÔ’B‚ª–‚ŠE‚ğÄ‚Ñ••ˆó‚µA$world_name‘å—¤‚É‚Ğ‚Æ‚Æ‚«‚ÌˆÀ‚ç‚¬‚ª‚¨‚Æ‚¸‚ê‚é");
		}
	}
	else {
		if ($union) {
			$mes .= "<em>$world_name‘å—¤‚ğ“ˆê‚µ‚Ü‚µ‚½</em>";
			&write_world_news("<em>$c_m$cs{name}[$union]“¯–¿‚Ì$m{name}‚ª$world_name‘å—¤‚ğ“ˆê‚µ‚Ü‚µ‚½</em>",1);
			&write_legend('touitu', "$c_m$cs{name}[$union]“¯–¿‚Ì$m{name}‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é")
		}
		else {
			&mes_and_world_news("<em>$world_name‘å—¤‚ğ“ˆê‚µ‚Ü‚µ‚½</em>",1);
			&write_legend('touitu', "$c_m‚Ì$m{name}‚ª$world_name‘å—¤‚ğ“ˆê‚·‚é");
		}
	}

	require "./lib/reset.cgi";
	&reset;

	$m{lib} = 'world';
	$m{tp}  = 100;
	
}

#=================================================
# •œ‹»
#=================================================
sub _hukkou {
	&c_up('huk_c');
	$cs{is_die}[$m{country}] = 0;
	&mes_and_world_news("<b>$c_m‚ğ•œ‹»‚³‚¹‚é‚±‚Æ‚É¬Œ÷‚µ‚Ü‚µ‚½</b>", 1);
	
	--$w{game_lv};
#	--$w{game_lv} if $time + 7 * 24 * 3600 > $w{limit_time};
}

#=================================================
# –Å–S
#=================================================
sub _metubou {
	&c_up('met_c');
	$cs{strong}[$y{country}] = 0;
	$cs{is_die}[$y{country}] = 1;
	&mes_and_world_news("<b>$c_y‚ğ–Å‚Ú‚µ‚Ü‚µ‚½</b>", 1);

	# •¨‘Down
	for my $k (qw/food money soldier/) {
		$cs{$k}[$y{country}] = int( $cs{$k}[$y{country}] * ( rand(0.3)+0.3 ) );
	}
	
	# ‘ó‘Ô•Ï‰»
	for my $i (1 .. $w{country}) {
		$cs{state}[$i] = int(rand(@country_states));
	}
}
#=================================================
# –Å–S‘‚©‚ç‘—Í‚ğ’Dæ‚µ‚½‚Ì”±‘¥
#=================================================
sub _penalty {
	# ĞŠQ
	if ( ($w{world} eq '13' && rand(3) < 1) || rand(12) < 1 ) {
		&disaster;
	}
}

#=================================================
# —FD“xDown
#=================================================
sub down_friendship {
	my $c_c = &union($m{country}, $y{country});
	$w{'f_'.$c_c} -= 1;
	if ($w{'p_'.$c_c} ne '2' && $w{'f_'.$c_c} < 10) {
		$w{'p_'.$c_c} = 2;
		&write_world_news("<b>$c_m‚Ì$m{name}‚ÌiŒR‚É‚æ‚è$c_y‚ÆŒğíó‘Ô‚É‚È‚è‚Ü‚µ‚½</b>");
	}
	$w{'f_'.$c_c} = int(rand(20)) if $w{'f_'.$c_c} < 1;
}


1; # íœ•s‰Â
