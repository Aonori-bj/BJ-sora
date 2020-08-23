#================================================
# メイン画面 Created by Merino
#================================================

# お店の売上金の税金(0(税金なし)～0.99まで)
my $shop_sale_tax = 0.5;

# ﾒﾆｭｰ ◎追加/変更/削除/並べ替え可能
my @menus = (
	['更新',		''],
	['ｼｮｯﾋﾟﾝｸﾞﾓｰﾙ',	'shopping'],
	['預かり所',	'depot'],
	['国庫',	'depot_country'],
	['ﾏｲﾙｰﾑ',		'myself'],
	['修行',		'training'],
	['討伐',		'hunting'],
	['国情報',		'country'],
	['内政',		'domestic'],
	['外交',		'promise'],
	['軍事',		'military'],
	['戦争',		'war_form'],
);

if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
	push @menus, ['孵化', 'incubation'];
}
if (&on_summer) {
	push @menus, ['夏祭り', 'summer_festival'];
}

#================================================
sub begin {
	&menu( map { $_->[0] } @menus );
	&main_system;
}
sub tp_1 { $cmd ? &b_menu(@menus) : &begin; }


#================================================
# ﾒｲﾝｼｽﾃﾑ
#================================================
sub main_system {
	# Lv up
	if ($m{exp} >= 100) {
		if ($m{egg}) {
			$m{egg_c} += int(rand(6)+10);
			$m{egg_c} += int(rand(16)+20) if $jobs[$m{job}][1] eq '卵士';
			push @menus, ['孵化', 'incubation'] if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]);
		}
		&lv_up;
	}
	# ﾀﾏｺﾞ成長
	#↓なぜかここの行、字下げを行うとバグる（by あおのり　2020/4/29）
elsif (!$m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
		$m{egg_c} = 0;
		$mes .= "持っていた$eggs[$m{egg}][1]が光だしました!<br>";

		# ﾊｽﾞﾚｴｯｸﾞ専用処理
		if ( $eggs[$m{egg}][1] eq 'ﾊｽﾞﾚｴｯｸﾞ' && rand(7) > 1 ) {
			if (rand(6) > 1) {
				$mes .= "なんと、$eggs[$m{egg}][1]の中から $eggs[$m{egg}][1]が産まれました<br>";
			}
			else {
				$mes .= "なんと、$eggs[$m{egg}][1]の中は空っぽでした…<br>";
				$m{egg} = 0;
			}
		}
		# ｱﾋﾞﾘﾃｨｴｯｸﾞ専用処理(曜日により変わる)
		elsif ( $eggs[$m{egg}][1] eq 'ｱﾋﾞﾘﾃｨｴｯｸﾞ' ) {
			my($wday) = (localtime($time))[6];
			my @borns = @{ $eggs[5+$wday][3] };
			my $v = $borns[int(rand(@borns))];

			$mes .= "なんと、$eggs[$m{egg}][1]の中から $pets[$v][1] が産まれました<br>$pets[$v][1]は預かり所に送られました<br>";
			&send_item($m{name}, 3, $v);
			$m{egg} = 0;
		}
		else {
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];

			$mes .= "なんと、$eggs[$m{egg}][1]の中から $pets[$v][1] が産まれました<br>$pets[$v][1]は預かり所に送られました<br>";
			&send_item($m{name}, 3, $v);
			$m{egg} = 0;
		}
	}
	# ｵｰｸｼｮﾝ代、お店の売上金、送金系の受け取り
	elsif (-s "$userdir/$id/money.cgi") {
		open my $fh, "+< $userdir/$id/money.cgi" or &error("$userdir/$id/money.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $money, $is_shop_sale) = split /<>/, $line;

			if ($money < 0) {
				$m{money} += $money;
				$money *= -1;
				$mes .= "$nameに $money Gを支払いました<br>";

			}
			elsif ($is_shop_sale eq '1') {
				if ($jobs[$m{job}][1] eq '商人') {
					$mes .= "$nameから $money Gの売上金を受け取りました<br>";
				}
				else {
					my $v = int($money * $shop_sale_tax);
					$mes .= "$nameから $money Gの売上金を受け取り、$v G税金として取られました<br>";
					$money -= $v;
				}
				$m{money} += $money;
			}
			else {
				$m{money} += $money;
				$mes .= "$nameから $money Gを受け取りました<br>";
			}
		}
		# 銀行経営者が資金マイナスになった場合は銀行は倒産
		# ↑修正、資金マイナス、かつ、銀行預金が100万以下の時倒産
		if ($m{money} < 0 && -f "$userdir/$id/shop_bank.cgi") {
			my $shop_id = unpack 'H*', $m{name};

			my $last_year = 0;
			my $save_money = 0;
			open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgiﾌｧｲﾙが開けません");
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
				&mes_and_send_news("<b>経営する銀行は赤字経営のため倒産しました</b>", 1);
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	# 国に所属している場合
	elsif ($m{country}) {
		# Rank UP
		if ($m{rank_exp} >= $m{rank} * $m{rank} * 10 && $m{rank} < $#ranks) {
			$m{rank_exp} -= $m{rank} * $m{rank} * 10;
			++$m{rank};
			$mes .= "日頃の国への貢献が認められ、$m{name}の階級が$ranks[$m{rank}]に昇進しました<br>";
		}
		# Rank Down
		elsif ($m{rank_exp} < 0) {
			if ($m{rank} eq '1') {
				$m{rank_exp} = 0;
			}
			else {
				--$m{rank};
				$m{rank_exp} = int($m{rank} * $m{rank} * 10 + $m{rank_exp});
				$mes .= "$m{name}の階級が$ranks[$m{rank}]に降格しました<br>";
			}
		}
		# 給与
	elsif ($m{country} && $time >= $m{next_salary}) {
		if($m{salary_switch} && $in{get_salary} ne '1'){
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="hidden" name="get_salary" value="1">|;
			$mes .= qq|<input type="submit" value="給料を受け取る" class="button1"></form>|;
		}else{
			$m{egg_c} += int(rand(50)+100) if $m{egg};
			&salary;
		}
	}
	}
}


#================================================
# 給与
#================================================
sub salary {
	# 給与税
	sub tax { (100 - $cs{tax}[$m{country}]) * 0.01 };

	$m{next_salary} = int( $time + 3600 * $salary_hour );

	my $salary_base = $rank_sols[$m{rank}] * 0.8 + $cs{strong}[$m{country}] * 0.5;
	$salary_base += $cs{strong}[$union] * 0.6 if $union;

	my $v = int( $salary_base * &tax ) + 1000;

	# 国の代表者ならﾎﾞｰﾅｽ
#	$v *= 1.5 if &is_daihyo;

	# 統一国ならﾎﾞｰﾅｽ
	my($c1, $c2) = split /,/, $w{win_countries};
	if ($c1 eq $m{country}) {
		# 同盟なしで統一なら2倍
		$v *= defined $c2 ? 1.75 : 2;
	}
	elsif ($c2 eq $m{country}) {
		$v *= 1.75;
	}

	# 滅亡時
	$v *= 0.5 if $cs{is_die}[$m{country}];

	# 商人ならﾎﾞｰﾅｽ
	$v += 5000 if $jobs[$m{job}][1] eq '商人';
	$v = &use_pet('salary', $v);
	$v = int($v);

	$m{money} += $v;
	$mes .= "$c_mから $v Gの給与があたえられました<br>";
}


#================================================
# 世代交代/ﾚﾍﾞﾙｱｯﾌﾟ
#================================================
sub lv_up {
	$m{exp} -= 100;
	++$m{lv};

	# 世代交代
	if ($m{lv} >= 100) {
		$m{lv} = 1;
		&c_up('sedai');

		# 結婚していた場合
		if ($m{marriage}) {
			&mes_and_world_news("$m{marriage}との間にできた$m{sedai}代目の子供に意志が引き継がれました", 1);
			for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
				$m{$k} = int($m{$k} * (rand(0.2)+0.65) );
			}
			$m{rank} -= $m{rank} > 10 ? 2 : 1;
#			$m{rank} -= int(rand(2));

			my $y_id = unpack 'H*', $m{marriage};
			if (-f "$userdir/$y_id/user.cgi") {
				my %datas = &get_you_datas($y_id, 1);
				if ($datas{skills}) { # 覚えている技を保存
					open my $fh, "+< $userdir/$id/skill.cgi";
					eval { flock $fh, 2; };
					my $line = <$fh>;
					$line =~ tr/\x0D\x0A//d;

					my $is_rewrite = 0;
					for my $skill (split /,/, $datas{skills}) {
						# 覚えていないｽｷﾙなら追加
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
					$mes .= "$pets[$m{pet}][1]は$datas{name}のﾍﾟｯﾄの$pets[$datas{pet}][1]をｺﾋﾟｰしました<br>";
					$m{pet} = $datas{pet};
				}

			}
			$m{marriage} = '';
		}
		# 結婚していないとき
		else {
			&mes_and_world_news("$m{sedai}代目へと意志が引き継がれました", 1);

			if ($pets[$m{pet}][2] eq 'keep_status') {
				$mes .= "$pets[$m{pet}][1]の力によりｽﾃｰﾀｽがそのまま引き継がれました<br>";
				$mes .= "役目を終えた$pets[$m{pet}][1]は、光の中へと消えていった…<br>";
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

		# 以下共通の処理
		$m{rank} = 1 if $m{rank} < 1;

		&use_pet('sedai');

		if ($m{skills}) { # 覚えている技を保存
			open my $fh, "+< $userdir/$id/skill.cgi";
			eval { flock $fh, 2; };
			my $line = <$fh>;
			$line =~ tr/\x0D\x0A//d;

			my $is_rewrite = 0;
			for my $skill (split /,/, $m{skills}) {
				# 覚えていないｽｷﾙなら追加
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
	# レベルアップ
	else {
		$mes .= "Lvｱｯﾌﾟ♪<br>";

		# HP だけは必ず１以上upする仕様
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




1; # 削除不可
