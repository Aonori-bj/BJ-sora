my $this_file = "$logdir/junk_shop.cgi";
#================================================
# �ެݸ����� Created by Merino
#=================================================

# �����Ȃ��Ƃ��̔���(����)
my @wea_nos = (1,6,11,16,21,26);

# ����������Ϻ�
my @gacha_eggs = (
	# �l�i,		�Ϻ�No
	[5000,	[42,42,43,43,43,43,51,51,51,1,4],		],
	[20000,	[42,42,42,42,42,43,43,1,4..15,33,50],	],
	[50000,	[42,43,1,3..24,33,33,33,50],			],
);

# ���������Ϻނ��ł���Ԋu(�b)
my $gacha_time = 24 * 60 * 60;

# �����l�i
my $buy_price  = 500;

# ����l�i
my $sall_price = 100;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ�����?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�ެݸ����߂łȂ�ł������Ȃ�ł�����<br>';
		$mes .= '���O������?<br>';
	}
	
	&menu('��߂�','����','����', '������');
}

sub tp_1 {
	return if &is_ng_cmd(1..3);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '1') {
		$mes .= "�~�����̂�����?<br>������ӂ̂��� $buy_price G�ł�����<br>";
		&menu('��߂�','����');
	}
	elsif ($cmd eq '2') {
		$mes .= "���𔄂Ă���� $sall_price G�Ŕ������<br>";
		my @menus = ('��߂�');
		push @menus, $m{wea} ? $weas[$m{wea}][1] : '';
		push @menus, $m{egg} ? $eggs[$m{egg}][1] : '';
		push @menus, $m{pet} ? $pets[$m{pet}][1] : '';
		&menu(@menus);
	}
	elsif ($cmd eq '3') {
		$mes .= '�^���܂��̶��������ϺށB�l�i�F�X�B�����o�邩�͂��y����<br>';
		my @menus = ('��߂�');
		for my $i (0..$#gacha_eggs) {
			push @menus, "$gacha_eggs[$i][0] G";
		}
		&menu(@menus);
	}
	else {
		&begin;
	}
}

#=================================================
# ����
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	
	if ($m{money} < $buy_price) {
		$mes .= '���O�n�R�B����Ȃ��B�n�R�ɂȂ�����<br>';
	}
	elsif ($m{is_full}) {
		$mes .= '���O�̗a���菊���ς��B����Ȃ�<br>';
	}
	else {
		$m{money} -= $buy_price;

		if (-s $this_file) {
			my $count = 0;
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_file ̧�ق��J���܂���");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				push @lines, $line;
				last if ++$count > 50;
			}
			my $get_line = int(rand(2)) == 0 ? shift @lines : pop @lines;
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
			
			my($kind, $item_no, $item_c) = split /<>/, $get_line;
			
			&send_item($m{name}, $kind, $item_no, $item_c);
			$mes .= $kind eq '1' ? $weas[$item_no][1]
				  : $kind eq '2' ? $eggs[$item_no][1]
				  :				   $pets[$item_no][1]
				  ;
			$mes .= '�𔃂��܂���<br>';
			
		}
		# �����Ȃ��ꍇ�̓f�t�H���g�A�C�e��
		else {
			my $wea_no = $wea_nos[int(rand(@wea_nos))];
			&send_item($m{name}, 1, $wea_no, $weas[$wea_no][4]);
			$mes .= "$weas[$wea_no][1]�𔃂��܂���<br>";
		}
		$mes .= "���O�����z�A�F�B�B�������͗a���菊�ɑ�����<br>";
	}
	&begin;
}

#=================================================
# ����
#=================================================
sub tp_200 {
	if (    ($cmd eq '1' && $m{wea})
		 || ($cmd eq '2' && $m{egg})
		 || ($cmd eq '3' && $m{pet}) ) {
		 
			if ($cmd eq '1') {
				$mes .= "$weas[$m{wea}][1]�𔄂�܂���<br>";
				$line = "$cmd<>$m{wea}<>$m{wea_c}<>\n";
				$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
			}
			elsif ($cmd eq '2') {
				$mes .= "$eggs[$m{egg}][1]�𔄂�܂���<br>";
				$line = "$cmd<>$m{egg}<>$m{egg_c}<>\n";
				$m{egg} = $m{egg_c} = 0;
			}
			elsif ($cmd eq '3') {
				$mes .= "$pets[$m{pet}][1]�𔄂�܂���<br>";
				$line = "$cmd<>$m{pet}<>0<>\n";
				$m{pet} = 0;
			}
			else {
				&error('���т̎�ނ��ُ�ł�');
			}
			
			$mes .= "���O�����l�A���ǂ��B�ǂ����̎��Ă� $sall_money G���<br>";
			$m{money} += $sall_price;
			
			open my $fh, ">> $this_file" or &error("$this_filȩ�ق��J���܂���");
			print $fh $line;
			close $fh;
	}
	&begin;
}

#=================================================
# ������
#=================================================
sub tp_300 {
	return if &is_ng_cmd(1..$#gacha_eggs+1);
	--$cmd;
	
	if ($m{gacha_time} + $gacha_time > $time) {
		my $g_time = $m{gacha_time} + $gacha_time - $time;
		my $next_gacha_time = sprintf("%02d��%02d��", int($g_time / 3600), int($g_time % 3600 / 60) );
		$mes .= "�����������߂���Ƃ��O����B���� $next_gacha_time ���炢�҂�<br>";
	}
	elsif ($m{money} >= $gacha_eggs[$cmd][0]) {
		my @egg_nos = @{ $gacha_eggs[$cmd][1] };
		my $egg_no  = $egg_nos[int(rand(@egg_nos))];
		$m{money}  -= $gacha_eggs[$cmd][0];
		
		&send_item($m{name}, 2, $egg_no,);
		$mes .= "�����������߰��<br>$eggs[$egg_no][1]���o�܂���<br>";
		
		$m{gacha_time} = $time;
	}
	else {
		$mes .= '���O�n�R�B����������ҁB�n�R�ɂȂ�����<br>';
	}

	&begin;
}


1; # �폜�s��
