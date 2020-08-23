#================================================
# ���C����� Created by Merino
#================================================

# ���X�̔�����̐ŋ�(0(�ŋ��Ȃ�)�`0.99�܂�)
my $shop_sale_tax = 0.5;

# �ƭ� ���ǉ�/�ύX/�폜/���בւ��\
my @menus = (
	['�X�V',		''],
	['�����ݸ�Ӱ�',	'shopping'],
	['�a���菊',	'depot'],
	['����',	'depot_country'],
	['ϲٰ�',		'myself'],
	['�C�s',		'training'],
	['����',		'hunting'],
	['�����',		'country'],
	['����',		'domestic'],
	['�O��',		'promise'],
	['�R��',		'military'],
	['�푈',		'war_form'],
);

if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
	push @menus, ['�z��', 'incubation'];
}
if (&on_summer) {
	push @menus, ['�čՂ�', 'summer_festival'];
}

#================================================
sub begin {
	&menu( map { $_->[0] } @menus );
	&main_system;
}
sub tp_1 { $cmd ? &b_menu(@menus) : &begin; }


#================================================
# Ҳݼ���
#================================================
sub main_system {
	# Lv up
	if ($m{exp} >= 100) {
		if ($m{egg}) {
			$m{egg_c} += int(rand(6)+10);
			$m{egg_c} += int(rand(16)+20) if $jobs[$m{job}][1] eq '���m';
			push @menus, ['�z��', 'incubation'] if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]);
		}
		&lv_up;
	}
	# �Ϻސ���
	#���Ȃ��������̍s�A���������s���ƃo�O��iby �����̂�@2020/4/29�j
elsif (!$m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
		$m{egg_c} = 0;
		$mes .= "�����Ă���$eggs[$m{egg}][1]���������܂���!<br>";

		# ʽ�ڴ��ސ�p����
		if ( $eggs[$m{egg}][1] eq 'ʽ�ڴ���' && rand(7) > 1 ) {
			if (rand(6) > 1) {
				$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $eggs[$m{egg}][1]���Y�܂�܂���<br>";
			}
			else {
				$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒��͋���ۂł����c<br>";
				$m{egg} = 0;
			}
		}
		# ����è���ސ�p����(�j���ɂ��ς��)
		elsif ( $eggs[$m{egg}][1] eq '����è����' ) {
			my($wday) = (localtime($time))[6];
			my @borns = @{ $eggs[5+$wday][3] };
			my $v = $borns[int(rand(@borns))];

			$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $pets[$v][1] ���Y�܂�܂���<br>$pets[$v][1]�͗a���菊�ɑ����܂���<br>";
			&send_item($m{name}, 3, $v);
			$m{egg} = 0;
		}
		else {
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];

			$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $pets[$v][1] ���Y�܂�܂���<br>$pets[$v][1]�͗a���菊�ɑ����܂���<br>";
			&send_item($m{name}, 3, $v);
			$m{egg} = 0;
		}
	}
	# �����ݑ�A���X�̔�����A�����n�̎󂯎��
	elsif (-s "$userdir/$id/money.cgi") {
		open my $fh, "+< $userdir/$id/money.cgi" or &error("$userdir/$id/money.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $money, $is_shop_sale) = split /<>/, $line;

			if ($money < 0) {
				$m{money} += $money;
				$money *= -1;
				$mes .= "$name�� $money G���x�����܂���<br>";

			}
			elsif ($is_shop_sale eq '1') {
				if ($jobs[$m{job}][1] eq '���l') {
					$mes .= "$name���� $money G�̔�������󂯎��܂���<br>";
				}
				else {
					my $v = int($money * $shop_sale_tax);
					$mes .= "$name���� $money G�̔�������󂯎��A$v G�ŋ��Ƃ��Ď���܂���<br>";
					$money -= $v;
				}
				$m{money} += $money;
			}
			else {
				$m{money} += $money;
				$mes .= "$name���� $money G���󂯎��܂���<br>";
			}
		}
		# ��s�o�c�҂������}�C�i�X�ɂȂ����ꍇ�͋�s�͓|�Y
		# ���C���A�����}�C�i�X�A���A��s�a����100���ȉ��̎��|�Y
		if ($m{money} < 0 && -f "$userdir/$id/shop_bank.cgi") {
			my $shop_id = unpack 'H*', $m{name};

			my $last_year = 0;
			my $save_money = 0;
			open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgi̧�ق��J���܂���");
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
				&mes_and_send_news("<b>�o�c�����s�͐Ԏ��o�c�̂��ߓ|�Y���܂���</b>", 1);
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	# ���ɏ������Ă���ꍇ
	elsif ($m{country}) {
		# Rank UP
		if ($m{rank_exp} >= $m{rank} * $m{rank} * 10 && $m{rank} < $#ranks) {
			$m{rank_exp} -= $m{rank} * $m{rank} * 10;
			++$m{rank};
			$mes .= "�����̍��ւ̍v�����F�߂��A$m{name}�̊K����$ranks[$m{rank}]�ɏ��i���܂���<br>";
		}
		# Rank Down
		elsif ($m{rank_exp} < 0) {
			if ($m{rank} eq '1') {
				$m{rank_exp} = 0;
			}
			else {
				--$m{rank};
				$m{rank_exp} = int($m{rank} * $m{rank} * 10 + $m{rank_exp});
				$mes .= "$m{name}�̊K����$ranks[$m{rank}]�ɍ~�i���܂���<br>";
			}
		}
		# ���^
	elsif ($m{country} && $time >= $m{next_salary}) {
		if($m{salary_switch} && $in{get_salary} ne '1'){
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="hidden" name="get_salary" value="1">|;
			$mes .= qq|<input type="submit" value="�������󂯎��" class="button1"></form>|;
		}else{
			$m{egg_c} += int(rand(50)+100) if $m{egg};
			&salary;
		}
	}
	}
}


#================================================
# ���^
#================================================
sub salary {
	# ���^��
	sub tax { (100 - $cs{tax}[$m{country}]) * 0.01 };

	$m{next_salary} = int( $time + 3600 * $salary_hour );

	my $salary_base = $rank_sols[$m{rank}] * 0.8 + $cs{strong}[$m{country}] * 0.5;
	$salary_base += $cs{strong}[$union] * 0.6 if $union;

	my $v = int( $salary_base * &tax ) + 1000;

	# ���̑�\�҂Ȃ��ްŽ
#	$v *= 1.5 if &is_daihyo;

	# ���ꍑ�Ȃ��ްŽ
	my($c1, $c2) = split /,/, $w{win_countries};
	if ($c1 eq $m{country}) {
		# �����Ȃ��œ���Ȃ�2�{
		$v *= defined $c2 ? 1.75 : 2;
	}
	elsif ($c2 eq $m{country}) {
		$v *= 1.75;
	}

	# �ŖS��
	$v *= 0.5 if $cs{is_die}[$m{country}];

	# ���l�Ȃ��ްŽ
	$v += 5000 if $jobs[$m{job}][1] eq '���l';
	$v = &use_pet('salary', $v);
	$v = int($v);

	$m{money} += $v;
	$mes .= "$c_m���� $v G�̋��^�����������܂���<br>";
}


#================================================
# ������/���ٱ���
#================================================
sub lv_up {
	$m{exp} -= 100;
	++$m{lv};

	# ������
	if ($m{lv} >= 100) {
		$m{lv} = 1;
		&c_up('sedai');

		# �������Ă����ꍇ
		if ($m{marriage}) {
			&mes_and_world_news("$m{marriage}�Ƃ̊Ԃɂł���$m{sedai}��ڂ̎q���Ɉӎu�������p����܂���", 1);
			for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
				$m{$k} = int($m{$k} * (rand(0.2)+0.65) );
			}
			$m{rank} -= $m{rank} > 10 ? 2 : 1;
#			$m{rank} -= int(rand(2));

			my $y_id = unpack 'H*', $m{marriage};
			if (-f "$userdir/$y_id/user.cgi") {
				my %datas = &get_you_datas($y_id, 1);
				if ($datas{skills}) { # �o���Ă���Z��ۑ�
					open my $fh, "+< $userdir/$id/skill.cgi";
					eval { flock $fh, 2; };
					my $line = <$fh>;
					$line =~ tr/\x0D\x0A//d;

					my $is_rewrite = 0;
					for my $skill (split /,/, $datas{skills}) {
						# �o���Ă��Ȃ���قȂ�ǉ�
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
					$mes .= "$pets[$m{pet}][1]��$datas{name}���߯Ă�$pets[$datas{pet}][1]���߰���܂���<br>";
					$m{pet} = $datas{pet};
				}

			}
			$m{marriage} = '';
		}
		# �������Ă��Ȃ��Ƃ�
		else {
			&mes_and_world_news("$m{sedai}��ڂւƈӎu�������p����܂���", 1);

			if ($pets[$m{pet}][2] eq 'keep_status') {
				$mes .= "$pets[$m{pet}][1]�̗͂ɂ��ð�������̂܂܈����p����܂���<br>";
				$mes .= "��ڂ��I����$pets[$m{pet}][1]�́A���̒��ւƏ����Ă������c<br>";
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

		# �ȉ����ʂ̏���
		$m{rank} = 1 if $m{rank} < 1;

		&use_pet('sedai');

		if ($m{skills}) { # �o���Ă���Z��ۑ�
			open my $fh, "+< $userdir/$id/skill.cgi";
			eval { flock $fh, 2; };
			my $line = <$fh>;
			$line =~ tr/\x0D\x0A//d;

			my $is_rewrite = 0;
			for my $skill (split /,/, $m{skills}) {
				# �o���Ă��Ȃ���قȂ�ǉ�
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
	# ���x���A�b�v
	else {
		$mes .= "Lv���߁�<br>";

		# HP �����͕K���P�ȏ�up����d�l
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




1; # �폜�s��
