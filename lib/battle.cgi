require "$datadir/skill.cgi";
$is_battle = 1; # �����׸�1
#================================================
# �퓬 Created by Merino
#================================================

# ����ɂ��D��
my %tokkous = (
# '��������' => qr/�ア����/,
	'��' => qr/��/,
	'��' => qr/��/,
	'��' => qr/��/,
	'��' => qr/��|��/,
	'��' => qr/��|��/,
	'��' => qr/��|��/,
	'��' => qr/��|��|��/,
);

#================================================
# �g���l�� Set
#================================================
my @m_skills = split /,/, $m{skills};
my @y_skills = split /,/, $y{skills};

# ��ʕ\���⽷قŎg���̂Ÿ�۰��ٕϐ�
$m_at = $m{at};
$y_at = $y{at};
$m_df = $m{df};
$y_df = $y{df};
$m_ag = $m{ag};
$y_ag = $y{ag};

# �g�p����̂� AT or MAT, DF or MDF �̂ǂ��炩
if    ($weas[$m{wea}][2] =~ /��|��|��|��/) { $m_at = $m{at}  + $weas[$m{wea}][3]; }
elsif ($weas[$m{wea}][2] =~ /��|��|��/)    { $m_at = $m{mat} + $weas[$m{wea}][3]; $y_df = $y{mdf}; }
if    ($weas[$y{wea}][2] =~ /��|��|��|��/) { $y_at = $y{at}  + $weas[$y{wea}][3]; }
elsif ($weas[$y{wea}][2] =~ /��|��|��/)    { $y_at = $y{mat} + $weas[$y{wea}][3]; $m_df = $m{mdf}; }

$m_ag -= $weas[$m{wea}][5];
$m_ag = int(rand(5)) if $m_ag < 1;
$y_ag -= $weas[$y{wea}][5];
$y_ag = int(rand(5)) if $y_ag < 1;

$m_at = int($m_at * 0.5) if $m{wea} && $m{wea_c} <= 0;

if ($m{wea} && $y{wea}) {
	if (&is_tokkou($m{wea},$y{wea})){
		$m_at = int(1.5 *$m_at);
		$y_at = int(0.75*$y_at);
		$is_m_tokkou = 1;
	}
	elsif (&is_tokkou($y{wea},$m{wea})) {
		$y_at = int(1.5 *$y_at);
		$m_at = int(0.75*$m_at);
		$is_y_tokkou = 1;
	}
}

#================================================
# Ҳݓ���
#================================================
&run_battle;
&battle_menu if $m{hp} > 0 && $y{hp} > 0;


#================================================
# ���s����
#================================================
sub run_battle {
	if ($cmd eq '') {
		$mes .= '�퓬����ނ�I�����Ă�������<br>';
	}
	elsif ($m{turn} >= 20) { # �Ȃ��Ȃ��������Ȃ��ꍇ
		$mes .= '�퓬���E��݂𒴂��Ă��܂����c����ȏ�͐킦�܂���<br>';
		&lose;
	}
	elsif ( rand($m_ag * 3) >= rand($y_ag * 3) ) {
		my $v = &m_attack;
		if ($y{hp} <= 0 && $m{hp} > 0) {
			&win;
		}
		else {
			&y_attack;
			if    ($m{hp} <= 0) { &lose; }
			elsif ($y{hp} <= 0) { &win;  }
			elsif ($m{pet}) {
				&use_pet('battle', $v);
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	else {
		&y_attack;
		if ($m{hp} <= 0) {
			&lose;
		}
		else {
			my $v = &m_attack;
			if    ($m{hp} <= 0) { &lose;  }
			elsif ($y{hp} <= 0) { &win; }
			elsif ($m{pet}) {
				&use_pet('battle', $v);
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	
	$m{mp} = 0 if $m{mp} <= 0;
	$y{mp} = 0 if $y{mp} <= 0;
}


#=================================================
# �����̍U��
#=================================================
sub m_attack {
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	# �K�E�Z ����Ⱥ���ނ� # �������������Ă�����̂Ɠ����� # MP�����邩
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && $m{mp} >= $m_s->[3] ) {
		$m{mp} -= $m_s->[3];
		$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
		$mes .= "$m{name}��$m_s->[1]!!<br>";
		local $who = 'm';
		&{ $m_s->[4] }($m_at);
	}
	# �ߺ��! �K���Z5���� ���� �������� ���� ����̋������ʈȏな 
	elsif (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0) {
		local $who = 'm';
		&_pikorin;
	}
	else { # �U��
		$mes .= "$m{name}�̍U��!!";
		my $v = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0
			? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
		
		if ($is_counter) {
			$mes .= "<br>�U����Ԃ��� $v ����Ұ�ނ������܂���<br>";
			$m{hp} -= $v;
		}
		elsif ($is_stanch) {
			$mes .= "<br>��݂œ����Ȃ�!<br>";
		}
		else {
			$mes .= "<br>$v ����Ұ�ނ��������܂���<br>";
			if ($m{wea_c} > 0) {
				--$m{wea_c};
				$mes .= "$weas[$m{wea}][1]�͉��Ă��܂���<br>" if $m{wea_c} == 0;
			}
			$y{hp} -= $v;
		}
	}
}
#=================================================
# ����̍U��
#=================================================
sub y_attack {
	my $y_s = $skills[ $y_skills[ int(rand(6))-1 ] ];
	
	# �K�E�Z ����Ⱥ���ނ� # �������������Ă�����̂Ɠ����� # MP�����邩
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && $y{mp} >= $y_s->[3] ) {
		$y{mp} -= $y_s->[3];
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}��$y_s->[1]!!<br>";

		local $who = 'y';
		&{ $y_s->[4] }($y_at);
	}
	else {
		$mes .= "$y{name}�̍U��!!";
		my $v = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0
			? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);

		if ($is_counter) {
			$mes .= "<br>�U����Ԃ� $v ����Ұ�ނ��������܂���<br>";
			$y{hp} -= $v;
		}
		elsif ($is_stanch) {
			$mes .= "<br>��݂œ����Ȃ�!<br>";
		}
		else {
			$mes .= "<br>$v ����Ұ�ނ������܂���<br>";
			$m{hp} -= $v;
		}
	}
}

#=================================================
# ��S�A�ʏ�U��
#=================================================
sub _attack_kaishin {
	my $at = shift;
	$mes .= '<b>��S�̈ꌂ!!</b>';
	return int($at * (rand(0.4)+0.8) );
}
sub _attack_normal {
	my($at, $df) = @_;
	my $v = int( ($at * 0.5 - $df * 0.3) * (rand(0.3)+ 0.9) );
	   $v = int(rand(5)+1) if $v < 5;
	return $v;
}
#=================================================
# �V�Z�K��(���łɊo���Ă���Z�ł�����)
#=================================================
sub _pikorin {
	# �o�����鑮���̂��̂�S��@lines�ɓ����
	my @lines = ();
	for my $i (1 .. $#skills) {
		push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
	}
	
	if (@lines) {
		my $no = $lines[int(rand(@lines))];
		$m_mes = "�M����!! $skills[$no][1]!";
		# �o���Ă��Ȃ��Z�Ȃ�ǉ�
		my $is_learning = 1;
		for my $m_skill (@m_skills) {
			if ($m_skill eq $no) {
				$is_learning = 0;
				last;
			}
		}
		$m{skills} .= "$no," if $is_learning;
		$mes .= qq|<font color="#CCFF00">���M��!!$m{name}��$skills[ $no ][1]!!</font><br>|;
		$skills[ $no ][4]->($m_at);
	}
	else { # ��O�����F�o��������̂��Ȃ�
		$m_mes = '�M�߂������őM���Ȃ��c';
	}
}


#=================================================
# �퓬�p���j���[
#=================================================
sub battle_menu {
	$menu_cmd  = qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
	$menu_cmd .= qq|<option value="0">�U��</option>|;
	for my $i (1 .. $#m_skills+1) {
		next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
		next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
		$menu_cmd .= qq|<option value="$i"> $skills[ $m_skills[$i-1] ][1]</option>|;
	}
	$menu_cmd .= qq|</select><br><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= qq|<input type="submit" value="�� ��" class="button1"></form>|;
}


#=================================================
# ����
#=================================================
sub win {
	$m{hp} = 0 if $m{hp} < 0;
	$y{hp} = 0;
	$m{turn} = 0;
	$mes .= "$y{name}��|���܂���<br>";

	$m_mes = $m{mes_win}  unless $m_mes;
	$y_mes = $y{mes_lose} unless $y_mes;
}

#=================================================
# �s�k
#=================================================
sub lose {
	$m{hp} = 0;
	$y{hp} = 0 if $y{hp} < 0;
	$m{turn} = 0;
	$mes .= "$m{name}�͂���Ă��܂����c<br>";

	$m_mes = $m{mes_lose} unless $m_mes;
	$y_mes = $y{mes_win}  unless $y_mes;
}


#=================================================
# ����ɂ����U�������ǂ���
#=================================================
sub is_tokkou {
	my($wea1, $wea2) = @_;
	return defined $tokkous{ $weas[$wea1][2] } && $weas[$wea2][2] =~ /$tokkous{ $weas[$wea1][2] }/ ? 1 : 0;
}



1; # �폜�s��
