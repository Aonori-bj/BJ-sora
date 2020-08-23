require "$datadir/hunting.cgi";
#=================================================
# ���� Created by Merino
#=================================================

# ���яE���m��(����1)
my $get_item_par = 200;

my $new_sedai = 5;

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "��������̂�$e2j{hp}�����Ȃ����܂�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	$m{turn} = 0;
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= '�����𓢔����ɍs���܂�<br>';
	$mes .= '�ǂ��Ɍ������܂���?<br>';

	my $m_st = &m_st;
	my @menus = ('��߂�');
	for my $i (0..$#places) {
		next if $i == 0 && $m{sedai} > $new_sedai;
		push @menus, "$places[$i][2]" if $m_st * 2 >= $places[$i][1] || $pets[$m{pet}][2] eq 'hunt_lv';
	}

	&menu(@menus);
}
sub tp_1 {
	if ($cmd) {
		$m{stock} = $cmd-1;
		&_get_hunt_you_data;
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}

#=================================================
# Get ����f�[�^
#=================================================
sub _get_hunt_you_data {
	my $line = '';
	open my $fh, "< $logdir/monster/$m{stock}.cgi" or &error("$logdir/monster/$m{stock}.cgi̧�ق�����܂���");
	rand($.) < 1 and $line = $_ while <$fh>;
	close $fh;

	my @datas = split /<>/, $line;
	my $i = 0;
	for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon/) {
		$y{$k} = $datas[$i];
		++$i;
	}
	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};
	$y{icon} = $default_icon unless -f "$icondir/$y{icon}";

	if ( rand($m{cha}) < rand($y{cha}) ) {
		$m{tp} = 200;
		$mes .= "$y{name} ���P���������Ă��܂���<br>";
		&n_menu;
	}
	else {
		$m{tp} = 100;
		$mes .= "$y{name} �����܂�<br>";
		&menu('�키','������');
	}
}

#=================================================
# �키 or ������
#=================================================
sub tp_100 {
	if ($cmd eq '0') {
		$mes .= "$y{name} �Ɛ킢�܂�<br>";
		$m{tp} = 200;
		&n_menu;
	}
	elsif ( rand($m{ag}) > rand($y{ag}) ) {
		$mes .= '�����܂���<br>';
		&begin;
	}
	else {
		$mes .= '�������܂���ł����B�퓬�Ԑ��ɓ���܂�<br>';
		$m{tp} = 200;
		&n_menu;
	}
}

#=================================================
# �퓬
#=================================================
sub tp_200 {
	require './lib/battle.cgi';

	# ����
	if ($m{hp} <= 0) {
		$m{act} += 12;
		&refresh;
		&n_menu;
	}
	# ����
	elsif ($y{hp} <= 0) {
		# İ�ٽð������������҂��ƌo���l���Ȃ�
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = $st_lv eq '2' ? int( rand(10) + 10)
			  : $st_lv eq '0' ? int( rand(3)  + 1)
			  :                 int( rand(5)  + 5)
			  ;
		$v = int( rand(10) + 10) if $m{stock} == 0;
		my $vv = int( ($m{stock}+1) * 70 + $y_st * 0.1);

		&c_up('tou_c');
		$v  = &use_pet('hunting', $v);
		$vv = &use_pet('hunt_money', $vv);
		$m{exp} += $v;
		$m{act} += 6;
		$m{egg_c} += int(rand($m{stock})+1+$m{stock}) if $m{egg};
		$m{money} += $vv;
		$mes .= "$v ��$e2j{exp}�� $vv G����ɓ���܂���<br>";

		# ���ѹޯ�(�����߯ĐE�Ƃ��Ǝ擾��up)
		$get_item_par *= 0.4 if $pets[$m{pet}][2] eq 'get_item' || $jobs[$m{job}][1] eq '�V�ѐl';
		&_get_item if int(rand($get_item_par)) == 0;

		$mes .= '�����𑱂��܂���?<br>';
		&menu('������','��߂�');
		$m{tp} += 10;
	}
}

#=================================================
# �p�� or ��߂�
#=================================================
sub tp_210 {
	if ($cmd eq '0') {
		&_get_hunt_you_data;
	}
	else {
		$mes .= '�������I�����܂�<br>';
		&refresh;
		&n_menu;
	}
}

#=================================================
# ����(�Ϻ�)�E������
#=================================================
sub _get_item {
	my @egg_nos = @{ $places[$m{stock}][3] };
	my $egg_no = $egg_nos[int(rand(@egg_nos))];

	$mes .= qq|<font color="#FFCC00">$eggs[$egg_no][1]���E���܂���!</font><br>|;
	if ($m{is_full}) {
		$mes .= "�������A�a���菊�������ς��Ȃ̂�$eggs[$egg_no][1]��������߂܂���<br>";
	}
	else {
		$mes .="$eggs[$egg_no][1]��a���菊�ɑ���܂���!<br>";
		&send_item($m{name}, 2, $egg_no);
	}
}



1; # �폜�s��
