my $entry_file = $m{sex} eq '1' ? "$logdir/marriage_man.cgi" : "$logdir/marriage_woman.cgi";
my $this_file  = $m{sex} eq '2' ? "$logdir/marriage_man.cgi" : "$logdir/marriage_woman.cgi";
#================================================
# �������k�� Created by Merino
#================================================

# �ő�o�^��:�Â��l�͎����폜
my $max_marriage_list = 20;

# ���ِ���:�������وȏ�łȂ��Ɨ��p�ł��Ȃ�
my $need_lv = 20;

# �o�^��,����߰�ޗ�
my $need_money = $m{sedai} > 20 ? int(40000+$m{lv}*1000) : int($m{sedai}*2000+$m{lv}*1000);


#================================================
# ���p����
#================================================
sub is_satisfy {
	if ($m{lv} < $need_lv) { # Lv
		$mes .= "�������k���́ALv.$need_lv�ȏ�̕��łȂ��Ɠ���܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{marriage}) { # ����
		$mes .= "�s�ς��邱�Ƃ͂ł��܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ�������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�����͌������k���ł������܂�<br>';
		$mes .= '�{���͂ǂ̂悤�Ȃ��p���ł��傤��?<br>';
	}
	
	&menu('��߂�','�߰�Ű��T��','�o�^����','���񂷂�');
}

sub tp_1 {
	return if &is_ng_cmd(1..3);

	$m{tp} = $cmd * 100;
	&{'tp_'. $m{tp} };
}

#================================================
# �߰�Ű�T��
#================================================
sub tp_100 {
	$layout = 1;
	$mes .= '�����炪�A�o�^��ؽĂɂȂ�܂�<br>';
	$mes .= '�C�ɂȂ�������܂�������۰������Ă݂Ă͂������ł���?<br>';
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>���O</th><th>$e2j{name}</th><th>�o�^��</th><th>Lv</th><th>�K��</th><th>ү����<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file ���J���܂���");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		$name .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/�o�^��$mdate/Lv$lv/�K��$ranks[$rank]/$message<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$ranks[$rank]</td><td>$message<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���۰�����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
# ------------------
# ���۰�
sub tp_110 {
	unless ($cmd) {
		&begin;
		return;
	}
	
	my $send_to;
	open my $fh, "< $this_file" or &error("$this_file ���J���܂���");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($cmd eq $no) {
			$send_to = $name;
			last;
		}
	}
	close $fh;

	unless ($send_to) {
		$mes .= '�o�^��ؽĂɓo�^����Ă��Ȃ��l�ɂͱ��۰��ł��܂���<br>';
		&begin;
		return;
	}

	$layout = 1;
	$mes .= "���۰�(�����ү���ނ𑗂�)�͖����ł�<br>";
	$mes .= "����߰�ނ́A�������Ă����s���Ă� $need_money G������܂��̂ŁA<br>����߰�ނ͐e���Ȋ֌W�ɂȂ��Ă���ɂ��܂��傤<br>";
	
	my $rows = $is_mobile ? 2 : 6;
	$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="$cmd">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|[$send_to]�ɱ��۰�<br>|;
	$mes .= qq|<textarea name="comment" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="submit" value="�莆�𑗂�/��߂�" class="button1">|;
	$mes .= qq|�@ <input type="checkbox" name="is_proposal" value="1"> ����߰��</form>|;
	$m{tp} += 10;
}
# ------------------
sub tp_120 {
	if (!$in{comment}) {
		$mes .= '�{��������܂���<br>';
		&begin;
		return;
	}
	elsif ($in{is_proposal}) {
		if ( !&is_entry_marriage($m{name}) ) {
			$mes .= "����߰�ނ���ɂ͓o�^����K�v������܂�<br>";
			&begin;
			return;
		}
		elsif ($m{money} < $need_money) {
			$mes .= "����߰�ނ���ɂ� $need_money G�K�v�ł�<br>";
			&begin;
			return;
		}
	}
	
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file ���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($cmd eq $no) {
			if ($name eq $m{name}) { # ���]���ɂ��
				$mes .= '�����ɱ��۰����邱�Ƃ͂ł��܂���<br>';
				$is_rewrite = 1;
			}
			elsif ( &is_unmarried($name) ) { # ���݂��� + �����Ȃ�
				$in{comment} .= "<hr>�y�������k���F$m{name}�l����$name�l���z";
				$in{comment} .= "������߰�ށ�" if $in{is_proposal};
				&send_letter($name);
				$mes .= "$name�ɱ��۰��̎莆�𑗂�܂���<br>";
				
				# ����߰��
				&proposal($name) if $in{is_proposal};
				
				push @lines, $line;
			}
			else {
				$is_rewrite = 1;
			}
		}
		else {
			push @lines, $line;
		}
	}
	# ���݂��Ȃ��l�A���]�������l�A�����̐l�������珑������
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
	
	&begin;
}

# ------------------
# ����߰��
sub proposal {
	my $name = shift;
	
	my $y_id = unpack 'H*', $name;
	my @lines = ();
	open my $fh, "+< $userdir/$y_id/proposal.cgi" or &error("$userdir/$y_id/proposal.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($pname) = (split /<>/, $line)[2];
		next if $pname eq $m{name};
		push @lines, $line
	}
	my($last_no) = (split /<>/, $lines[0])[0];
	++$last_no;
	unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{lv}<>$m{rank}<>$m{shogo}<>$m{mes}<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	$mes .= "����߰�ޑ� $need_money G���x�����A$name������߰�ނ��܂���<br>";
	$m{money} -= $need_money;
}

#================================================
# �o�^
#================================================
sub tp_200 {
	$layout = 2;
	my $sex_name   = $m{sex} eq '1' ? '�j��' : '����';
	
	$mes .= qq|�o�^����ɂ́A$need_money G������܂�<br>|;
	$mes .= qq|<hr>���ݓo�^����Ă���$sex_nameؽ�<br>|;
	$mes .= qq|<table class="table1"><tr><th>���O</th><th>$e2j{name}</th><th>�o�^��</th><th>Lv</th><th>�K��</th><th>ү����<br></th></tr>| unless $is_mobile;

	open my $fh, "< $entry_file" or &error("$entry_filȩ�ق��J���܂���");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		$name .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr>$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/�o�^��$mdate/Lv$lv/�K��$ranks[$rank]/$message<br>|
			 : qq|<tr><td>$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$ranks[$rank]</td><td>$message<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;

	&menu('��߂�','�o�^����');
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1);

	my $is_find = 0;
	my @lines = ();
	open my $fh, "+< $entry_file" or &error("$entry_filȩ�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
		if ($name eq $m{name}) {
			$is_find = 1;
			last;
		}
		push @lines, $line;

		last if @lines >= $max_marriage_list+1;
	}
	if ($is_find) {
		close $fh;
		$mes .= "$m{name}�l�͂��łɂ��o�^�ς݂ł�<br>";
	}
	elsif ($m{money} < $need_money) {
		close $fh;
		$mes .= "�o�^���邨��������܂���<br>";
	}
	else {
		my($last_no) = (split /<>/, $lines[0])[0];
		++$last_no;
		unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{lv}<>$m{rank}<>$m{shogo}<>$m{mes}<>$m{icon}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$mes .= "�o�^�� $need_money G���x�����܂���<br>";
		$mes .= "$m{name}�l�ł��ˁB���o�^�������܂���<br>";
		$m{money} -= $need_money;
	}
	
	&begin;
}


#================================================
# ���񂷂�
#================================================
sub tp_300 {
	if (-s "$userdir/$id/proposal.cgi") {
		$layout = 1;
		$mes .= '����߰�ގ҈ꗗ<br>';
			
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
		$mes .= qq|<table class="table1"><tr><th>���O</th><th>$e2j{name}</th><th>�o�^��</th><th>Lv</th><th>�K��</th><th>ү����<br></th></tr>| unless $is_mobile;
		
		open my $fh, "< $userdir/$id/proposal.cgi" or &error("$userdir/$id/proposal.cgi ̧�ق��ǂݍ��߂܂���");
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/�o�^��$mdate/Lv$lv/�K��$ranks[$rank]/$message<br>|
				: qq|<tr><td><input type="radio" name="cmd" value="$no">$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$lv</td><td>$ranks[$rank]</td><td>$message<br></td></tr>|;
		}
		close $fh;
		$mes .= qq|</table>| unless $is_mobile;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="�i���̈��𐾂�" class="button1"></p></form>|;
		
		$m{tp} += 10;
	}
	else {
		$mes .= '�܂��A�N���������߰�ނ���Ă��Ȃ��悤�ł�<br>';
		$mes .= '�҂��Ă��Ă��n�܂�܂���<br>�����炩����۰����Ă݂Ă͂������ł��傤?<br>';
		&begin;
	}
}
# ����
sub tp_310 {
	if ($cmd) {
		my $is_marriage = 0;
		open my $fh, "+< $userdir/$id/proposal.cgi" or &error("$userdir/$id/proposal.cgi ̧�ق��ǂݍ��߂܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			if ($cmd eq $no) {
				if ( &is_unmarried($name) ) {
					$mes .= "$name�ƌ������邱�ƂɌ��߂܂���!<br>";
					
					# ����̌������ڂ�ύX
					&regist_you_data($name, 'marriage', $m{name});
					
					$m{marriage} = $name;
					$is_marriage = 1;
					
					# ����̎v���o̧�قɏ�������
					&write_memory("$m{name}�ƌ������܂�����", $name);
					&write_memory("$name�ƌ������܂�����");
					&write_world_news(qq|<font color="#FF99FF">����:�*'����'*�:����$m{name}��$name���������܂���</font>|);
					
					my %you_datas = &get_you_datas($name);
					my $v = int( ($rank_sols[$you_datas{rank}] + $rank_sols[$m{rank}]) * 0.5);
					
					&send_money($name,    '�����j����', $v);
					&send_money($m{name}, '�����j����', $v);
					
					# �o�^����Ă��閼�O���폜
					&delete_entry_marriage($m{name});
					&delete_entry_marriage($name);
					
					last;
				}
			}
			else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines unless $is_marriage; # ������I���������A���炩�̖��Ō����ł����A���̐l�������㏑��
		close $fh;
	}
	
	&begin;
}


#================================================
# �������ǂ���
#================================================
sub is_unmarried {
	my $name = shift;
	my $y_id = unpack 'H*', $name;

	unless (-f "$userdir/$y_id/user.cgi") {
		$mes .= "�c�O�Ȃ��Ƃ�$name�l�͂��łɑ��E���Ă��܂����悤�ł��c<br>";
		return 0;
	}
	
	my %you_datas = &get_you_datas($name);
	
	if ($m{sex} eq $you_datas{sex}) {
		$mes .= "�c�O�Ȃ��Ƃ�$name�l�͐��ʂ��ς���Ă��܂����悤�ł��c<br>";
		return 0;
	}
	elsif ($you_datas{marriage} eq '') { # ����
		return 1;
	}
	else {
		$mes .= "�c�O�Ȃ��Ƃ�$name�l�͂��łɑ��̐l�ƌ������Ă��܂����悤�ł��c<br>";
		return 0;
	}
}

#================================================
# �o�^�҂��ǂ���
#================================================
sub is_entry_marriage {
	my $entry_name = shift || $m{name};
	
	open my $fh, "< $entry_file" or &error("$entry_filȩ�ق��J���܂���");
	while (my $line = <$fh>) {
		my($name) = (split /<>/, $line)[2];
		return 1 if $name eq $entry_name;
	}
	close $fh;
	
	return 0;
}

#================================================
# �o�^�폜
#================================================
sub delete_entry_marriage {
	my $del_name = shift || $m{name};
	
	for my $file ($entry_file, $this_file) {
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $file" or &error("$filȩ�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
			if ($name eq $del_name) {
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
}


1; # �폜�s��