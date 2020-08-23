$mes .= qq|ŒMÍ $m{medal}ŒÂ<br>| if $is_mobile;
#=================================================
# •”‘à•ÏX Created by Merino
#=================================================

# ŒMÍ1ŒÂ‚Ì‹àŠz
my $exchange_money = 3000;

# ˆø‚«Š·‚¦•i
my @prizes = (
# í—Ş 1=•Ší,2=—‘,3=Íß¯Ä 
#	[0]í—Ş,[1]No,[2]ŒMÍ
	[0,	0,	0,	],
	[1,	12,	5,	],
	[1,	17,	5,	],
	[1,	27,	5,	],
	[2,	21,	15,	],
	[2,	33,	20,	],
	[2,	48,	25,	],
	[2,	3,	30,	],
	[2,	45,	80,	],
	[2,	37,	90,	],
	[2,	46,	99,	],
);


# “Á•ÊğŒ‚Å¸×½Áªİ¼Ş‚Å‚«‚é‚à‚Ì
my %plus_needs = (
# •”‘àNo => ğŒ•¶,					ifğŒ									# ğŒ¸Ø±Œã‚Ìˆ—
	7  => ['ÀŞ°¸Î°½‚ğ¶æÑ',			sub{ $pets[$m{pet}][2] eq 'speed_up' },	sub{ $mes.="$pets[$m{pet}][1]‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; $m{pet} = 0; } ],
	8  => ['ÄŞ×ºŞİŒn‚ÌÍß¯Ä‚ğ¶æÑ',	sub{ $pets[$m{pet}][1] =~ /ÄŞ×ºŞİ/ },	sub{ $mes.="$pets[$m{pet}][1]‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; $m{pet} = 0; } ],
	11 => ['E‹Æ‚ª”EÒ',			sub{ $jobs[$m{job}][1] eq '”EÒ' },		sub{} ],
	12 => ["$eggs[23][1]‚ğ¶æÑ",	sub{ $m{egg} eq '23'},					sub{ $mes.="$eggs[$m{egg}][1]‚ğ¶æÑ‚É‚µ‚Ü‚µ‚½<br>"; $m{egg} = 0; $m{egg_c} = 0; } ],
	15 => ['E‹Æ‚ª–‚•¨g‚¢',		sub{ $jobs[$m{job}][1] eq '–‚•¨g‚¢' },	sub{} ],
);


#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '‘¼‚É‰½‚©‚ ‚è‚Ü‚·‚©?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "‚±‚±‚Å‚Í$m{name}‚Ì‚Á‚Ä‚¢‚éŒMÍ‚É‰‚¶‚Ä•”‘à‚ğ¸×½Áªİ¼Ş‚µ‚½‚è‚Å‚«‚Ü‚·<br>";
		$mes .= '‚Ç‚¤‚µ‚Ü‚·‚©?<br>';
	}
	&menu('‚â‚ß‚é','‚¨‹à‚ª—~‚µ‚¢','±²ÃÑ‚ª—~‚µ‚¢','•”‘à‚ğ•Ï‚¦‚½‚¢');
}
sub tp_1 {
	return if &is_ng_cmd(1..3);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# ŒMÍ¨‚¨‹à
#=================================================
sub tp_100 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}‚ÌŠ‚µ‚Ä‚¢‚éŒMÍ‚Í$m{medal}ŒÂ‚Å‚·‚Ë<br>";
	$mes .= "ŒMÍ1ŒÂ‚É‚Â‚« $exchange_money G‚ÉŠ·‚¦‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>";
	$mes .= "‰½ŒÂ‚ÌŒMÍ‚ğŒ£ã‚µ‚Ü‚·‚©?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="medal" value="0" class="text_box1" style="text-align:right">ŒÂ|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="Œ£ã‚·‚é" class="button1"></p></form>|;
}
sub tp_110 {
	if ($in{medal} && $in{medal} !~ /[^0-9]/) {
		if ($in{medal} > $m{medal}) {
			$mes .= "$in{medal}ŒÂ‚àŒMÍ‚ğ‚Á‚Ä‚¢‚Ü‚¹‚ñ<br>";
		}
		else {
			my $v = $in{medal} * $exchange_money;
			$m{money} += $v;
			$m{medal} -= $in{medal};
			
			$mes .= "ŒMÍ$in{medal}ŒÂ‚ğŒ£ã‚µ‚Ä $v G‚ğ‚à‚ç‚¢‚Ü‚µ‚½<br>";
		}
	}
	&begin;
}

#=================================================
# ŒMÍ¨±²ÃÑ
#=================================================
sub tp_200 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}‚ÌŠ‚µ‚Ä‚¢‚éŒMÍ‚Í$m{medal}ŒÂ‚Å‚·‚Ë<br>";
	$mes .= "‚Ç‚ê‚ÆŒğŠ·‚µ‚Ü‚·‚©?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1" cellpadding="3"><tr><th>–¼‘O</th><th>ŒMÍ<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked>‚â‚ß‚é<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i">|;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[—‘]$eggs[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[ƒy]$pets[ $prizes[$i][1] ][1]</td>|
			  ;
		$mes .= qq|<td align="right">$prizes[$i][2]ŒÂ<br></td></tr>|;
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="ŒğŠ·‚·‚é" class="button1"></p></form>|;
}
sub tp_210 {
	if ($cmd && defined $prizes[$cmd]) {
		if ($m{medal} >= $prizes[$cmd][2]) {
			$m{medal} -= $prizes[$cmd][2];
			
			$mes .= "ŒMÍ$prizes[$cmd][2]ŒÂ‚ğŒ£ã‚µ‚Ä";

			if ($prizes[$cmd][0] eq '1') {
				$mes .= "$weas[ $prizes[$cmd][1] ][1]‚ÉŒğŠ·‚µ‚Ü‚µ‚½<br>";
				&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], $weas[ $prizes[$cmd][1] ][4]);
			}
			elsif ($prizes[$cmd][0] eq '2') {
				$mes .= "$eggs[ $prizes[$cmd][1] ][1]‚ÉŒğŠ·‚µ‚Ü‚µ‚½<br>";
				&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1]);
			}
			elsif ($prizes[$cmd][0] eq '3') {
				$mes .= "$pets[ $prizes[$cmd][1] ][1]‚ÉŒğŠ·‚µ‚Ü‚µ‚½<br>";
				&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1]);
			}
		}
		else {
			$mes .= 'ŒMÍ‚ª‘«‚è‚Ü‚¹‚ñ<br>';
		}
	}
	&begin;
}

#=================================================
# ŒMÍ¨•”‘à{‚¨‹à
#=================================================
sub tp_300 {
	$m{tp} += 10;
	$mes .= "$m{name}‚ÌŠ‚µ‚Ä‚¢‚éŒMÍ‚Í$m{medal}ŒÂ‚Å‚·‚Ë<br>";
	$mes .= "¸×½Áªİ¼Ş‚Å—]‚Á‚½ŒMÍ‚Í‚¨‹à‚ÉŠ·‹à‚µ‚Ü‚·<br>";
	$mes .= "‚Ç‚Ì•”‘à‚É¸×½Áªİ¼Ş‚µ‚Ü‚·‚©?<hr>";
	$mes .= "¡‚Ì•”‘à‚©‚ç‚Å¸×½Áªİ¼Ş‚Å‚«‚é‚Ì‚ÍˆÈ‰º‚Å‚·<br>";
	
	$mes .= "$units[0][1] ğŒF‚È‚µ<br>";
	my @menus = ('‚â‚ß‚é', $units[0][1]);
	for my $i (1 .. $#units) {
		if ($i eq $units[$m{unit}][2]) {
			$mes .= "$units[$i][1] ğŒF‚È‚µ<br>";
			push @menus, $units[$i][1];
		}
		elsif ($m{unit} eq $units[$i][2]) {
			$mes .= "$units[$i][1] ğŒF$units[ $units[$i][2] ][1]/ŒMÍ$units[$i][3]ŒÂ/";
			$mes .= $plus_needs{$i}[0] if defined $plus_needs{$i};
			$mes .= "<br>";
			
			push @menus, $units[$i][1];
		}
		else {
			push @menus, '';
		}
	}
	
	&menu(@menus);
}
sub tp_310 {
	if ($cmd) {
		--$cmd;
		
		if ($cmd) {
			# ¸×½ÀŞ³İ
			unless ($cmd eq $units[$m{unit}][2]) {
				# “ÁêğŒ
				if (defined $plus_needs{$cmd}) {
					if (&{ $plus_needs{$cmd}[1] } && $units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
						&{ $plus_needs{$cmd}[2] };
						$m{medal} -= $units[$cmd][3];
					}
					else {
						$mes .= "¸×½Áªİ¼Ş‚Å‚«‚éğŒ‚ğ–‚½‚µ‚Ä‚¢‚Ü‚¹‚ñ<br>";
						&begin;
						return;
					}
				}
				elsif ($units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
					$m{medal} -= $units[$cmd][3];
				}
				else {
					$mes .= "¸×½Áªİ¼Ş‚Å‚«‚éğŒ‚ğ–‚½‚µ‚Ä‚¢‚Ü‚¹‚ñ<br>";
					&begin;
					return;
				}
			}
		}
		
		$m{unit} = $cmd;
		$mes .= "$units[$m{unit}][1]‚É¸×½Áªİ¼Ş‚µ‚Ü‚µ‚½<br>";

		if ($m{medal} > 0) {
			my $v = $m{medal} * $exchange_money;
			$m{money} += $v;
			$mes .= "c‚è‚ÌŒMÍ$m{medal}ŒÂ‚ğŒ£ã‚µ‚Ä $v G‚ğ‚à‚ç‚¢‚Ü‚µ‚½<br>";
			$m{medal} = 0;
		}
	}
	&begin;
}


1; # íœ•s‰Â
