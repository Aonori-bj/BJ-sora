sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
#=================================================
# �S�� Created by Merino
#=================================================

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{act} >= 100) {
		$mes .= "$m{name}�͏����x�����Ƃ邱�Ƃɂ���<br>���ɍs���ł���̂� $GWT����ł�";
		$m{act} = 0;
		&wait;
		return 0;
	}
	return 1;
}

#=================================================
# �S���ƭ�
#=================================================
sub tp_100 {
	if (-f "$userdir/$id/rescue_flag.cgi" # ڽ����׸ނ����邩
		|| $time < $w{reset_time} # �I�풆
		|| !defined $cs{name}[$y{country}]) { # ���폜

			unlink "$userdir/$id/rescue_flag.cgi" or &error("$userdir/$id/rescue_flag.cgi�폜���s") if -f "$userdir/$id/rescue_flag.cgi";
			$mes .= "���Ԃɋ~�o����܂���<br>";
			
			&refresh;
			&n_menu;
			&escape;
	}
	else {
		$mes .= "$m{name}��$c_y�̘S���ɕ����߂��܂���<br>";
		$mes .= '�ǂ����܂���?<br>';
		&menu('������҂�','�E�������݂�','�Q�Ԃ�');
		$m{tp} += 10;
	}
}

sub tp_110 {
	# �E�o
	if ($cmd eq '1') {
		$mes .= "$m{name}�͒E�����ł��������F�X�Ǝ����Ă݂�<br>";
		if ( int(rand(4)) == 0 ) { # ����
			$mes .= '�Ȃ�Ƃ��S������E�o���邱�Ƃɐ�������!<br>';
			$m{tp} += 10;
		}
		elsif ( $m{cha} > rand(1000)+400 ) {
			$mes .= '�Ŏ��U�f���ĘS������E�o���邱�Ƃɐ�������!<br>';
			$m{tp} += 10;
		}
		else {
			$mes .= '�ǂ���疳���Ȃ悤���c<br>';
			$m{act} += 10;
			$m{tp} = 100;
		}
		&n_menu;
	}
	# �Q�Ԃ�
	elsif ($cmd eq '2') {
		$mes .= "�Q�Ԃ�ƊK���Ƒ�\\���߲�Ă�������A�葱����$GWT��������܂�<br>";
		$mes .= "$c_m �𗠐؂�A$c_y�ɐQ�Ԃ�܂���?<br>";
		&menu('��߂�','�Q�Ԃ�');
		$m{tp} = 200;
	}
	else {
		$m{tp} = 100;
		&tp_100;
	}
}

#=================================================
# �S���E�o
#=================================================
sub tp_120 {
	$m{tp} += 10;
	$m{value} = int(rand(40))+40;
	$m{turn}  = int(rand(4)+4);
	$mes .= "�S������E�o���܂���! <br>";
	$mes .= "$c_y�E�o�܂Ŏc��y$m{turn}��݁z�G���̋C�z�y$m{value}%�z<br>";
	$mes .= '�ǂ���ɐi�݂܂���?<br>';
	&menu('��','�E');
	$m{value} += int( 10 - rand(21) ); # �}10
	$m{value} = int(rand(30)) if $m{value} < 10;
}

#=================================================
# ٰ���ƭ� �߂܂邩�E�o����܂�
#=================================================
sub loop_menu {
	$mes .= "$c_y�E�o�܂Ŏc��y$m{turn}��݁z�G���̋C�z�y$m{value}%�z<br>";
	$mes .= '�ǂ���ɐi�݂܂���?<br>';
	int(rand(3)) == 0 ? &menu('��','�E') : &menu('��','���i','�E');
}
sub tp_130 {
	# ������
	if ( $m{value} > rand(110)+30 ) {
		$mes .= '�G���Ɍ������Ă��܂���!!<br>';
		$m{tp} += 10;
		&n_menu;
	}
	# �E�o����
	elsif (--$m{turn} <= 0) {
		&mes_and_world_news("������$c_y����̎��͒E�o�ɐ������܂���!");
		&refresh;
		&n_menu;
		&escape;
	}
	else {
		&loop_menu;
	}
	$m{value} += int( 10 - rand(21) ); # �}10
	$m{value} = int(rand(30)) if $m{value} < 10;
}
# ����������:�����؂�� or �߂܂�
sub tp_140 {
	if ( rand(6) < 1 ) {
		$mes .= '�Ȃ�Ƃ��G����U��؂�܂���<br>';
		$m{tp} -= 10;
		&loop_menu;
	}
	else {
		$mes .= '�G���Ɉ͂܂�S���ւƘA��߂���܂���<br>';
		$m{tp} = 100;
		$m{act} += 20;
		&n_menu;
	}
}


#=================================================
# �Q�Ԃ�
#=================================================
sub tp_200 {
	if ($cmd eq '1') {
		if ($cs{ceo}[$m{country}] eq $m{name}) {
			$mes .= "$e2j{ceo}�͐Q�Ԃ邱�Ƃ��ł��܂���<br>";
			$m{tp} = 100;
			&n_menu;
		}
#		if ($m{name} eq $m{vote} || &is_daihyo) {
#			$mes .= "���̑�\\�҂�$e2j{ceo}�ɗ���₵�Ă���ꍇ�͐Q�Ԃ邱�Ƃ��ł��܂���<br>";
#			$m{tp} = 100;
#			&n_menu;
#		}
		elsif ($m{shogo} eq $shogos[1][0]) {
			$mes .= "$shogos[1][0]�͐Q�Ԃ邱�Ƃ��ł��܂���<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($cs{member}[$y{country}] >= $cs{capacity}[$y{country}]) {
			$mes .= "$c_y�͒���������ς��ł�<br>";
			$m{tp} = 100;
			&n_menu;
		}
		else {
			require './lib/move_player.cgi';
			&move_player($m{name}, $m{country}, $y{country});
			&escape;
			
			$m{shogo} = $shogos[1][0];

			$m{rank} -= $m{rank} > 10 ? 2 : 1;
			$m{rank} = 1 if $m{rank} < 1;
			$mes .= "�K����$ranks[$m{rank}]�ɂȂ�܂���<br>";

			&mes_and_world_news("$cs{name}[$y{country}]�ɐQ�Ԃ�܂���", 1);
			$m{country} = $y{country};
			$m{vote} = '';
			
			# ��\�߲��Down
			for my $key (qw/war dom mil pro/) {
				$m{$key.'_c'} = int($m{$key.'_c'} * 0.4);
			}

			&refresh;
			&wait;
			&n_menu;
		}
	}
	else {
		$mes .= '��߂܂���<br>';
		$m{tp} = 100;
		&n_menu;
	}
}

#=================================================
# �S��̧�ق��玩���̖��O������
#=================================================
sub escape {
	my @lines = ();
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country) = split /<>/, $line;
		push @lines, $line unless $name eq $m{name};
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # �폜�s��
