#================================================
# ���l�̋�s Created by Merino
#================================================

# ��̋�s�ŗ��p�ł���ő�l��
my $max_player_bank = 10;

# �Œ�����z
my $min_save_money = 10000;


#================================================
# ��s�̖��O�ꗗ�\��
#================================================
sub begin {
	$layout = 2;

	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "���݌_�񂵂Ă����s�y�o�c�� $m{bank}�z<br>" if $m{bank};
	$mes .= "�ǂ��̋�s�ɍs���܂���?<br>";

	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>��s��</th><th>�o�c��</th><th>�Љ<br></th></tr>| unless $is_mobile;

	my $is_find = 0;
	open my $fh, "< $logdir/shop_list_bank.cgi" or &error("$logdir/shop_list_bank.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		my $shop_id = unpack 'H*', $name;
		next unless -f "$userdir/$shop_id/shop_bank.cgi";

		$is_find = 1 if $m{bank} eq $name;
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	$m{bank} = '' unless $is_find;

	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��s�ɓ���" class="button1"></p></form>|;
}

#================================================
# ��s���X
#================================================
sub tp_1 {
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}

	my $shop_id = unpack 'H*', $y{name};

	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list_bank.cgi" or &error("$logdir/shop_list_bank.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		if ($y{name} eq $name) {
			$is_find = 1;
			$m{stock} = $shop_name;
			$shop_message = $message;
			last;
		}
	}
	close $fh;

	# ��s�����݂��Ȃ�
	if (!$is_find || !-f "$userdir/$shop_id/shop_bank.cgi") {
		$mes .= "$m{stock}�Ƃ�����s�͕X���Ă��܂����悤�ł�<br>";
		&begin;
	}
	else {
		my($fee, $rishi) = &bank_price("$userdir/$shop_id/shop_bank.cgi");
		$mes .= "�y$m{stock}�z�萔��$fee G / ���� $rishi %<br>";
		$mes .= "$y{name}�u$shop_message�v<br>";

		&menu('��߂�', '������', '�����o��');
		$m{tp} = 10;
	}
}

sub tp_10 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

sub bank_price {
	my $bank_file = shift;

	open my $fh, "< $bank_file" or &error("$bank_filȩ�ق��J���܂���");
	my $line = <$fh>;
	close $fh;

	my($fee, $rishi) = split /<>/, $line;
	return $fee, $rishi;
}



#================================================
# ����
#================================================
sub tp_100 {
	if ($m{bank} ne '' && $m{bank} ne $y{name}) {
		$mes .= "���̋�s�𗘗p����ꍇ�́A���ݗ��p���Ă����s����S�z���o���K�v������܂�<br>";
		&begin;
		return;
	}
	my $shop_id = unpack 'H*', $y{name};

	my $count = 0;
	my $last_year = '';
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
		++$count;
	}
	close $fh;

	if ($save_money > 0 || $count < $max_player_bank) {
		my($fee, $rishi) = &bank_price("$userdir/$shop_id/shop_bank.cgi");
		$mes .= qq|�y$m{stock}�z�萔��$fee G / ���� $rishi%<br>|;
		$mes .= qq|$world_name��$last_year�N���� $save_money G �a���Ă��܂�<br>| if $save_money > 0;
		$mes .= qq|������������܂���?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="text" name="save_money" value="0" class="text_box1" style="text-align:right">G<br>|;
		$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;

		$m{tp} = 110;
		&n_menu;
	}
	else {
		$mes .= "$m{stock}�͒���������ς��ŁA�����p���邱�Ƃ��ł��܂���<br>";
		&begin;
	}
}
sub tp_110 {
	if ($in{save_money} <= 0 || $in{save_money} =~ /[^0-9]/) {
		$mes .= "��߂܂���<br>";
		&begin;
		return;
	}
	elsif ($min_save_money > $in{save_money}) {
		$mes .= "�����z�͍Œ�ł� $min_save_money G�ȏ�K�v�ł�<br>";
		&tp_100;
		return;
	}

	my $shop_id = unpack 'H*', $y{name};
	my $save_money = 0;
	my @lines = ();
	open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($fee, $rishi) = split /<>/, $head_line;

	# �S�z
	if ($in{save_money} > $m{money}) {
		$in{save_money} = $m{money} - $fee;
		if ($m{name} ne $y{name} && $in{save_money} < $fee) {
			close $fh;
			$mes .= "�萔��($fee G)������܂���<br>";
			&tp_100;
			return;
		}
	}
	elsif ($m{name} ne $y{name} && $m{money} - $in{save_money} < $fee) {
		close $fh;
		$mes .= "�萔��($fee G)������܂���<br>";
		&tp_100;
		return;
	}

	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		if ($name eq $m{name}) {
			$save_money = $money;
		}
		else {
			push @lines, $line;
		}
	}

	if ($save_money + $in{save_money} > 4999999) {
		$in{save_money} = 4999999 - $save_money;
		$save_money = 4999999;
	}
	else {
		$save_money += $in{save_money};
	}
	$m{money} -= $in{save_money};

	if ($m{name} ne $y{name}) {
		$m{money} -= $fee;
		&send_money($y{name}, "�y$m{stock}(�萔��)�z$m{name}", $fee);

		# ��������Z
		open my $fh2, "+< $userdir/$shop_id/shop_sale_bank.cgi" or &error("����̧�ق��J���܂���");
		eval { flock $fh2, 2; };
		my $line2 = <$fh2>;
		my($sale_c, $sale_money) = split /<>/, $line2;
		$sale_c++;
		$sale_money += $fee;
		seek  $fh2, 0, 0;
		truncate $fh2, 0;
		print $fh2 "$sale_c<>$sale_money<>";
		close $fh2;
		$mes .= "�萔�� $fee G���x�����A";
	}

	push @lines, "$w{year}<>$m{name}<>$save_money<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	$mes .= "$in{save_money} G�������܂���(�a���z $save_money G)<br>";
	$m{bank} = $y{name};
	&tp_1;
}

#================================================
# �����o������
#================================================
sub tp_200 {
	my $shop_id = unpack 'H*', $y{name};

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

	if ($save_money == 0) {
		$mes .= "$m{name}���񂩂�̂����͗a�����Ă��܂���<br>";
		&begin;
	}
	else {
		my($fee, $rishi) = &bank_price("$userdir/$shop_id/shop_bank.cgi");
		$mes .= qq|�y$m{stock}�z�萔��$fee G / ���� $rishi%<br>|;
		$mes .= qq|$world_name��$last_year�N���� $save_money G �a���Ă��܂�<br>��������o���܂���?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="text" name="get_money" value="0" class="text_box1" style="text-align:right">G<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="���o��" class="button1"></p></form>|;

		$m{tp} += 10;
		&n_menu;
	}
}
sub tp_210 {
	$cmd = $y{name};
	if ($in{get_money} <= 0 || $in{get_money} =~ /[^0-9]/) {
		$mes .= "��߂܂���<br>";
		&tp_1;
		return;
	}

	my $shop_id = unpack 'H*', $y{name};
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };

	my $head_line = <$fh>;
	my($fee, $rishi) = split /<>/, $head_line;

	if ($m{name} ne $y{name} && $m{money} < $fee) {
		$mes .= "�萔��($fee G)������܂���";
		&tp_1;
		return;
	}

	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;

		if ($m{name} eq $name) {
			$is_rewrite = 1;

			my $v = int( $money * ($w{year} - $year) * $rishi * 0.01);
			$in{get_money} = $money if $in{get_money} >= $money;
			$m{money} += int($in{get_money} + $v);
			$money -= $in{get_money};

			if ($m{name} ne $y{name}) {
				$m{money} -= $fee;
				&send_money($y{name}, "�y$m{stock}(�萔��)�z$m{name}", $fee);
				$mes .= "�萔�� $fee G ���x�����A" ;
			}

			$mes .= "$in{get_money} G���o���܂���(�a���z $money G)<br>";

			if ($v > 0 && $m{name} ne $y{name}) {
				$mes .= "�N���Ƃ��� $v G���o���z����׽����܂���<br>";
				&send_money($y{name}, "�y$m{stock}(�N����)�z$m{name}", "-$v");
			}

			if ($money <= 0) {
				$m{bank} = '';
				$mes .= "�������z�� 0 G�ȉ��ɂȂ�܂����̂ŁA$m{stock}�ƌ_�񂪏I�����܂���<br>";
			}
			else {
				push @lines, "$w{year}<>$m{name}<>$money<>\n";
			}
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}



1; # �폜�s��
