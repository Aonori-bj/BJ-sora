#================================================
# “]EŠ Created by Merino ###
#================================================

# “]E‚É•K—v‚È‹àŠz
my $need_money = $m{sedai} > 10 ? 20000 : $m{sedai} * 2000;


#=================================================
sub begin {
	$mes .= '‚±‚±‚Í“]EŠ‚¶‚áB‚¨å‚ÌE‹Æ‚ğ•Ï‚¦‚é‚±‚Æ‚ª‚Å‚«‚é‚¼<br>';
	$mes .= "‚½‚¾‚µA“]E‚·‚é‚É‚Í $need_money G•K—v‚¶‚á‚¼<br>";
	$mes .= 'E‹Æ‚ğ•Ï‚¦‚é‚Ì‚©?<br>';

	my @menus = ('‚â‚ß‚é');
	for my $i (0 .. $#jobs) {
		push @menus, $jobs[$i][11]->() ? $jobs[$i][1] : '';
	}
	&menu(@menus);
}

sub tp_1 {
	--$cmd;
	if ($m{job} eq $cmd) {
		$mes .= "$jobs[$cmd][1]‚É‚È‚è‚½‚¢‚Æ\\‚·‚©c<br>‚¦?‚Å‚àA‚·‚Å‚É‚»‚ÌE‹Æ‚É‚È‚Á‚Ä‚¨‚é‚Å‚Í‚È‚¢‚©?<br>";
	}
	elsif ($cmd >= 0 && &{ $jobs[$cmd][11] }) {
		if ($m{money} >= $need_money) {
			$m{money} -= $need_money;
			$m{job} = $cmd;
			$mes .= "$jobs[$cmd][1]‚Æ‚È‚Á‚ÄV‚½‚È“¹‚ği‚Ş‚ª‚æ‚¢<br>$m{name}‚Í$jobs[$cmd][1]‚É“]E‚µ‚Ü‚µ‚½<br>";
		}
		else {
			$mes .= '‚¨‹à‚ª‘«‚è‚ñ‚¼‚¢<br>‚¨‹à‚ğ‚½‚ß‚Ä‚Ü‚½—ˆ‚È‚³‚ê<br>';
		}
	}
	else {
		$mes .= '‚»‚ÌE‹Æ‚É“]E‚·‚éğŒ‚ª–‚½‚³‚ê‚Ä‚¢‚È‚¢‚æ‚¤‚¶‚á<br>';
	}

	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}




1; # íœ•s‰Â
