$mes .= qq|��� $m{coin} ��<br>| if $is_mobile;
#================================================
# ���� Created by Merino
#================================================
# @m�cmark @o�cozz �̈Ӗ�

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�̕��͏o����֎~�ł�<br>";
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
		$mes .= '���ɉ���������Ⴄ?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "���������`�����ެݼެݗV��ł����Ă�<br>";
	}
	
	&menu('��߂�','$1�ۯ�','$10�ۯ�','$100�ۯ�','ʲ۳','�ޯ���');
}

sub tp_1 {
	return if &is_ng_cmd(1..5);
	
	$m{tp} = $cmd * 100;
	&menu('Play!', '��߂�');
	$m{stock} = 0;
	$m{value} = '';

	if    ($cmd eq '1') { $mes .= '������$1�ۯĂł�<br>'; }
	elsif ($cmd eq '2') { $mes .= '������$10�ۯĂł�<br>'; }
	elsif ($cmd eq '3') { $mes .= '������$100�ۯĂł�<br>'; }
	elsif ($cmd eq '4') {
		$mes .= 'ʲ۳�ւ悤����!<br>';
		$mes .= '�O�̶��ނ��傫�������������𓖂Ă�ްтł�<br>';
		$mes .= '�������ނ̏ꍇ�͕����ł��̂Œ��ӂ��Ă���������<br>';
		$mes .= '���10��݂ł�<br>';
	}
	elsif ($cmd eq '5') { # �ޯ���
		$mes .= '�ޯ��قւ悤����!<br>';
		$mes .= '3���̶��ނ̒�����A�ި�װ�����������ނƓ������ނ������Ώ����ł�<br>';
		$mes .= '���10��݂ł�<br>';
	}
	else {
		&refresh;
		&n_menu;
	}
}


#=================================================
# �ۯ�
#=================================================
sub tp_100 { &_slot(1) }
sub tp_200 { &_slot(10) }
sub tp_300 { &_slot(100) }
sub _slot {
	my $bet = shift;
	
	if ($cmd eq '0') {
		if ($m{coin} >= $bet) {
			my @m = ('��','��','��','��','�V');
			my @o = (5,10, 15,  20,  30,  50); # ���� ��ԍ�����ذ��2���낢�̂Ƃ�
			my @s = ();
			$s[$_] = int(rand(@m)) for (0 .. 2);
			$mes .= "[\$$bet�ۯ�]<br>";
			$mes .= "<p>�y$m[$s[0]]�z�y$m[$s[1]]�z�y$m[$s[2]]�z</p>";
			$m{coin} -= $bet;
			
			if ($s[0] == $s[1]) { # 1�ڂ�2��
				if ($s[1] == $s[2]) { # 2�ڂ�3��
					my $v = $bet * $o[$s[0]+1]; # +1 = ��ذ2���낢
					$m{coin} += $v;
					$mes .= "�Ȃ��!! $m[$s[0]] ��3���낢�܂���!!<br>";
					$mes .= '���߂łƂ��������܂�!!<br>';
					$mes .= "***** ��� $v �� GET !! *****<br>";
					&c_up('cas_c');
					&use_pet('casino');
				}
				elsif ($s[0] == 0) { # ��ذ�̂�1�ڂ�2�ڂ����낦�΂悢
					my $v = $bet * $o[0];
					$m{coin} += $v;
					$mes .= '��ذ��2���낢�܂�����<br>';
					$mes .= "��� $v ��Up��<br>";
					&c_up('cas_c');
					&use_pet('casino');
				}
				else {
					$mes .= '<p>ʽ��</p>';
					$m{act} += 1;
				}
			}
			else {
				$mes .= '<p>ʽ��</p>';
				$m{act} += 1;
			}
			$mes .= '������x���܂���?';
			&menu('Play!', '��߂�');
		}
		else {
			$mes .= '��݂�����܂���<br>';
			&begin;
		}
	}
	else {
		&begin;
	}
}

#=================================================
# ʲ۳
#=================================================
sub tp_400 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # �Ⴂ��
			$m{value} = int(rand(@m)) if $m{value} eq '';
			$mes .= "�y$m[$m{value}]�z<br>���̶��ނ� High(����)? or Low(�Ⴂ)?";
			&menu('High!(����)','Low!(�Ⴂ)');
			
			$m{tp} = 410;
		}
		else {
			$mes .= '��݂�����܂���<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} ������ꍇ�͏���->��߂�̑I��
		$mes .= "��� $m{stock} ������ɓ���܂���!<br>";
		$m{coin} += $m{stock};
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_410 {
	my $stock_old = $m{value};
	my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # �Ⴂ��
	
	$m{value} = int(rand(@m));
	$mes .= "�y$m[$stock_old]�z-> �y$m[$m{value}]�z<br>";

	if (   ($cmd eq '0' && $m{value} > $stock_old)     # �����I���ō�����
		|| ($cmd eq '1' && $m{value} < $stock_old) ) { # �Ⴂ�I���ŒႢ��
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 2;
			$mes .= '���߂łƂ��������܂�!<br>';
			$mes .= "$m{stock}��� Get!<br>";
			$mes .= '��ɓ��ꂽ��݂����̂܂܎��ւƓq���邱�Ƃ��ł��܂�<br>';
			&menu('���킷��','��߂�');

			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # ����
		$m{coin} -= 10;
		$m{stock} = 0;
		$m{value} = '';
		$mes .= '<p>�c�O�ł����ˁB������x���܂���?</p>';
		&menu('Play!','��߂�');
		$m{act} += 6;
	}
	$m{tp} = 400;
}


#=================================================
# �ޯ���
#=================================================
sub tp_500 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('��','��','��');
			$m{value} = int(rand(@m));
			$mes .= "�ި�װ�̶��ށy$m[$m{value}]�z<br>";
			$mes .= '<p>�y���z�y���z�y���z</p><p>�ǂ̶��ނ�I�т܂���?</p>';
	
			&menu('��','�^��','�E');
			$m{tp} = 510;
		}
		else {
			$mes .= '��݂�����܂���<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} ������ꍇ�͏���->��߂�̑I��
		$mes .= "��� $m{stock} ������ɓ���܂���<br>";
		$m{coin} += $m{stock};
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_510 {
	my @m = ('��','��','��');
	my @s = (0,1,2);
	my $a = int(rand(@m));
	
	$mes .= "�ި�װ�̶��ށy$m[$m{value}]�z<br>";
	$mes .= "<p>�y$m[$s[$a]]�z�y$m[$s[$a-1]]�z�y$m[$s[$a-2]]�z</p>";
	
	if (   ($cmd eq '0' && $m[$m{value}] eq $m[$s[$a]])       # ���I��
		|| ($cmd eq '1' && $m[$m{value}] eq $m[$s[$a-1]])     # �^�񒆑I��
		|| ($cmd eq '2' && $m[$m{value}] eq $m[$s[$a-2]]) ) { # �E�I��
		
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 6;
			$mes .= '���߂łƂ��������܂�!<br>';
			$mes .= "��� $m{stock} �� Get!<br>";
			$mes .= '��ɓ��ꂽ��݂����̂܂܎��ւƓq���邱�Ƃ��ł��܂�<br>';
			&menu('���킷��','��߂�');
			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # ����
		$m{coin} -= 10;
		$m{stock} = $m{value} = 0;
		$mes .= '<p>�c�O�ł����ˁB������x���܂���?</p>';
		&menu('Play!','��߂�');
		$m{act} += 5;
	}
	$m{tp} = 500;
}



1; # �폜�s��
