my $u = &union($m{country}, $y{country});
#================================================
# �O�� Created by Merino
#================================================

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
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
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
		$mes .= "�����ƊO�������܂�($GWT��)<br>�����s���܂���?<br>";
	}

	my @menus = ('��߂�','�F�D���','��틦��');

	if (&is_daihyo) {
		push @menus, '���z��','���퓯��','�����j��';
		push @menus, '�H���A��','������','���m�h��' if $union;
	}
	&menu(@menus);
}

sub tp_1 {
	return if &is_ng_cmd(1..8);

	if    ($cmd eq '1') { $mes .= '�F�D�������їF�D�x���グ�܂�<br>'; }
	elsif ($cmd eq '2') {
		if (($w{world} eq '8' || ($w{world} eq '19' && $w{world_sub} eq '8'))) {
#		if ($w{world} eq '9') {
			$mes .= "���E���$world_states[$w{world}]�Ȃ̂ŁA���������Ԃ��Ƃ͂ł��܂���<br>";
			$m{tp} = 2;
			&begin;
			return;
		}
		$mes .= '���������ь���Ԃ��������܂�<br>';
	}
	elsif ( &is_daihyo ) {
		if    ($cmd eq '3') { $mes .= '���z�������A����Ԃɂ��܂�<br>'; }
		elsif ($cmd eq '4') { $mes .= '���퓯�������т܂�<br>'; }
		elsif ($cmd eq '5') { $mes .= '������j�����܂�<br>'; }

		elsif ($cmd eq '6') { $mes .= "������$cs{name}[$union]�Ɏ�����$e2j{food}��A�����܂�<br>"; }
		elsif ($cmd eq '7') { $mes .= "������$cs{name}[$union]�Ɏ�����$e2j{money}����t���܂�<br>"; }
		elsif ($cmd eq '8') { $mes .= "������$cs{name}[$union]�Ɏ����̕��m��h�����܂�<br>"; }
	}
	else {
		$mes .= "���̺���ނ́A���̑�\\�҂����ł��܂���<br>";
		$m{tp} = 2;
		&begin;
		return;
	}

	$m{tp} = $cmd * 100;

	if ($cmd >= 6) {
		$mes .= qq|�ǂꂭ�炢����܂���?<br>|;
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="text" name="value" value="0" class="text_box1" style="text-align: right">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="����"></p></form>|;
		&n_menu;
	}
	else {
		$mes .= '�ǂ̍��Ɍ������܂���?<br>';
		&menu('��߂�', @countries);
	}
}


#=================================================
# �O���
#=================================================
sub tp_100 { &exe1("�F�D����������") }
sub tp_200 { &exe1("������������") }
sub tp_300 { &exe1("���z��������") }
sub tp_400 { &exe1("������������") }
sub tp_500 { &exe1("������j������") }
sub exe1 {
	return if &is_ng_cmd(1..$w{country});

	if ($m{tp} >= 300 && !&is_daihyo) {
		$mes .= "���̺���ނ́A���̑�\\�҂����ł��܂���<br>";
		&begin;
	}
	elsif ($m{country} eq $cmd) {
		$mes .= '�����͑I�ׂ܂���<br>';
		&begin;
	}
	else {
		$m{tp} += 10;
		$y{country} = $cmd;
		$mes .= "$_[0]$cs{name}[$y{country}]�Ɍ������܂���<br>";
		$mes .= "���ʂ�$GWT����ł�<br>";
		&wait;
	}
}


#=================================================
# �F�D���
#=================================================
sub tp_110 {
	if ( rand($w{"f_$u"}) > 5 || rand(4) > 1  ) {
		&mes_and_world_news("$c_y�ƗF�D�������т܂���");
		$w{"f_$u"} += int( rand(5)+7 );
		$w{"f_$u"} = 100 if $w{"f_$u"} > 100;
		&success;
	}
	else {
		$mes .= "$c_y�Ƃ̗F�D���Ɏ��s���܂���<br>";
		&failed;
	}
}
#=================================================
# ���
#=================================================
sub tp_210 {
#	if ($w{world} eq '9') {
	if (($w{world} eq '8' || ($w{world} eq '19' && $w{world_sub} eq '8'))) {
		$mes .= "���E���$world_states[$w{world}]�Ȃ̂ŁA��킷�邱�Ƃ��ł��܂���<br>";
		&failed;
	}
	elsif ($w{"p_$u"} eq '2') {
		&mes_and_world_news("<b>$c_y�ƒ��������т܂���</b>");
		$w{"f_$u"} = int( rand(20)+40 );
		$w{"p_$u"} = 0;

		&success;
	}
	else {
		$mes .= "$c_y�Ƃ̒����Ɏ��s���܂���<br>";
		&failed;
	}
}
#=================================================
# ���z��
#=================================================
sub tp_310 {
	if ($w{"p_$u"} eq '1') {
		$mes .= "�܂��A$c_y�Ƃ̓�����j�����Ă�������<br>";
		&failed;
	}
	elsif ($cs{is_die}[$m{country}]) {
		$mes .= "�ŖS���Ă��鍑�́A���z�������邱�Ƃ��ł��܂���<br>";
		&failed;
	}
	elsif ($cs{is_die}[$y{country}]) {
		$mes .= "�ŖS���Ă��鍑�ɐ��z�������邱�Ƃ͂ł��܂���<br>";
		&failed;
	}
	else {
		&mes_and_world_news("<b>$c_y�ɐ��z�������܂���</b>");
		$w{"p_$u"} = 2;
		$w{"f_$u"} = int( rand(20) );
		&success;
	}
}
#=================================================
# ����
#=================================================
sub tp_410 {
	if ( $w{world} eq '8'|| $w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '8' || $w{world_sub} eq '13')) || $w{world} == $#world_states-5 || $w{world} == $#world_states-2 || $w{world} == $#world_states-3 ) {
	#if ( $w{world} eq '9' || $w{world} eq '14' || $w{world} == $#world_states-5 || $w{world} == $#world_states-2 || $w{world} == $#world_states-3 ) {
		$mes .= "���E���$world_states[$w{world}]�Ȃ̂ŁA�������邱�Ƃ��ł��܂���<br>";
		&failed;
	}
	elsif ( !$union && $w{"p_$u"} eq '0' && $w{"f_$u"} >= 80 && !&is_other_union($y{country}) ) {
		&mes_and_world_news("<b>$c_y�Ƌ��퓯�������т܂���</b>");
		$w{"p_$u"} = 1;
		&success;
	}
	else {
		$mes .= "$c_y�Ƃ̓����Ɏ��s���܂���<br>";
		&failed;
	}
}
#=================================================
# �����j��
#=================================================
sub tp_510 {
	if (($w{world} eq '6' || ($w{world} eq '19' && $w{world_sub} eq '6'))) {
#	if ($w{world} eq '7') {
		$mes .= "���E���$world_states[$w{world}]�Ȃ̂ŁA������j�����邱�Ƃ��ł��܂���<br>";
		&failed;
	}
	elsif ( $union && $w{"p_$u"} eq '1') {
		&mes_and_world_news("<b>$c_y�Ƃ̓�����j�����܂���</b>");
		$w{"p_$u"} = 0;
		&success;
	}
	else {
		$mes .= "$c_y�Ƃ͓�����g��ł��܂���<br>";
		&failed;
	}
}


#=================================================
# �������ɕ������
#=================================================
sub tp_600 { &exe2('food',    '�H��') }
sub tp_700 { &exe2('money',   '����') }
sub tp_800 { &exe2('soldier', '���m') }
sub exe2 {
	if ($in{value} > 0 && $in{value} !~ /[^0-9]/) {
		if (!$union) {
			$mes .= '�������Ă܂���<br>';
			&begin;
		}
		elsif ($cs{$_[0]}[$m{country}] <= $in{value}) {
			$mes .= "$c_m��$_[1]���Ȃ��Ȃ��Ă��܂��܂�<br>";
			&begin;
		}
		elsif ($in{value} < 10000) {
			$mes .= "�����̎x���͍Œ�ł� 10000 �ȏ�ɂ���K�v������܂�<br>";
			&begin;
		}
		else {
			$cs{$_[0]}[$m{country}] -= $in{value};
			&write_cs;

			$m{value} = $in{value};

			$m{tp} += 10;
			$y{country} = $union;

			&mes_and_send_news("��������$cs{name}[$union]��$_[1]�� $m{value} ����܂���");
			$mes .= "$GWT���ɓ�������\\��ł�<br>";
			&wait;
		}
	}
	else {
		$mes .= "��߂܂���<br>";
		&begin;
	}
}
sub tp_610 { # ������
	if ($union) {
		$cs{food}[$union] += $m{value};
		&exe3('�H��');
	}
	else {
		$mes .= "���̍��Ɠ�����g��ł��܂���<br>";
		&failed;
	}
}
sub tp_710 { # ���Ɨ\�Z
	if ($union) {
		$cs{money}[$union] += $m{value};
		&exe3('����');
	}
	else {
		$mes .= "���̍��Ɠ�����g��ł��܂���<br>";
		&failed;
	}
}
sub tp_810 { # ���m
	if ($union) {
		$cs{soldier}[$union] += $m{value};
		&exe3('���m');
	}
	else {
		$mes .= "���̍��Ɠ�����g��ł��܂���<br>";
		&failed;
	}
}
sub exe3 {
	my $name = shift;

	$w{"f_$u"} += int( rand(10)+20 );
	$w{"f_$u"} = 100 if $w{"f_$u"} > 100;
	&write_cs;
	&write_send_news("$c_m��$m{name}�̗A����������������$cs{name}[$union]�ɓ������A$m{value} ��$name�������ɓ͂����܂���");
	$mes .= "�A����������������$cs{name}[$union]�ɓ������A$m{value} ��$name�������ɓ͂����܂���<br>";
	&success;
}

#=================================================
# ����
#=================================================
sub success {
	$m{act} += 1;
	&c_up('gai_c');

	my $v = int(rand(11)+10);
	$v = &use_pet('promise', $v);

	$m{exp} += $v;
	$m{egg_c} += int(rand(6)+5) if $m{egg};
	$m{rank_exp} += int(rand(6)+4);

	$mes .= "$m{name}�ɑ΂���]�����オ��܂���<br>";
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";

	&daihyo_c_up('pro_c'); # ��\�n���x

	&refresh;
	&n_menu;
	&write_cs;
}
#=================================================
# ���s
#=================================================
sub failed {
	$m{act} += 1;

	my $v = int(rand(11)+5);
	$m{exp} += $v;
	$m{egg_c} += int(rand(6)+5) if $m{egg};
	$m{rank_exp} -= int(rand(3)+2);

	$mes .= "���Ɏ��s�������߁A$m{name}�ɑ΂���]����������܂���<br>";
	$mes .= "$v ��$e2j{exp}����ɓ���܂���<br>";

	&refresh;
	&n_menu;
}


#=================================================
# �����Ɠ���������ł��邩
#=================================================
sub is_other_union {
	my $country = shift;

	for my $i (1 .. $w{country}) {
		next if $country eq $i;
		my $c_c = &union($country, $i);
		return 1 if $w{ "p_$c_c" } eq '1';
	}
	return 0;
}




1; # �폜�s��