require './lib/move_player.cgi';
my $this_file = "$logdir/violator.cgi";
#=================================================
# ���ݒ� Created by Merino
#=================================================

# �N��̋c���ɂ����ڲ԰�폜����(0:�Ȃ�,1:����)
my $is_ceo_delete = 1;

# �폜��������̏ꍇ�B�K�v�[
my $need_vote_violator = 2;

# �폜��������̏ꍇ�B�N��̑��dIP��������(0:�Ȃ�,1:����)
my $is_ceo_watch_multi = 1;


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
	elsif ($cs{ceo}[$m{country}] ne $m{name}) {
		$mes .= "����$e2j{ceo}�łȂ��ƍs�����Ƃ��ł��܂���<br>";
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
		$mes .= "���Y�҂��e����$e2j{ceo}�̓��[�ɂ��폜���邱�Ƃ��ł��܂�<br>" if $is_ceo_delete;
		$mes .= "$c_m�̖��O�A�F�A���j��ύX���邱�Ƃ��ł��܂�<br>";
		$mes .= "$e2j{name}�F$c_m<br>";
		$mes .= "���F�F$cs{color}[$m{country}]<br>";
	}
	my @menus = ('��߂�', '����/�F��ύX', '���j/����ق�ύX');
	if ($is_ceo_delete) {
		push @menus, '���Y�ҋc��';
		push @menus, '���Y�Ґ\\��';
		
		if ($is_ceo_watch_multi) {
			push @menus, '���d������';
		}
	}
	&menu(@menus);
}
sub tp_1 {
	return if &is_ng_cmd(1..5);

	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#================================================
# ����/�F��ύX
#================================================
sub tp_100 {
	$mes .= qq|$e2j{name}�͑S�p7(���p14)�����܂ŁB���p�L��(,;"'&)�A��(��߰�)�͎g���܂���<br>|;
	$mes .= qq|���F��#����n�܂�16�i���\\�L<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|$e2j{name}�F<input type="text" name="name" value="$c_m" class="text_box1"><br>|;
	$mes .= qq|�F�F<input type="text" name="color" value="$cs{color}[$m{country}]" class="text_box1"><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	my $is_rewrite = 0;
	if ($in{name} || $in{color}) {
		unless ($c_m eq $in{name}) {
			&error("$e2j{name}���L�����Ă�������") if $in{name} eq '';
			&error("$e2j{name}�ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�") if $in{name} =~ /[,;\"\'&<>\\\/]/;
			&error("$e2j{name}�ɕs���ȋ󔒂��܂܂�Ă��܂�") if $in{name} =~ /�@/ || $in{name} =~ /\s/;
			&error("$e2j{name}�͑S�p7(���p14)�����܂łł�") if length $in{name} > 14;
			for my $name (@{ $cs{name} }) {
				&error('����$e2j{name}�͂��łɎg���Ă��܂�') if $in{name} eq $name;
			}
			
			$in{color} ||= $cs{color}[$m{country}];
			$mes .= "$e2j{name}��$in{name}�ɕύX���܂���<br>";
			&write_world_news(qq|<b>$c_m��$e2j{ceo}$m{name}�ɂ���āA$c_m��<font color="$in{color}">$in{name}</font>��$e2j{name}�����߂܂���</b>|, 1);
			
			$cs{name}[$m{country}] = $in{name};
			$is_rewrite = 1;
		}
	
		unless ($cs{color}[$m{country}] eq $in{color}) {
			&error('�F�𔼊p�p�����ŋL�����Ă�������') if $in{color} eq '' || $in{color} =~ /[^0-9a-zA-Z#]/;
			&error('�F��#����n�܂�16�i���̐F�ŋL�����Ă�������') if $in{color} !~ /#.{6}/;
			$mes .= "���F��$in{color}�ɕύX���܂���<br>";
			$cs{color}[$m{country}] = $in{color};
			$is_rewrite = 1;
		}
	}

	if ($is_rewrite) {
		&write_cs;
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}

#================================================
# ���j��ύX
#================================================
sub tp_200 {
	my $line = &get_countries_mes($m{country});
	my($country_mes, $country_mark) = split /<>/, $line;
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|���j[�S�p100(���p200)�����܂�]<br>�E���s�͍폜����܂�<br>|;
	$mes .= qq|<textarea name="country_mes" cols="60" rows="3" class="textarea1">$country_mes</textarea><br>|;
	$mes .= qq|<hr>�����<br>|;

	# �����
	$mes .= qq|<input type="radio" name="country_mark" value="">�Ȃ�<hr>|;
	if ($country_mark) {
		my $file_title = &get_goods_title($country_mark);
		$mes .= qq|<input type="radio" name="country_mark" value="$country_mark" checked><img src="$icondir/$country_mark">[���݂̼����]$file_title<hr>|;
	}
	opendir my $dh, "$userdir/$id/picture" or &error("$userdir/$id/picture �ިڸ�؂��J���܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^_/;
		next if $file_name =~ /^index.html$/;
		my $file_title = &get_goods_title($file_name);
		$mes .= qq|<input type="radio" name="country_mark" value="$file_name"><img src="$userdir/$id/picture/$file_name" style="vertical-align:middle;">$file_title<hr>|;
	}
	closedir $dh;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_210 {
	unless (defined $in{country_mes}) {
		$mes .= "��߂܂���<br>";
		&begin;
		return;
	}
	
	&error("���̕��j�͑S�p100(���p200)�����܂łł�") if length $in{country_mes} > 200;
	&error("�M�l�c�����V���E�g�V�e�C���m�J�c���J�b�e�C���m�J�c�H") if $w{world} eq $#world_states && $m{country} eq $w{country};
	
	my $is_rewrite = 0;
	my $country = 0;
	my @lines = ();
	open my $fh, "+< $logdir/countries_mes.cgi" or &error("$logdir/countries_mes.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if ($country eq $m{country}) {
			my($country_mes, $country_mark) = split /<>/, $line;
			
			unless ($country_mes eq $in{country_mes}) {
				$is_rewrite = 1;
				$mes .= "���̕��j��<hr>$in{country_mes}<hr>�ɕύX���܂���<br>";
			}
			
			# ����ق��聨�Ȃ�
			if ($country_mark && $in{country_mark} eq '') {
				$is_rewrite = 1;
				rename "$icondir/$country_mark", "$userdir/$id/picture/$country_mark" or &error("����ق̏��������Ɏ��s���܂���");
				$mes .= qq|���̼���ق��Ȃ��ɕύX���܂���<br>|;
			}
			# ����ٕύX
			elsif ($country_mark ne $in{country_mark}) {
				&error("�������ق̼���ق����łɎg���Ă��܂�") if -f "$icondir/$in{country_mark}";
				&error("$non_title�̕������قɂ��邱�Ƃ͂ł��܂���") if $in{country_mark} =~ /^_/;
				&error("�I�������G�����݂��܂���") unless -f "$userdir/$id/picture/$in{country_mark}";

				$is_rewrite = 1;
				rename "$icondir/$country_mark", "$userdir/$id/picture/$country_mark" or &error("����ق̏��������Ɏ��s���܂���") if -f "$icondir/$country_mark";
				rename "$userdir/$id/picture/$in{country_mark}", "$icondir/$in{country_mark}" or &error("����ق̏��������Ɏ��s���܂���");
				
				my $file_title = &get_goods_title($in{country_mark});
				$mes .= qq|���̼���ق�$file_title<img src="$icondir/$in{country_mark}">�ɕύX���܂���<br>|;
			}
			
			if ($is_rewrite) {
				$line = "$in{country_mes}<>$in{country_mark}<>\n";
			}
			else {
				$mes .= "��߂܂���<br>";
				last;
			}
		}
		push @lines, $line;
		++$country;
	}
	if ($country < $m{country}) { # �o�O�ō��̕��j�̐��ƍ��̐�������Ȃ���
		$is_rewrite = 1;
		push @lines, "$in{country_mes}<><>\n";
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}


#================================================
# ���Y�ҋc��
#================================================
sub tp_300 {
	unless ($is_ceo_delete) {
		&begin;
		return;
	}
	
	$layout = 1;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="��߂�" class="button1"></form>|;

	$mes .= "�e��$e2j{ceo}�̋c���ɂ��r�炵�⑽�d�o�^�҂Ȃǂ𗬌Y(�폜)���邱�Ƃ��ł��܂�<br>";
	$mes .= "���ȓI�ȍl����NG�B�܂��͊e����\\�]�c��ő��k<br>";
	$mes .= "�^����$need_vote_violator�[�ȏ�F���Y�҂𗬌Y<br>";
	$mes .= "���΂�$need_vote_violator�[�ȏ�F�\\������$e2j{ceo}��������Ǖ�<br>";
	$mes .= '<hr>���Y��ؽ�<br>';
	open my $fh, "< $this_file" or &error("$logdir/suspect.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos) = split /<>/, $line;
		
		my @yes_c = split /,/, $yess;
		my @no_c  = split /,/, $nos;
		my $yes_c = @yes_c;
		my $no_c  = @no_c;
		
		$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="$no">|;
		$mes .= qq|<font color="$cs{color}[$country]">$cs{name}[$country]</font>��$e2j{ceo}$name���w$violator�x�𗬌Y���ׂ��Ǝv���Ă��܂�<br>|;
		$mes .= qq|���R�F$message<br>|;
		$mes .= qq|<input type="radio" name="answer" value="1">�^�� $yes_c�[�F$yess<br>|;
		$mes .= qq|<input type="radio" name="answer" value="2">���� $no_c�[�F$nos<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="���[" class="button_s"></form><hr>|;
	}
	close $fh;

	$m{tp} += 10;
}

sub tp_310 {
	unless ($is_ceo_delete) {
		&begin;
		return;
	}
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
				$mes .= "$violator�̗��Y�Ґ\\��������܂���<br>";
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
				$mes .= "$violator�̗��Y�Ɏ^�����܂�<br>";
			}
			elsif ($in{answer} eq '2') {
				$new_nos .= "$m{name},";
				$mes .= "$violator�̗��Y�ɔ��΂��܂�<br>";
			}

			my @yes_c = split /,/, $new_yess;
			my @no_c  = split /,/, $new_nos;
			my $yes_c = @yes_c;
			my $no_c  = @no_c;
			
			if ($yes_c >= $need_vote_violator) {
				my %datas = &get_you_datas($v_id, 1);
				&move_player($violator, $datas{country}, 'del');
				&write_world_news("<b>�y�c���z�e����$e2j{ceo}�B�̕]�c�ɂ��A$cs{name}[$datas{country}]��$violator�����Y�ɂȂ�܂���</b>");
				$mes .= "�^����$need_vote_violator�[�ȏ�ɂȂ����̂�$violator�͗��Y�ƂȂ�܂�<br>";

				# �ᔽ�҃��X�g�ɒǉ�
				open my $fh2, ">> $logdir/deny_addr.cgi" or &error("$logdir/deny_addr.cgi̧�ق��J���܂���");
				print $fh2 $datas{agent} =~ /DoCoMo/ || $datas{agent} =~ /KDDI|UP\.Browser/
					|| $datas{agent} =~ /J-PHONE|Vodafone|SoftBank/ ? "$datas{agent}\n" : "$datas{addr}\n";
				close $fh2;
			}
			elsif ($no_c >= $need_vote_violator) {
				my $y_id = unpack 'H*', $name;
				next unless -f "$userdir/$y_id/user.cgi"; # �\�������l�������Ă����ꍇ
				&move_player($name, $country, 0);

				&regist_you_data($name, 'wt', 3 * 24 * 3600);
				&regist_you_data($name, 'country', 0);
				&regist_you_data($name, 'lib', '');
				&regist_you_data($name, 'tp', 0);

				&write_world_news("�y�c���z�e����$e2j{ceo}�B�̕]�c�ɂ��A$cs{name}[$country]��$e2j{ceo}$name�����O�Ǖ��ƂȂ�܂���</b>", 1, $name);
				$mes .= "���΂�$need_vote_violator�[�ȏ�ɂȂ����̂�$name�����O�Ǖ��ƂȂ�܂�<br>";
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


#================================================
# ���Y�Ґ\��
#================================================
sub tp_400 {
	unless ($is_ceo_delete) {
		&begin;
		return;
	}
	$mes .= qq|�������\\�������̂�����ꍇ�́A���Y�ҋc���Ŕ��΂ɓ���Ă�������<br>|;
	$mes .= qq|<hr>���Y�Ґ\\��<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|���O�F<input type="text" name="violator" value="$in{violator}" class="text_box1"><br>|;
	$mes .= qq|���R[�S�p40(���p80)�����܂�]�F<br><input type="text" name="message" class="text_box_b">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�\\������" class="button1"></p></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_410 {
	unless ($is_ceo_delete) {
		&begin;
		return;
	}
	if ($in{violator} && $in{message}) {
		&error('���������������܂��S�p40(���p80)�����܂�') if length $in{message} > 80;

		my $y_id = unpack 'H*', $in{violator};
		
		if (-f "$userdir/$y_id/user.cgi") {
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
			
			$mes .= "$in{violator}��$in{message}�̗��R�ŗ��Y�҂Ƃ��Đ\\�����܂���<br>";
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


#================================================
# ���d������
#================================================
sub tp_500 {
	if (!$is_ceo_delete || !$is_ceo_watch_multi) {
		&begin;
		return;
	}

	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		open my $fh, "< $userdir/$id/user.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
		my $line_data = <$fh>;
		my $line_info = <$fh>;
		close $fh;
		
		my %p = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$p{$k} = $v;
		}
		($p{addr}, $p{host}, $p{agent}) = split /<>/, $line_info;

		my $line = "$id<>";
		for my $k (qw/name shogo country addr host agent ldate/) {
			$line .= "$p{$k}<>";
		}
		push @lines, "$line\n";
	}
	closedir $dh;
	
	@lines = map { $_->[0] }
		sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] }
			map { [$_, split /<>/] } @lines;
	
	$layout = 1;
	$mes .= "IP���ڽ�AνĖ��A��׳�ނ������lؽ�<br>";
	$mes .= "�ȉ��̏󋵂ɂ��ؽĂɍڂ邱�Ƃ�����̂ŁA����ؽĂɕ\�����ꂽ�l�����d�Ɗ֘A�t����̂͒���!!<br>";
	$mes .= "���Ǘ������������Ă�����ڲ԰�́A����ڲ԰��۸޲݂��邱�Ƃ��ł���<br>";
	$mes .= "�������n���w�Z�Ȃǂ̌����{�݂���۸޲݂��Ă���ꍇ<br>";
	$mes .= "���g����ڲ԰�̏ꍇ�͂�������������\\��������̂ŗv�m�F!(�g�т̔��ʂ�νĖ��Ŋm�F)<br>";
	$mes .= "�����炳�܂ȑ��d�ȊO�́A�Ƃ肠�����{�l�Ɋm�F���Ă݂邱��<br>";

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="violator" value="" checked>��߂�|;
	$mes .= $is_mobile ? qq|<hr>���O/������/IP���ڽ/νĖ�/��׳��/�X�V��<br>|
		: qq|<table class="table1"><tr><th>���O</th><th>������</th><th>IP���ڽ</th><th>νĖ�</th><th>�X�V��<br></th></tr>|;
	
	my $b_line  = '';
	my $b_addr  = '';
	my $b_host  = '';
	my $b_agent = '';
	my $is_same = 0;
	for my $line (@lines) {
		my($sid, $sname, $sshogo, $scountry, $saddr, $shost, $sagent, $sldate) = split /<>/, $line;
		if ($saddr eq $b_addr && $shost eq $b_host && $sagent eq $b_agent
			|| ($sagent eq $b_agent && ($sagent =~ /DoCoMo/ || $sagent =~ /KDDI|UP\.Browser/ || $sagent =~ /J-PHONE|Vodafone|SoftBank/)) ) {

				unless ($is_same) {
					$is_same = 1;
					my($bid, $bname, $bshogo, $bcountry, $baddr, $bhost, $bagent, $bldate) = split /<>/, $b_line;
					$bname .= "[$bshogo]" if $bshogo;
					$mes .= $is_mobile ? qq|<hr><input type="radio" name="violator" value="$bname">$bname/<font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]/$baddr/$bhost/$bldate<br>|
						: qq|<tr><td><input type="radio" name="violator" value="$bname">$bname</td><td><font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]</font></td><td>$baddr</td><td>$bhost</td><td>$bldate<br></td></tr>|;
				}
					$sname .= "[$sshogo]" if $sshogo;
					$mes .= $is_mobile ? qq|<hr><input type="radio" name="violator" value="$sname">$sname/<font color="$cs{color}[$scountry]">$cs{name}[$scountry]/$saddr/$shost/$sldate<br>|
						: qq|<tr><td><input type="radio" name="violator" value="$sname">$sname</td><td><font color="$cs{color}[$scountry]">$cs{name}[$scountry]</font></td><td>$saddr</td><td>$shost</td><td>$sldate<br></td></tr>|;
		}
		else {
			$b_line  = $line;
			$b_addr  = $saddr;
			$b_host  = $shost;
			$b_agent = $sagent;
			$is_same = 0;
		}
	}
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���Y�Ґ\\��" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_510 {
	if ($in{violator}) {
		$m{tp} = 300;
		&{ 'tp_'.$m{tp} };
	}
	else {
		&begin;
	}
}



1; # �폜�s��
