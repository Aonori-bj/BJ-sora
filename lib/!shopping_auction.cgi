my $this_file = "$logdir/auction.cgi";
#=================================================
# ������ Created by Merino
#=================================================

# ���D����(��)
my $limit_day = 3;

# �ő�o�i��
my $max_auction = 30;

# �o�i�֎~����
my %taboo_items = (
	wea => [1,6,11,16,21,26], # ����
	egg => [], # �Ϻ�
	pet => [], # �߯�
);


#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�̕��͂��f�肵�Ă��܂�<br>";
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�����݉��ɗ��܂���<br>�������܂���?<br>';
	}
	&menu('��߂�','���D����','�o�i����');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#=================================================
# ���D
#=================================================
sub tp_100 {
	$layout = 1;
	
	$mes .= qq|�����݂̗��D�����́A�o�i������ $limit_day���O��ł�<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
 	$mes .= $is_mobile ? qq|<hr>���D�i/���D�z/���D��/�o�i��<br>|
 		: qq|<table class="table1" cellpadding="3"><tr><th>���D�i</th><th>���D�z</th><th>���D��</th><th>�o�i��<br></th>|;

	open my $fh, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price) = split /<>/, $line;
		my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
					   : $kind eq '2' ? "[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
					   : "[�y]$pets[$item_no][1]"
					   ;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$item_title/$item_price G/$to_name/$from_name<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$item_title</td><td align="right">$item_price G</td><td>$to_name</td><td>$from_name<br></td></tr>|;
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<p>���D���z�F<input type="text" name="money" value="0" class="text_box1" style="text-align:right" class="text1">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���D����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_110 {
	$in{money} = int($in{money});
	if ($m{money} < $in{money}) {
		$mes .= '����Ȃɂ����������Ă��܂���<br>';
	}
	elsif ($cmd && $in{money} && $in{money} !~ /[^0-9]/) {
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price) = split /<>/, $line;
			if ($no eq $cmd) {
				my $need_money = int($item_price * 1.2);
				if ( $in{money} >= $need_money ) {
					my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
								   : $kind eq '2' ? "[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
								   :			    "[�y]$pets[$item_no][1]"
								   ;
					
					$mes .= "$item_title�� $in{money} G�œ��D���܂���<br>";
					$line = "$bit_time<>$no<>$kind<>$item_no<>$item_c<>$item_lv<>$from_name<>$m{name}<>$in{money}<>\n";
					$is_rewrite = 1;
				}
				else {
					$mes .= "���D�͌��݂̗��D�z��1.2�{�ȏ�̋��z( $need_money G)���K�v�ł�<br>";
				}
				push @lines, $line;
			}
			# ���D����
			elsif ($time > $bit_time) {
				my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
							   : $kind eq '2' ? "[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
							   :			    "[�y]$pets[$item_no][1]"
							   ;

				&send_item($to_name, $kind, $item_no, $item_c, $item_lv);
				&send_money($to_name, '�����݉��', "-$item_price");
				&send_money($from_name, '�����݉��', $item_price);
				&write_send_news("$from_name�̏o�i����$item_title��$to_name�� $item_price G�ŗ��D���܂���");
				$is_rewrite = 1;
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
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}

#=================================================
# �o�i
#=================================================
sub tp_200 {
	$layout = 1;
	$mes .= '�ǂ���o�i���܂���?<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">$weas[$m{wea}][1]��$m{wea_lv}($m{wea_c})<br>| if $m{wea};
	$mes .= qq|<input type="radio" name="cmd" value="2">$eggs[$m{egg}][1]($m{egg_c})<br>| if $m{egg};
	$mes .= qq|<input type="radio" name="cmd" value="3">$pets[$m{pet}][1]<br>| if $m{pet};
	$mes .= qq|<p>�������z<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�o�i����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..3);
	
	my $is_find = 0;
	my @lines = ();
	open my $fh, "< $this_file" or &error("$this_file ���J���܂���ł���");
	while (my $line = <$fh>) {
		my($name) = (split /<>/, $line)[6];
		if (!$is_find && $m{name} eq $name) {
			$is_find = 1;
		}
		push @lines, $line;
	}
	close $fh;
	
	if ($is_find) {
		$mes .= '�o�i���Ă�����̂����D�����܂ŁA�o�i���邱�Ƃ͂ł��܂���<br>';
	}
	elsif (@lines >= $max_auction) {
		$mes .= '���݁A�o�i�̎�t�͂��Ă���܂���<br>�o�i���������Ă���ēx�\\�����݂�������<br>';
	}
	elsif ($in{price} =~ /[^0-9]/ || $in{price} >= 999999) {
		$mes .= '�l�i�� 99��9999 G�ȓ��ɂ���K�v������܂�<br>';
	}
	elsif ( ($cmd eq '1' && $m{wea})
		 || ($cmd eq '2' && $m{egg})
		 || ($cmd eq '3' && $m{pet}) ) {
			
			my @kinds = ('', 'wea', 'egg', 'pet');
			for my $taboo_item (@{ $taboo_items{ $kinds[$cmd] } }) {
				if ($taboo_item eq $m{ $kinds[$cmd] }) {
					my $t_item_name = $cmd eq '1' ? $weas[$m{wea}][1]
									: $cmd eq '2' ? $eggs[$m{egg}][1]
									:               $pets[$m{pet}][1]
									;
					$mes .= "$t_item_name�͏o�i�֎~���тƂȂ��Ă���܂�<br>";
					&begin;
					return;
				}
			}
			
			my $item_price = $in{price} || 0;
			my $item_no = $m{ $kinds[$cmd]       };
			my $item_c  = $m{ $kinds[$cmd].'_c'  } || 0;
			my $item_lv = $m{ $kinds[$cmd].'_lv' } || 0;
			
			if ($cmd eq '1' && $m{wea}) {
				&mes_and_send_news("$weas[$m{wea}][1]���o�i���܂���");
				$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
			}
			elsif ($cmd eq '2' && $m{egg}) {
				&mes_and_send_news("$eggs[$m{egg}][1]���o�i���܂���");
				$m{egg} = $m{egg_c} = 0;
			}
			elsif ($cmd eq '3' && $m{pet}) {
				&mes_and_send_news("$pets[$m{pet}][1]���o�i���܂���");
				$m{pet} = 0;
			}
			
			my $bit_time = $time + int( $limit_day * 3600 * 24 + rand(3600) ); # ���D���Ԃ��P���Ԓ��x�΂炯����
			
			my($last_no) = (split /<>/, $lines[-1])[1];
			++$last_no;
			open my $fh2, ">> $this_file" or &error("$this_file ���J���܂���ł���");
			print $fh2 "$bit_time<>$last_no<>$cmd<>$item_no<>$item_c<>$item_lv<>$m{name}<>$m{name}<>$item_price<>\n";
			close $fh2;
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}


1; # �폜�s��
