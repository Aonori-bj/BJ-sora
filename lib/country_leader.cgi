my $this_file = "$logdir/$m{country}/leader.cgi";
#=================================================
# ��\���[ Created by Merino
#=================================================

# ��\�҂ɂȂ�̂ɕK�v�ȕ[
my $need_ceo_point = int($cs{member}[$m{country}] * 0.1)+2;

# �����ɕK�v�Ȕ�p
my $need_money = 50000;


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
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ����s���܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "$c_m��$e2j{ceo}�����肵�܂�<br>";
		$mes .= "$e2j{ceo}�ɂȂ�ɂ͍Œ�ł�$need_ceo_point�[�K�v�ł�<br>";
	}
	&menu('��߂�', "$e2j{ceo}��I��", '����₷��', '���C����');
}

sub tp_1 {
	return if &is_ng_cmd(1..3);

	$m{tp} = $cmd * 100;
	&{'tp_' . $m{tp} };
}

#=================================================
# �x���E�s�x���̑I��
#=================================================
sub tp_100 {
	if (!-s $this_file) {
		$mes .= '�����҂����܂���<br>';
		$m{vote} = '';
		&begin;
		return;
	}

	my $sub_mes = '';
	my $is_find = 0;
	open my $fh, "< $this_file" or &error('�����[�_�[�t�@�C�����ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		$is_find = 1 if $name eq $m{vote};
		$sub_mes .= qq|<input type="radio" name="vote" value="$name">$name�F$vote�[<br>|;
	}
	close $fh;

	$mes .= '�N���x�����܂���?<br>';

	$mes .= qq|$m{vote} ���x�����Ă��܂�<br>| if $is_find;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="vote" value="$m{vote}" checked>���̂܂�<br>| if $is_find;
	$mes .= qq|<input type="radio" name="vote" value="">�x�����Ȃ�<hr>|;
	$mes .= qq|$sub_mes|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�� ��" class="button1"></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	if ($m{vote} eq $m{name}) {
		$mes .= '�����҂͓��[�ł��܂���<br>';
		&begin;
		return;
	}
	# ���̂܂�
	elsif ($m{vote} eq $in{vote}) {
		&begin;
		return;
	}

	my @lines = ();
	open my $fh, "+< $this_file" or &error('�����[�_�[�t�@�C�����J���܂���');
	eval { flock $fh, 2 };
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;

		$vote-- if $m{vote} eq $name && ($in{vote} eq '' || $in{vote} ne $m{vote}); # �N�����x�����ˑ��̐l���x�� or �x�����Ȃ�
		$vote++ if $name eq $in{vote}; # �x��

		push @lines, "$name<>$vote<>\n" if $vote > 0; # 0�[�͏�����
	}
	# �[���������ɕ��ёւ�
	@lines = map { $_->[0] } sort { $b->[2] <=> $a->[2]  } map { [$_, split/<>/] } @lines;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	# ��ԕ[�������l�ƍ��̑�\���Ⴄ�ꍇ�̏���
	my($top_name, $top_vote) =  split /<>/, $lines[0];
	if ($cs{ceo}[$m{country}] ne $top_name && $top_vote >= $need_ceo_point) {
		$cs{ceo}[$m{country}] = $top_name;
		&write_world_news("<b>$top_name��$c_m�̐V����$e2j{ceo}�ɂȂ�܂���</b>", 1, $top_name);

		# ���̑�\�ɂȂ��Ă�����O��
		for my $k (qw/war pro dom mil/) {
			if ($cs{$k}[$m{country}] eq $top_name) {
				$cs{$k}[$m{country}] = '';
				$cs{$k.'_c'}[$m{country}] = 0;
			}
		}
		&write_cs;
	}
	# �N�傪��x�I�΂ꂽ���ǎx�����Ȃ����N��̕[����\�ɕK�v�ȕ[��艺��������
	elsif ($cs{ceo}[$m{country}] && $top_vote < $need_ceo_point) {
		$cs{ceo}[$m{country}] = '';
		&write_cs;
		&write_world_news("<b>$top_name��$c_m��$e2j{ceo}����͂�����܂���</b>");
	}

	$m{vote} = $in{vote};
	$mes .= $in{vote} ? "$m{vote}���x�����܂�<br>" : '�x������̂���߂܂���<br>';

	&begin;
}

#=================================================
# �����
#=================================================
sub tp_200 {
	$mes .= "$c_m��$e2j{ceo}�ɗ���₵�܂���?<br>";
	$mes .= "����₷��ɂ� $need_money G�K�v�ł�<br>";
	&menu('��߂�','����₷��');
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1);

	my $is_find = 0;
	my @lines = ();
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		$is_find = 1 if $name eq $m{name};
		push @lines, $line;
	}
	close $fh;

	if ($is_find) {
		$mes .= '���łɗ����҂ɂȂ��Ă��܂�<br>';
		&begin;
		return;
	}
	#elsif ($cs{old_ceo}[$m{country}] eq $m{name}) {
		#$mes .= "�O��$e2j{ceo}�������l�͗���₷�邱�Ƃ��ł��܂���<br>";
		#&begin;
		#return;
	#}
	elsif ($m{money} < $need_money) {
		$mes .= '����₷��̂ɂ���������܂���<br>';
		&begin;
		return;
	}
	elsif ($m{vote}) {
		$mes .= "����₷��ꍇ�́A$e2j{ceo}��I�ԂŎx�����Ȃ���I�����Ă�������<br>";
		&begin;
		return;
	}

	open my $fh, ">> $this_file" or &error("$this_filȩ�ق��J���܂���");
	print $fh "$m{name}<>1<>\n";
	close $fh;

	$mes .= "$e2j{ceo}�ɗ���₵�܂���<br>";
	&write_world_news("<b>$m{name}��$c_m��$e2j{ceo}�ɗ���₵�܂���</b>",1);
	$m{vote} = $m{name};
	$m{money} -= $need_money;
	&begin;
}

#=================================================
# ���C
#=================================================
sub tp_300 {
	$mes .= "$c_m��$e2j{ceo}�̗���₩�玫�C���܂���?<br>";
	&menu('��߂�','���C����');
	$m{tp} += 10;
}
sub tp_310 {
	return if &is_ng_cmd(1);

	unless ($m{vote} eq $m{name}) {
		$mes .= '�����҂łȂ��̂Ŏ��C�͂ł��܂���<br>';
		&begin;
		return;
	}

	my @lines = ();
	open my $fh, "+< $this_file" or &error('�����[�_�[�t�@�C�����J���܂���');
	eval { flock $fh, 2 };
	while (my $line = <$fh>) {
		my($name, $vote) = split /<>/, $line;
		next if $m{name} eq $name;
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	$mes .= '����₩�玫�C���܂���<br>';
	$m{vote} = '';

	# ��\�҂����C
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		$cs{ceo}[$m{country}] = '';
		&mes_and_world_news("<b>$e2j{ceo}�����C���܂���</b>",1);
		&write_cs;
	}

	&begin;
}



1; # �폜�s��