#================================================
# ƒƒCƒ“‰æ–Ê Created by Merino
#================================================

# ‚¨“X‚Ì”„ã‹à‚ÌÅ‹à(0(Å‹à‚È‚µ)`0.99‚Ü‚Å)
my $shop_sale_tax = 0.2;

# ÒÆ­° ’Ç‰Á/•ÏX/íœ/•À‚×‘Ö‚¦‰Â”\
my @menus = (
	['XV',		''],
	['¼®¯Ëßİ¸ŞÓ°Ù',	'shopping'],
	['—a‚©‚èŠ',	'depot'],
	['‘ŒÉ',	'depot_country'],
	['Ï²Ù°Ñ',		'myself'],
	['Cs',		'training'],
	['“¢”°',		'hunting'],
	['‘î•ñ',		'country'],
	['“à­',		'domestic'],
	['ŠOŒğ',		'promise'],
	['ŒR–',		'military'],
	['í‘ˆ',		'war_form'],
);

if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
	push @menus, ['›z‰»', 'incubation'];
}
if (&on_summer) {
	push @menus, ['‰ÄÕ‚è', 'summer_festival'];
}

#================================================
sub begin {
	&menu( map { $_->[0] } @menus );
	&main_system;
}
sub tp_1 { $cmd ? &b_menu(@menus) : &begin; }


#================================================
# Ò²İ¼½ÃÑ
#================================================
sub main_system {
	# Lv up
	if ($m{exp} >= 100) {
		if ($m{egg}) {
			$m{egg_c} += int(rand(6)+10);
			$m{egg_c} += int(rand(16)+20) if $jobs[$m{job}][1] eq '—‘m';
			push @menus, ['›z‰»', 'incubation'] if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]);
		}
		&lv_up;
	}
	# ÀÏºŞ¬’·
	elsif (!$m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
		$m{egg_c} = 0;
		$mes .= "‚Á‚Ä‚¢‚½$eggs[$m{egg}][1]‚ªŒõ‚¾‚µ‚Ü‚µ‚½!<br>";

		# Ê½ŞÚ´¯¸Şê—pˆ—
		if ( $eggs[$m{egg}][1] eq 'Ê½ŞÚ´¯¸Ş' && rand(7) > 1 ) {
			if (rand(6) > 1) {
				$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚©‚ç $eggs[$m{egg}][1]‚ªY‚Ü‚ê‚Ü‚µ‚½<br>";
			}
			else {
				$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚Í‹ó‚Á‚Û‚Å‚µ‚½c<br>";
				$m{egg} = 0;
			}
		}
		# ±ËŞØÃ¨´¯¸Şê—pˆ—(—j“ú‚É‚æ‚è•Ï‚í‚é)
		elsif ( $eggs[$m{egg}][1] eq '±ËŞØÃ¨´¯¸Ş' ) {
			my($wday) = (localtime($time))[6];
			my @borns = @{ $eggs[5+$wday][3] };
			my $v = $borns[int(rand(@borns))];

			$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚©‚ç $pets[$v][1] ‚ªY‚Ü‚ê‚Ü‚µ‚½<br>$pets[$v][1]‚Í—a‚©‚èŠ‚É‘—‚ç‚ê‚Ü‚µ‚½<br>";
			&send_item($m{name}, 3, $v);
			$m{egg} = 0;
		}
		else {
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];

			$mes .= "‚È‚ñ‚ÆA$eggs[$m{egg}][1]‚Ì’†‚©‚ç $pets[$v][1] ‚ªY‚Ü‚ê‚Ü‚µ‚½<br>$pets[$v][1]‚Í—a‚©‚èŠ‚É‘—‚ç‚ê‚Ü‚µ‚½<br>";
			&send_item($m{name}, 3, $v);
			$m{egg} = 0;
		}
	}
	# µ°¸¼®İ‘ãA‚¨“X‚Ì”„ã‹àA‘—‹àŒn‚Ìó‚¯æ‚è
	elsif (-s "$userdir/$id/money.cgi") {
		open my $fh, "+< $userdir/$id/money.cgi" or &error("$userdir/$id/money.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $money, $is_shop_sale) = split /<>/, $line;

			if ($money < 0) {
				$m{money} += $money;
				$money *= -1;
				$mes .= "$name‚É $money G‚ğx•¥‚¢‚Ü‚µ‚½<br>";

			}
			elsif ($is_shop_sale eq '1') {
				if ($jobs[$m{job}][1] eq '¤l') {
					$mes .= "$name‚©‚ç $money G‚Ì”„ã‹à‚ğó‚¯æ‚è‚Ü‚µ‚½<br>";
				}
				else {
					my $v = int($money * $shop_sale_tax);
					$mes .= "$name‚©‚ç $money G‚Ì”„ã‹à‚ğó‚¯æ‚èA$v GÅ‹à‚Æ‚µ‚Äæ‚ç‚ê‚Ü‚µ‚½<br>";
					$money -= $v;
				}
				$m{money} += $money;
			}
			else {
				$m{money} += $money;
				$mes .= "$name‚©‚ç $money G‚ğó‚¯æ‚è‚Ü‚µ‚½<br>";
			}
		}
		# ‹âsŒo‰cÒ‚ª‘‹àƒ}ƒCƒiƒX‚É‚È‚Á‚½ê‡‚Í‹âs‚Í“|Y
		# ªC³A‘‹àƒ}ƒCƒiƒXA‚©‚ÂA‹âs—a‹à‚ª100–œˆÈ‰º‚Ì“|Y
		if ($m{money} < 0 && -f "$userdir/$id/shop_bank.cgi") {
			my $shop_id = unpack 'H*', $m{name};

			my $last_year = 0;
			my $save_money = 0;
			open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
			my $head_line = <$fh>;
			while (my $line = <$fh>) {
				my($year, $name, $money) = split /<>/, $line;
				if ($m{name} eq $name) {
					$save_money = $money;
					$last_year = $year;
					last;
				}
			}
			close $fh;
			if ($save_money < 1000000) {
				unlink "$userdir/$id/shop_bank.cgi";
				unlink "$userdir/$id/shop_sale_bank.cgi";
				&mes_and_send_news("<b>Œo‰c‚·‚é‹âs‚ÍÔšŒo‰c‚Ì‚½‚ß“|Y‚µ‚Ü‚µ‚½</b>", 1);
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	# ‘‚ÉŠ‘®‚µ‚Ä‚¢‚éê‡
	elsif ($m{country}) {
		# Rank UP
		if ($m{rank_exp} >= $m{rank} * $m{rank} * 10 && $m{rank} < $#ranks) {
			$m{rank_exp} -= $m{rank} * $m{rank} * 10;
			++$m{rank};
			$mes .= "“ú ‚Ì‘‚Ö‚ÌvŒ£‚ª”F‚ß‚ç‚êA$m{name}‚ÌŠK‹‰‚ª$ranks[$m{rank}]‚É¸i‚µ‚Ü‚µ‚½<br>";
		}
		# Rank Down
		elsif ($m{rank_exp} < 0) {
			if ($m{rank} eq '1') {
				$m{rank_exp} = 0;
			}
			else {
				--$m{rank};
				$m{rank_exp} = int($m{rank} * $m{rank} * 10 + $m{rank_exp});
				$mes .= "$m{name}‚ÌŠK‹‰‚ª$ranks[$m{rank}]‚É~Ši‚µ‚Ü‚µ‚½<br>";
			}
		}
		# ‹‹—^
	elsif ($m{country} && $time >= $m{next_salary}) {
		if($m{salary_switch} && $in{get_salary} ne '1'){
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="hidden" name="get_salary" value="1">|;
			$mes .= qq|<input type="submit" value="‹‹—¿‚ğó‚¯æ‚é" class="button1"></form>|;
		}else{
			$m{egg_c} += int(rand(50)+100) if $m{egg};
			&salary;
		}
	}
	}
}


#================================================
# ‹‹—^
#================================================
sub salary {
	# ‹‹—^Å
	sub tax { (100 - $cs{tax}[$m{country}]) * 0.01 };

	$m{next_salary} = int( $time + 3600 * $salary_hour );

	my $salary_base = $rank_sols[$m{rank}] * 0.8 + $cs{strong}[$m{country}] * 0.5;
	$salary_base += $cs{strong}[$union] * 0.6 if $union;

	my $v = int( $salary_base * &tax ) + 1000;

	# ‘‚Ì‘ã•\Ò‚È‚çÎŞ°Å½
#	$v *= 1.5 if &is_daihyo;

	# “ˆê‘‚È‚çÎŞ°Å½
	my($c1, $c2) = split /,/, $w{win_countries};
	if ($c1 eq $m{country}) {
		# “¯–¿‚È‚µ‚Å“ˆê‚È‚ç2”{
		$v *= defined $c2 ? 1.75 : 2;
	}
	elsif ($c2 eq $m{country}) {
		$v *= 1.75;
	}

	# –Å–S
	$v *= 0.5 if $cs{is_die}[$m{country}];

	# ¤l‚È‚çÎŞ°Å½
	$v += 5000 if $jobs[$m{job}][1] eq '¤l';
	$v = &use_pet('salary', $v);
	$v = int($v);

	$m{money} += $v;
	$mes .= "$c_m‚©‚ç $v G‚Ì‹‹—^‚ª‚ ‚½‚¦‚ç‚ê‚Ü‚µ‚½<br>";
}


#================================================
# ¢‘ãŒğ‘ã/ÚÍŞÙ±¯Ìß
#================================================
sub lv_up {
	$m{exp} -= 100;
	++$m{lv};

	# ¢‘ãŒğ‘ã
	if ($m{lv} >= 100) {
		$m{lv} = 1;
		&c_up('sedai');

		# Œ‹¥‚µ‚Ä‚¢‚½ê‡
		if ($m{marriage}) {
			&mes_and_world_news("$m{marriage}‚Æ‚ÌŠÔ‚É‚Å‚«‚½$m{sedai}‘ã–Ú‚Ìq‹Ÿ‚ÉˆÓu‚ªˆø‚«Œp‚ª‚ê‚Ü‚µ‚½", 1);
			for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
				$m{$k} = int($m{$k} * (rand(0.2)+0.65) );
			}
			$m{rank} -= $m{rank} > 10 ? 2 : 1;
#			$m{rank} -= int(rand(2));

			my $y_id = unpack 'H*', $m{marriage};
			if (-f "$userdir/$y_id/user.cgi") {
				my %datas = &get_you_datas($y_id, 1);
				if ($datas{skills}) { # Šo‚¦‚Ä‚¢‚é‹Z‚ğ•Û‘¶
					open my $fh, "+< $userdir/$id/skill.cgi";
					eval { flock $fh, 2; };
					my $line = <$fh>;
					$line =~ tr/\x0D\x0A//d;

					my $is_rewrite = 0;
					for my $skill (split /,/, $datas{skills}) {
						# Šo‚¦‚Ä‚¢‚È‚¢½·Ù‚È‚ç’Ç‰Á
						unless ($line =~ /,\Q$skill\E,/) {
							$is_rewrite = 1;
							$line .= "$skill,";
						}
					}
					if ($is_rewrite) {
						$line  = join ",", sort { $a <=> $b } split /,/, $line;
						$line .= ',';

						seek  $fh, 0, 0;
						truncate $fh, 0;
						print $fh $line;
					}
					close $fh;
				}

				if ($pets[$m{pet}][2] eq 'copy_pet' && $datas{pet}) {
					$mes .= "$pets[$m{pet}][1]‚Í$datas{name}‚ÌÍß¯Ä‚Ì$pets[$datas{pet}][1]‚ğºËß°‚µ‚Ü‚µ‚½<br>";
					$m{pet} = $datas{pet};
				}

			}
			$m{marriage} = '';
		}
		# Œ‹¥‚µ‚Ä‚¢‚È‚¢‚Æ‚«
		else {
			&mes_and_world_news("$m{sedai}‘ã–Ú‚Ö‚ÆˆÓu‚ªˆø‚«Œp‚ª‚ê‚Ü‚µ‚½", 1);

			if ($pets[$m{pet}][2] eq 'keep_status') {
				$mes .= "$pets[$m{pet}][1]‚Ì—Í‚É‚æ‚è½Ã°À½‚ª‚»‚Ì‚Ü‚Üˆø‚«Œp‚ª‚ê‚Ü‚µ‚½<br>";
				$mes .= "–ğ–Ú‚ğI‚¦‚½$pets[$m{pet}][1]‚ÍAŒõ‚Ì’†‚Ö‚ÆÁ‚¦‚Ä‚¢‚Á‚½c<br>";
				$m{pet} = 0;
			}
			else {
				my $down_par = $m{sedai} > 7 ? (rand(0.25)+0.6) : $m{sedai} * 0.05 + 0.35;
				for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
					$m{$k} = int($m{$k} * $down_par);
				}
				$m{rank} -= $m{rank} > 10 ? 2 : 1;
				$m{rank} -= int(rand(2));
			}
		}

		# ˆÈ‰º‹¤’Ê‚Ìˆ—
		$m{rank} = 1 if $m{rank} < 1;

		&use_pet('sedai');

		if ($m{skills}) { # Šo‚¦‚Ä‚¢‚é‹Z‚ğ•Û‘¶
			open my $fh, "+< $userdir/$id/skill.cgi";
			eval { flock $fh, 2; };
			my $line = <$fh>;
			$line =~ tr/\x0D\x0A//d;

			my $is_rewrite = 0;
			for my $skill (split /,/, $m{skills}) {
				# Šo‚¦‚Ä‚¢‚È‚¢½·Ù‚È‚ç’Ç‰Á
				unless ($line =~ /,\Q$skill\E,/) {
					$is_rewrite = 1;
					$line .= "$skill,";
				}
			}
			if ($is_rewrite) {
				$line  = join ",", sort { $a <=> $b } split /,/, $line;
				$line .= ',';

				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh $line;
			}
			close $fh;
		}
	}
	# ƒŒƒxƒ‹ƒAƒbƒv
	else {
		$mes .= "Lv±¯Ìßô<br>";

		# HP ‚¾‚¯‚Í•K‚¸‚PˆÈãup‚·‚éd—l
		my $v = int( rand($jobs[$m{job}][2]) ) + 1;
		$m{max_hp} += $v;
		$mes .= "$e2j{max_hp}+$v ";

		my $count = 3;
		for my $k (qw/max_mp at df mat mdf ag lea cha/) {
			my $v = int( rand($jobs[$m{job}][$count]+1) );
			$m{$k} += $v;
			$mes .= "$e2j{$k}+$v ";
			++$count;
		}

		&use_pet('lv_up');
	}
}




1; # íœ•s‰Â
