require './lib/move_player.cgi';
#=================================================
# �d�� Created by Merino
#=================================================

# �S������
$GWT *= 2;

# �d������̂ɕK�v������
my $need_lv = 1;

# �d������̂ɕK�v�ȋ��z
my $need_money = $m{sedai} > 10 ? $rank_sols[$m{rank}]+30000 : $rank_sols[$m{rank}]+$m{sedai}*3000;

# ���E����Í��̏ꍇ�ANPC���֎d������̂ɕK�v�ȋ��z
my $need_money_npc = 300000;


#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�͎d�����邱�Ƃ��ł��܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{lv} < $need_lv) {
		$mes .= "�d������ɂ� $need_lv ���وȏ�K�v�ł�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{country}) {
		$mes .= "�d������葱���Ƃ���$GWT��������܂�<br>";
		$mes .= "���̍��Ɏd������Ƒ�\\���߲�ĂƊK����������܂�<br>";
		$mes .= "�������Ɏd������ꍇ�͊K����������܂���<br>" if $union;
		$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����K�v������܂�<br>";
		
		# �Í�
		if ($w{world} eq $#world_states) {
			$mes .= qq|<font color="#FF0000">$cs{name}[$w{country}]�Ɏd������ꍇ�́A���̔N�ɂȂ�܂ő��̍��Ɏd�����邱�Ƃ͂ł��܂���<br>|;
			$mes .= qq|$cs{name}[$w{country}]�Ɏd������ꍇ�́A��\\�߲�Ă� 0 �ɂȂ�A$need_money_npc G�x�����K�v������܂�<br></font>|;
		}
		
		$mes .= '�ǂ̍��Ɏd�����܂���?<br>';
		
		&menu('��߂�', @countries, '���Q����');
	}
	else {
		$mes .= '�ǂ̍��Ɏd�����܂���?<br>';
		&menu('��߂�', @countries);
	}
}
sub tp_1 {
	return if &is_ng_cmd(1 .. $w{country}+1);
	
	if ($cmd eq $m{country}) {
		$mes .= "�����Ɏd���͂ł��܂���<br>";
		&begin;
	}
	# �������Q
	elsif ($cmd == $w{country} + 1) {
		 # ������
		if ($m{name} eq $m{vote}) {
			$mes .= "$c_m��$e2j{ceo}�̗��������C����K�v������܂�<br>";
			&begin;
			return;
		}

		&move_player($m{name}, $m{country}, 0);
		$m{country} = 0;
		$m{rank} = 0;
		$m{rank_exp} = 0;
		
		&mes_and_world_news("$c_m���痧��������Q�̗��ɏo�܂���",1);
		
		# ��\�߲��0
		for my $k (qw/war dom mil pro/) {
			$m{$k.'_c'} = 0;
		}

		$mes .= "���ɍs���ł���̂�$GWT����ł�<br>";
		&refresh;
		&wait;
	}
	elsif ($cs{member}[$cmd] >= $cs{capacity}[$cmd]) {
		$mes .= "$cs{name}[$cmd]�͒���������ς��ł�<br>";
		&begin;
	}
	elsif (defined $cs{name}[$cmd]) { # �������݂���
		# �������̍�
		if ($m{country}) {
			# �N��
			if ($m{name} eq $cs{ceo}[$m{country}]) {
				$mes .= "$c_m��$e2j{ceo}�����C����K�v������܂�<br>";
				&begin;
				return;
			}
			elsif ($need_money > $m{money}) {
				$mes .= "�ڐЂ���ɂ� $need_money G�K�v�ł�<br>";
				&begin;
				return;
			}
			# �Í�
			elsif ($w{world} eq $#world_states) {
				if ($m{country} eq $w{country}) {
					$mes .= "$cs{name}[$m{country}]���甲���o�����Ƃ͋�����܂���<br>";
					&begin;
					return;
				}
				elsif ($cmd eq $w{country}) {
					require './lib/vs_npc.cgi';
					if ($need_money_npc > $m{money}) {
						$mes .= "�����ƌ_�񂷂�ɂ� $need_money_npc G�K�v�ł�<br>";
						&begin;
						return;
					}
					elsif (!&is_move_npc_country) {
						&begin;
						return;
					}
					$need_money = $need_money_npc;
				}
			}
			
			$m{money} -= $need_money;
			$cs{money}[$m{country}] += $need_money;
			$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����܂���<br>";
			
			unless ($union eq $cmd) {
				$m{rank} -= $m{rank} > 10 ? 2 : 1;
				$m{rank} = 1 if $m{rank} < 1;
				$mes .= "�K����$ranks[$m{rank}]�ɂȂ�܂���<br>";

				# ��\�߲�Ĕ���
				for my $k (qw/war dom mil pro/) {
					$m{$k.'_c'} = int($m{$k.'_c'} * 0.5);
				}
			}
			
			$mes .= "�ڐЂ̎葱����$GWT��������܂�<br>" ;
			&wait;
		}
		# ����������
		else {
			$m{rank} = 1 if $m{rank} < 1;
			&n_menu;
		}
		
		&move_player($m{name}, $m{country}, $cmd);
		$m{next_salary} = $time + 3600 * $salary_hour;
		$m{country} = $cmd;
		$m{vote} = '';
		
		&mes_and_world_news("$cs{name}[$cmd]�Ɏd�����܂���",1);
		
		&refresh;
	}
	else {
		&begin;
	}
}




1; # �폜�s��
