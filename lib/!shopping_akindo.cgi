#================================================
# ���l�̂��X Created by Merino
#================================================

#================================================
# ���X�̖��O�ꗗ�\��
#================================================
sub begin {
	$layout = 2;
	
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "�ǂ̂��X�Ŕ������܂���?<br>";
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>�X��</th><th>�X��</th><th>�Љ<br></th></tr>| unless $is_mobile;

	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";
		
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɓ���" class="button1"></p></form>|;
}

#================================================
# ���X�̏��i�ꗗ�\��
#================================================
sub tp_1 {
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��J���܂���');
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
	
	# ���X�����݂��Ȃ�
	if (!$is_find || !-f "$userdir/$shop_id/shop.cgi") {
		$mes .= "$m{stock}�Ƃ������X�͕X���Ă��܂����悤�ł�<br>";
		&begin;
	}
	# �����̂��X�Ŕ������ł��Ă��܂��ƁA�����ݷݸނ����󂵂Ă��܂��̂ŁB
	elsif ($m{name} eq $y{name}) {
		$mes .= "�����̂��X�Ŕ��������邱�Ƃ͂ł��܂���<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop.cgi") {
		$mes .= qq|�y$m{stock}�z$y{name}�u$shop_message�v<br>|;
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
		$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�l�i<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop.cgi" or &error("$y{name}�ɓ���܂���");
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
		$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
		$m{tp} = 100;
	}
	else {
#		$mes .= "�y$cmd�z������<br>";
		&begin;
	}
}

#================================================
# ����������
#================================================
sub tp_100 {
	my $shop_id = unpack 'H*', $y{name};
	if ($cmd && -f "$userdir/$shop_id/shop.cgi") {
		my $is_find    = 0;
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $userdir/$shop_id/shop.cgi" or &error("���iؽĂ��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			
			if ($cmd eq $no) {
				$is_find = 1;

				if ($m{money} >= $price) {
					$m{money} -= $price;
					
					my $item_name = $kind eq '1' ? $weas[$item_no][1]
								  : $kind eq '2' ? $eggs[$item_no][1]
								  :				   $pets[$item_no][1]
								  ;
					$mes .= "$item_name�𔃂��܂���<br>$item_name�͗a���菊�ɑ����܂���<br>";
					
					&send_item($m{name}, $kind, $item_no, $item_c, $item_lv);
					&send_money($y{name}, "�y$m{stock}($item_name)�z$m{name}", $price, 1);
					$is_rewrite = 1;
					
					# ��������Z
					open my $fh2, "+< $userdir/$shop_id/shop_sale.cgi" or &error("����̧�ق��J���܂���");
					eval { flock $fh2, 2; };
					my $line2 = <$fh2>;
					my($sale_c, $sale_money) = split /<>/, $line2;
					$sale_c++;
					$sale_money += $price;
					seek  $fh2, 0, 0;
					truncate $fh2, 0;
					print $fh2 "$sale_c<>$sale_money<>";
					close $fh2;
				}
				else {
					$mes .= "$y{name}�u����������܂���v<br>";
					last;
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
		
		unless ($is_find) {
			$mes .= "$y{name}�u���̏��i�́A������������؂�Ă��܂��܂����v<br>" ;
		}
		$cmd = $y{name}; # ���O��cmd�ɓ����&tp_1
		&tp_1;
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin
	}
}


1; # �폜�s��
