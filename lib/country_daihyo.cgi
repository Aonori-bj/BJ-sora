require './lib/move_player.cgi';
my $this_file = "$logdir/$m{country}/violator.cgi";
#=================================================
# ���ݒ� Created by Merino
#=================================================

# �Ǖ�����[(����\�҂�5�l)
my $need_vote_violator = 2;

# �ꊇ���M�ɕK�v�Ȕ�p
my $need_money = 3000;


#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (!&is_daihyo) {
		$mes .= '���̑�\\�҂łȂ��ƍs�����Ƃ��ł��܂���<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ����s���܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '���̺���ނ́A���̑�\\�҂̂ݍs�����Ƃ��ł��܂�<br>';
		$mes .= qq|<form method="$method" action="bbs_daihyo.cgi">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="��\\�]�c��" class="button1"></form>|;
	}
	
	&menu('��߂�', '��\\�]�c��', '�����ꊇ���M', '�ŗ�����', '�Ǖ��ҋc��', '�Ǖ��Ґ\\��', '����\\�����C');
}
sub tp_1 {
	return if &is_ng_cmd(1..6);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}


#=================================================
# �]�c������
#=================================================
sub tp_100 {
	$mes .= qq|�e���̑�\\�҂̂ݓ������邱�Ƃ��ł��܂�<br>|;
	$mes .= qq|<form method="$method" action="bbs_daihyo.cgi">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="��\\�]�c��" class="button1"></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	&begin;
}

#=================================================
# �ꊇ���M
#=================================================
sub tp_200 {
	$mes .= "���̍��ɏ���������ڲ԰�S���Ɏ莆�𑗂邱�Ƃ��ł��܂�<br>";
	$mes .= "�P��̑��M�� $need_money G������܂�<br>";

	my $rows = $is_mobile ? 2 : 6;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<textarea name="comment" cols="60" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ꊇ���M/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_210 {
	if ($in{comment}) {
		&error("�{�����������܂�(���p$max_comment�����܂�)") if length $in{comment} > $max_comment;

		if ($m{money} >= $need_money) {
			$in{comment} .= "<hr>�y$cs{name}[$m{country}]�S���ɑ��M�z";
			
			open my $fh_m, "< $logdir/$m{country}/member.cgi";
			while (my $line_m = <$fh_m>) {
				$line_m =~ tr/\x0D\x0A//d;
				
				my $y_id = unpack 'H*', $line_m;
				next unless -f "$userdir/$y_id/letter.cgi";
				
				my @lines = ();
				open my $fh, "+< $userdir/$y_id/letter.cgi" or &error('�ꊇ���M�Ɏ��s���܂���');
				eval { flock $fh, 2; };
				push @lines, $_ while <$fh>;
				unshift @lines, "$time<>$date<>$m{name}<>$m{country}<>$m{shogo}<>$addr<>$in{comment}<>$m{icon}<>\n";
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
				
				# �莆��������׸ނ����Ă�
				open my $fh9, "> $userdir/$y_id/letter_flag.cgi";
				close $fh9;
			}
			close $fh_m;
			
			$m{money} -= $need_money;
			$mes .= "$need_money G�x�����A$cs{name}[$m{country}]�S���Ɏ莆�𑗐M���܂���<br>";
		}
		else {
			$mes .= '����������܂���<br>';
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}


#=================================================
# �ŗ��ύX
#=================================================
sub tp_300 {
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|$e2j{tax} [1%�`99%]�F<input type="text" name="tax" value="$cs{tax}[$m{country}]" class="text_box_s" style="text-align:right">%<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�ύX����" class="button1"></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	if ($in{tax} && $cs{tax}[$m{country}] ne $in{tax}) {
		&error("$e2j{tax}�𔼊p�����ŋL�����Ă�������") if $in{tax} eq '' || $in{tax} =~ /[^0-9]/;
		&error("$e2j{tax}��1% �` 99%�܂łł�") if $in{tax} < 1 || $in{tax} > 99;

		$mes .= "$e2j{tax}�� $in{tax} %�ɕύX���܂���<br>";
		$cs{tax}[$m{country}] = $in{tax};
		&write_cs;
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}


#=================================================
# �Ǖ��ҋc��
#=================================================
sub tp_400 {
	$layout = 1;

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="��߂�" class="button1"></form>|;
	
	$mes .= "�c���ɂ��r�炵�⍑�̕��j�ɏ]��Ȃ��҂���������Ǖ����邱�Ƃ��ł��܂�<br>";
	$mes .= "�^����$need_vote_violator�[�ȏ�F�Ǖ��҂���������Ǖ�<br>";
	$mes .= "���΂�$need_vote_violator�[�ȏ�F�\\��������\\�҂�������Ǖ�<br>";
	$mes .= "<hr>�Ǖ���ؽ�<br>";
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos) = split /<>/, $line;
		
		my @yes_c = split /,/, $yess;
		my @no_c  = split /,/, $nos;
		my $yes_c = @yes_c;
		my $no_c  = @no_c;
		
		$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="$no">|;
		$mes .= qq|$name���w$violator�x��Ǖ����ׂ��Ǝv���Ă��܂�<br>|;
		$mes .= qq|���R�F$message<br>|;
		$mes .= qq|<input type="radio" name="answer" value="1">�^�� $yes_c�[�F$yess<br>|;
		$mes .= qq|<input type="radio" name="answer" value="2">���� $no_c�[�F$nos<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="���[" class="button_s"></form><hr>|;
	}
	close $fh;

	$m{tp} += 10;
}
sub tp_410 {
	if (!$in{answer} || $in{answer} =~ /[^12]/) {
		$mes .= '��߂܂���<br>';
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos) = split /<>/, $line;
		
		if ($cmd eq $no) {
			# �\�������̂������Ŕ��΂Ȃ�\�������
			if ($m{name} eq $name && $in{answer} eq '2') {
				$mes .= "$violator�̒Ǖ��\\��������܂���<br>";
				next;
			}
			elsif ($m{name} eq $violator) {
				&error("�����̕]�c�ɂ͓��[���邱�Ƃ��ł��܂���");
			}

			my $v_id = unpack 'H*', $violator;
			# �����폜�Ȃǂŏ����Ă����ꍇ�͏��O
			if (!-f "$userdir/$v_id/user.cgi") {
				$mes .= "$violator�Ƃ�����ڲ԰�����݂��܂���<br>";
				next;
			}
			# �����ɂ��Ȃ��ꍇ�͏��O
			elsif ( !&is_my_country($violator) ) {
				$mes .= "$violator�Ƃ�����ڲ԰��$cs{name}[$m{country}]�ɏ������Ă���܂���<br>";
				next;
			}

			# ���łɎ������ǂ��炩�ɓ���Ă����ꍇ�̂��߂ɁA��񔒎��ɂ���
			my $new_yess = '';
			my $new_nos  = '';
			for my $n (split /,/, $yess) {
				next if $m{name} eq $n;
				$new_yess .= "$n,";
			}
			for my $n (split /,/, $nos) {
				next if $m{name} eq $n;
				$new_nos .= "$n,";
			}
			
			if ($in{answer} eq '1') {
				$new_yess .= "$m{name},";
				$mes .= "$violator�̒Ǖ��Ɏ^�����܂�<br>";
			}
			elsif ($in{answer} eq '2') {
				$new_nos .= "$m{name},";
				$mes .= "$violator�̒Ǖ��ɔ��΂��܂�<br>";
			}

			my @yes_c = split /,/, $new_yess;
			my @no_c  = split /,/, $new_nos;
			my $yes_c = @yes_c;
			my $no_c  = @no_c;
			
			if ($yes_c >= $need_vote_violator) {
				my %datas = &get_you_datas($v_id, 1);
				&move_player($violator, $datas{country}, 0);

				&regist_you_data($violator, 'wt', 3 * 24 * 3600);
				&regist_you_data($violator, 'country', 0);
				&regist_you_data($violator, 'lib', '');
				&regist_you_data($violator, 'tp', 0);

				&write_world_news("�y�c���z$cs{name}[$m{country}]�̑�\\�ҒB�̕]�c�ɂ��A$violator�����O�Ǖ��ƂȂ�܂���", 1, $violator);
				$mes .= "�^����$need_vote_violator�[�ȏ�ɂȂ����̂�$violator���Ǖ�����܂���<br>";
			}
			elsif ($no_c >= $need_vote_violator) {
				my $y_id = unpack 'H*', $name;
				next unless -f "$userdir/$y_id/user.cgi"; # �\�������l�������Ă����ꍇ
				&move_player($name, $country, 0);

				&regist_you_data($name, 'wt', 3 * 24 * 3600);
				&regist_you_data($name, 'country', 0);
				&regist_you_data($name, 'lib', '');
				&regist_you_data($name, 'tp', 0);

				&write_world_news("�y�c���z$cs{name}[$m{country}]�̑�\\�ҒB�̕]�c�ɂ��A$name�����O�Ǖ��ƂȂ�܂���", 1, $name);
				$mes .= "���΂�$need_vote_violator�[�ȏ�ɂȂ����̂�$name���Ǖ�����܂���<br>";
			}
			else {
				push @lines, "$no<>$name<>$country<>$violator<>$message<>$new_yess<>$new_nos<>\n";
			}
		}
		else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	&begin;
}

#=================================================
# �Ǖ��Ґ\��
#=================================================
sub tp_500 {
	$mes .= qq|�����̑�\\�ҒB�̋c���ɂ�莩������ڲ԰��Ǖ����邱�Ƃ��ł��܂�<br>|;
	$mes .= qq|�������\\�������̂�����ꍇ�́A�Ǖ��ҋc���Ŕ��΂ɓ���Ă�������<br>|;
	$mes .= qq|<hr>�Ǖ��Ґ\\��<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|���O�F<input type="text" name="violator" class="text_box1"><br>|;
	$mes .= qq|���R[�S�p40(���p80)�����܂�]�F<br><input type="text" name="message" class="text_box_b">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�\\������" class="button1"></p></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_510 {
	if ($in{violator} && $in{message}) {
		&error('���������������܂��S�p40(���p80)�����܂�') if length $in{message} > 80;

		my $y_id = unpack 'H*', $in{violator};
		
		if (-f "$userdir/$y_id/user.cgi") {
			if ( &is_my_country($in{violator}) ) {
				my @lines = ();
				open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
				eval { flock $fh, 2; };
				push @lines, $_ while <$fh>;
				my($last_no) = (split /<>/, $lines[0])[0];
				++$last_no;
				push @lines, "$last_no<>$m{name}<>$m{country}<>$in{violator}<>$in{message}<>$m{name},<><>\n";
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
				
				$mes .= "$in{violator}��$in{message}�̗��R�ŒǕ��҂Ƃ��Đ\\�����܂���<br>";
			}
			else {
				$mes .= "$cs{name}[$m{country}]��$in{violator}�Ƃ�����ڲ԰���������Ă��܂���<br>";
			}
		}
		else {
			$mes .= "$in{violator}�Ƃ�����ڲ԰�����݂��܂���<br>";
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}


#=================================================
# ���̑�\���C
#=================================================
sub tp_600 {
	$mes .= "���ݑ�\\�ƂȂ��Ă����\\�߲�Ă�����ؾ�Ă���܂�<br>";
	$mes .= "$e2j{ceo}�̎��C��$e2j���[���玫�C���Ă�������<br>";
	$mes .= "���̑�\\�҂����C���܂���?<br>";
	&menu('��߂�', '���C����');

	$m{tp} += 10;
}
sub tp_610 {
	return if &is_ng_cmd(1);

	if ($cs{ceo}[$m{country}] eq $m{name}) {
		$mes .= "$e2j{ceo}�̎��C��$e2j{ceo}���[�ōs���Ă�������<br>";
		&begin;
		return;
	}

	for my $k (qw/war pro dom mil/) {
		if ($cs{$k}[$m{country}] eq $m{name}) {
			$cs{$k}[$m{country}] = '';
			$cs{$k.'_c'}[$m{country}] = 0;
			&write_cs;
			
			$m{$k.'_c'} = 0;
			&mes_and_world_news("$e2j{$k}�����C���܂���", 1);
			last;
		}
	}
	
	&begin;
}


#=================================================
# �Ǖ����悤�Ƃ��Ă���l�͎����̐l? 1(true) or 0(false)
#=================================================
sub is_my_country {
	my $name = shift;
	open my $fh, "< $logdir/$m{country}/member.cgi" or &error("$logdir/$m{country}/member.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		return 1 if $line eq $name;
	}
	close $fh;
	return 0;
}


1; # �폜�s��