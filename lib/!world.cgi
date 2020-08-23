sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ÌßÛ¸Ş×Ñ´×°ˆÙí‚Èˆ—‚Å‚·'); }
#================================================
# ¢ŠEî¨ Created by Merino
#================================================

#================================================
# ‘I‘ğ‰æ–Ê
#================================================
sub tp_100 {
	$mes .= "‚ ‚È‚½‚Í‚±‚Ì¢ŠE‚É‰½‚ğ‹‚ß‚Ü‚·‚©?<br>";
	&menu('ŠF‚ª–]‚Ş‚à‚Ì','Šó–]','â–]','•½˜a');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};

	if ($cmd eq '1') { # Šó–]
		&mes_and_world_news("<b>¢ŠE‚ÉŠó–]‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
		$w{world} = int(rand(8)+1);
	}
	elsif ($cmd eq '2') { # â–]
		&mes_and_world_news("<b>¢ŠE‚Éâ–]‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
		$w{world} = int(rand(9)+9);
	}
	elsif ($cmd eq '3') { # •½˜a
		&mes_and_world_news("<b>¢ŠE‚É•½˜a‚ğ–]‚İ‚Ü‚µ‚½</b>", 1);
		$w{world} = 0;
	}
	else {
		&mes_and_world_news('<b>¢ŠE‚É‚İ‚È‚ª–]‚Ş‚à‚Ì‚ğ–]‚İ‚Ü‚µ‚½</b>', 1);
		$w{world} = int(rand(@world_states-1));
	}

	# ‹­§ˆÃ•Šú
	if ($old_world eq $#world_states) {
		$w{world} = $#world_states;
		&write_world_news("<i>$m{name}‚ÌŠè‚¢‚Í‚©‚«Á‚³‚ê‚Ü‚µ‚½</i>");
	}
	# “¯‚¶‚Ì‚¶‚á‚Â‚Ü‚ç‚È‚¢‚Ì‚Å
	elsif ($w{world} eq $old_world) {
		$w{world} = int(rand(@world_states-1));
		++$w{world} if $w{world} eq $old_world;
		$w{world} = int(rand(10)) if $w{world} > $#world_states-1;
		&write_world_news("<i>¢ŠE‚Í $world_states[$old_world] ‚Æ‚È‚è‚Üc‚¹‚ñ $world_states[$w{world}]‚Æ‚È‚è‚Ü‚µ‚½</i>");
	}
	else {
		&write_world_news("<i>¢ŠE‚Í $world_states[$w{world}] ‚Æ‚È‚è‚Ü‚µ‚½</i>");
	}
	
	if ($w{world} eq '0') { # •½˜a
		$w{reset_time} += 3600 * 24 * 2;
	}
	elsif ($w{world} eq '7') { # Œ‹‘©
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			push @win_cs, [$i, $cs{win_c}[$i]];
		}
		@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;
		
		# Šï”‚Ìê‡‚Íˆê”Ô‘‚Íœ‚­
		shift @win_cs if @win_cs % 2 == 1;
		
		my $half_c = int(@win_cs*0.5-1);
		for my $i (0 .. $half_c) {
			my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
			$w{'p_'.$c_c} = 1;
		}
	}
	
	&refresh;
	&n_menu;
	&write_cs;
}



1; # íœ•s‰Â
