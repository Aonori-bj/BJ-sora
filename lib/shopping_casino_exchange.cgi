$mes .= qq|��� $m{coin} ��<br>| if $is_mobile;
#================================================
# ���Ɍ����� Created by Merino
#================================================

# �����ܕi
my @prizes = (
# ��� 1=����,2=��,3=�߯�
#	[0]���,[1]No,[2]����
	[0,	0,	0,		],
	[2,	22,	1000,	],
	[2,	24,	3000,	],
	[2,	23,	5000,	],
	[1,	2,	10000,	],
	[1,	7,	10000,	],
	[1,	22,	10000,	],
	[2,	25,	20000,	],
	[2,	16,	30000,	],
	[3,	126,40000,	],
	[2,	3,	100000,	],
	[2,	2,	200000,	],
);


#================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�͂��f�肾<br>";
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
		$mes .= '���ɉ�������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�����́A�莝���̂�����݂Ɍ���������<br>';
		$mes .= '��݂Əܕi�̌��������邱�Ƃ��ł��܂�<br>';
		$mes .= '�ǂ����܂����H<br>';
	}
	&menu('��߂�','��݂Ɍ���','�ܕi�ƌ���');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#=================================================
# ��������݂Ɍ���
#=================================================
sub tp_100 {
	$layout = 1;

	$mes .= "$m{name}�l�ͺ�݂�$m{coin}���������ł�<br>";
	$mes .= '���1��20G�ł�<br>�����炨���߂ł���?<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="coin" value="0" class="text_box1" style="text-align:right">��|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	if ($in{coin} && $in{coin} !~ /[^0-9]/) {
		my $v = int($in{coin} * 20);
		if ($m{money} >= $v) {
			$m{money} -= $v;
			$m{coin}  += $in{coin};
			$mes .= "$v G��� $in{coin} ���Ɍ������܂���<br>";
		}
		else {
			$mes .= '����������܂���<br>';
		}
	}
	&begin;
}


#=================================================
# ��݁��ܕi�Ɍ���
#=================================================
sub tp_200 {
	$layout = 1;

	$mes .= "$m{name}�l�ͺ�݂�$m{coin}���������ł�<br>";
	$mes .= "�ǂ̏ܕi�ƌ������܂���?<br>";

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>�ܕi</th><th>�K�v���<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked> ��߂�<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i"> |;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[��]$eggs[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[�y]$pets[ $prizes[$i][1] ][1]</td>|
			  ;
		$mes .= qq|<td align="right">$prizes[$i][2]���<br></td></tr>|;
	}
	$mes .= qq|</table><p><input type="submit" value="��������" class="button1"></p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"></form>|;
	$m{tp} += 10;
}
sub tp_210 {
	if ($cmd) {
		for my $i (1 .. $#prizes) {
			next unless $cmd eq $i;

			if ($m{coin} >= $prizes[$i][2]) {
				$m{coin} -= $prizes[$i][2];

				if ($prizes[$i][0] eq '1') {
					$mes .= "$weas[ $prizes[$i][1] ][1]�Ɍ������܂���<br>";
					&send_item($m{name}, $prizes[$i][0], $prizes[$i][1], $weas[ $prizes[$i][1] ][4]);
				}
				elsif ($prizes[$i][0] eq '2') {
					$mes .= "$eggs[ $prizes[$i][1] ][1]�Ɍ������܂���<br>";
					&send_item($m{name}, $prizes[$i][0], $prizes[$i][1]);
				}
				elsif ($prizes[$i][0] eq '3') {
					$mes .= "$pets[ $prizes[$i][1] ][1]�Ɍ������܂���<br>";
					&send_item($m{name}, $prizes[$i][0], $prizes[$i][1]);
				}
			}
			else {
				$mes .= '��݂�����܂���<br>';
			}
			last;
		}
	}
	&begin;
}




1; # �폜�s��
