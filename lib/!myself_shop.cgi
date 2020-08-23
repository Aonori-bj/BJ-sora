my $this_file      = "$userdir/$id/shop.cgi";
my $shop_list_file = "$logdir/shop_list.cgi";
#================================================
# ���l�̂��X Created by Merino
#================================================

# ���ݔ�p
my $build_money = 100000;

# ���X�ɂ�����ő吔
my $max_shop_item = 20;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ������܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "�����̏��l�̂��X�̐ݒ�����܂�<br>";
		$mes .= "��$sales_ranking_cycle_day���Ԃ��X�̔��オ�Ȃ��Ƃ��X�͎����I�ɕX�ɂȂ�܂�<br>";
	}
	&menu('��߂�','���i�{��', '�X���ɒu��', '���X�̏Љ�', '���X�����Ă�');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);

	$m{tp} = $cmd * 100;
	if ($cmd eq '4') {
		if (-f $this_file) {
			$mes .= "���łɎ����̂��X�������Ă��܂�<br>";
			&begin;
		}
		elsif ($jobs[$m{job}][1] ne '���l') {
			$mes .= "�E�Ƃ����l�łȂ��Ƃ��X�����Ă邱�Ƃ��ł��܂���<br>";
			&begin;
		}
		else {
			$mes .= "���X�����Ă�ɂ� $build_money G������܂�<br>";
			$mes .= "�����l�̂��X�ݷݸނ̍X�V���߂����Ɍ��Ă�Ƃ����ɕX���Ă��܂��܂�<br>";
			&menu('��߂�','���Ă�');
		}
	}
	elsif (!-f $this_file) {
		$mes .= '�܂��́A���X�����Ă�K�v������܂�<br>';
		&begin;
	}
	else {
		&{ 'tp_'. $m{tp} };
	}
}

#=================================================
# ����
#=================================================
sub tp_400 {
	if ($cmd eq '1') {
		if (-f $this_file) {
			$mes .= "���łɎ����̂��X�������Ă��܂�<br>";
		}
		elsif ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error('���X�����Ă�̂Ɏ��s���܂���');
			close $fh;
			chmod $chmod, "$this_file";

			open my $fh2, "> $userdir/$id/shop_sale.cgi" or &error('��ٽ̧�ق��J���܂���');
			print $fh2 "0<>0<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale.cgi";

			open my $fh3, ">> $shop_list_file" or &error('���Xؽ�̧�ق��J���܂���');
			print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>\n";
			close $fh3;

			&mes_and_send_news("<b>���l�̂��X�����Ă܂���</b>", 1);
			$mes .= '<br>�����������X�ɏ��i����ׂ܂��傤<br>';
			$m{money} -= $build_money;
		}
		else {
			$mes .= '����������܂���<br>';
		}
	}
	&begin;
}

#=================================================
# ���i�{��
#=================================================
sub tp_100 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $last_time = (stat "$userdir/$id/shop_sale.cgi")[9];
	my($min,$hour,$mday,$month) = (localtime($last_time))[1..4];
	++$month;
	open my $fh2, "< $userdir/$id/shop_sale.cgi" or &error("���X̧�ق��ǂݍ��߂܂���");
	my $line = <$fh2>;
	close $fh2;
	my($sale_c, $sale_money) = split /<>/, $line;
	$mes .= "�ŏI��������F$month/$mday $hour:$min<br>";
	$mes .= "���݂̔��グ�F$sale_c�� $sale_money G<br>";

	$mes .= '<hr>�a���菊�ɖ߂��܂���?<br>';
	$mes .= '���X�̏��i�ꗗ<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�l�i</th></tr>|;

	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$no">|;
		$mes .= $kind eq '1' ? "$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
			  : $kind eq '2' ? "$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
			  : 			   "$pets[$item_no][1]"
			  ;
		$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�a���菊�ɖ߂�" class="button1"></p></form>|;

	$m{tp} = 110;
}
sub tp_110 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	if ($cmd) {
		if ($m{is_full}) {
			$mes .= '�a���菊�������ς��ł�<br>';
			&begin;
		}
		else {
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;

				if ($cmd eq $no) {

					&send_item($m{name}, $kind, $item_no, $item_c, $item_lv);

					$mes .= $kind eq '1' ? "$weas[$item_no][1]"
						  : $kind eq '2' ? "$eggs[$item_no][1]"
						  :				   "$pets[$item_no][1]"
						  ;
					$mes .= '��a���菊�ɖ߂��܂���<br>';
				}
				else {
					push @lines, $line;
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;

			&tp_100;
		}
	}
	else {
		&begin;
	}
}


#=================================================
# �X���ɒu��
#=================================================
sub tp_200 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $i = 1;

	$mes .= '�ǂ�����X�ɏo���܂���?<br>';
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;

	open my $fh, "< $userdir/$id/depot.cgi" or &error("$userdir/$id/depot.cgi ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

		$mes .= $kind eq '1' ? qq|<input type="radio" name="cmd" value="$i">[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])<br>|
			  : $kind eq '2' ? qq|<input type="radio" name="cmd" value="$i">[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])<br>|
			  :				   qq|<input type="radio" name="cmd" value="$i">[��]$pets[$item_no][1]<br>|
			  ;
		++$i;
	}
	close $fh;
	$mes .= qq|<p>�l�i�F<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɒu��" class="button1"></p></form>|;

	$m{tp} = 210;
}
sub tp_210 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	if ($cmd) {
		my @shop_items = ();
		open my $in, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
		push @shop_items, $_ while <$in>;
		close $in;

		if (@shop_items >= $max_shop_item) {
			$mes .= '����ȏエ�X�ɏ��i��u�����Ƃ͂ł��܂���<br>';
			&begin;
			return;
		}
	elsif ($in{price} =~ /[^0-9]/ || $in{price} <= 0 || $in{price} >= 5000001) {
			$mes .= '�l�i�� 1 G �ȏ� 499��9999 G�ȓ��ɂ���K�v������܂�<br>';
			&begin;
			return;
		}

		my @lines = ();
		my $i = 1;
		open my $fh, "+< $userdir/$id/depot.cgi" or &error("$userdir/$id/depot.cgi ���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			if ($cmd eq $i) {
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

				my($last_no) = (split /<>/, $shop_items[-1])[0];
				++$last_no;

				open my $fh2, ">> $this_file" or &error("$this_file���J���܂���");
				print $fh2 "$last_no<>$kind<>$item_no<>$item_c<>$item_lv<>$in{price}<>\n";
				close $fh2;

				$mes .= $kind eq '1' ? "$weas[$item_no][1]"
					  : $kind eq '2' ? "$eggs[$item_no][1]"
					  :				   "$pets[$item_no][1]"
					  ;
				$mes .= "�� $in{price} G�œX���ɕ��ׂ܂���<br>";
			}
			else {
				push @lines, $line;
			}

			++$i;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		&tp_200;
	}
	else {
		&begin;
	}
}

#=================================================
# ���X�̐ݒ�
#=================================================
sub tp_300 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error('���XؽĂ��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		if ($name eq $m{name}) {
			$is_find = 1;

			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|�O��̔���F$sale_c�� $sale_money G<br>|;
			$mes .= qq|<hr>���X�̖��O[�S�p8(���p16)�����܂�]�F<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|�Љ[�S�p20(���p40)�����܂�]�F<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="�ύX����" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;

	# ���X������̂�ؽĂɂȂ��̂͂��������̂ł�����x�ǉ�
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error('���Xؽ�̧�ق��J���܂���');
		print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>\n";
		close $fh3;
	}

	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= '��߂܂���';
		&begin;
		return;
	}

	&error('���X�̖��O���������܂��B�S�p8(���p16)�����܂�') if length $in{name} > 16;
	&error('�Љ���������܂��B�S�p20(���p40)�����܂�') if length $in{mes} > 40;

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $shop_list_file" or &error('���XؽĂ��J���܂���');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		if ($name eq $m{name}) {
			unless ($shop_name eq $in{name}) {
				$mes .= "���X�̖��O�� $in{name} �ɕς��܂���<br>";
				$shop_name = $in{name};
				$is_rewrite = 1;
			}
			unless ($message eq $in{message}) {
				$mes .= "�Љ�� $in{message} �ɕς��܂���<br>";
				$message = $in{message};
				$is_rewrite = 1;
			}

			if ($is_rewrite) {
				$line = "$shop_name<>$name<>$message<>$sale_c<>$sale_money<>\n";
			}
			else {
				last;
			}
		}
		elsif ($shop_name eq $in{name}) {
			&error("���łɓ������O�̂��X�����݂��܂�");
		}
		push @lines, $line;
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
