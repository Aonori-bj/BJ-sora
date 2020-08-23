#=================================================
# [�Í�]NPC��p��۸��� Created by Merino
#=================================================

# ���x�������l��NPC���Ɏd�����Ȃ��悤�Ɏd�����O(�l)
$max_npc_old_member = $w{player} * 0.2;

# NPC��(�擪5���͐푈�����Ƃ��ɏo������)
my @npc_names = (qw/�ި���۽(NPC) ׳ޫ�(NPC) ҷ����(NPC) �ް�(NPC) ����۽(NPC) ����(NPC) �޽(NPC) �ײ(NPC) ׽�(NPC) ��ײ��(NPC) �ެ���(NPC) ���(NPC) ��ٽ(NPC) ѽ�(NPC) �ް��ް��(NPC) �ެ�è�(NPC) ����(NPC) �ާر�(NPC) �ٽޱ�(NPC)  ͳ�ݽ���(NPC) �۲(NPC) ����ٽ�(NPC) ��(NPC) ���(NPC) ���(NPC) ���(NPC)/);
#                   0             1          2           3         4


#=================================================
# NPC���̒ǉ�
#=================================================
sub add_npc_country {
	&write_world_news("<i>���̔e�ҒB�ɂ���ĕ��󂳂�Ă������E�̌��E����܂�A�������Ă��S�낤�Ƃ��Ă���c</i>");
	$w{game_lv} = 99;
	$w{world} = $#world_states;
	
	# NPC�̍��̖��O
	my @c_names = (qw/�ި���۽�鍑 �޽��ݽ�鍑 �ް��鍑 �א_�鍑 �����̏� �֒f�̖��E ������ �ł̖�����/);
	my $npc_country_name  = $c_names[int(rand(@c_names))];
	
	# NPC�̍��F
	my $npc_country_color = '#FF00FF';

	++$w{country};
	my $i = $w{country};

	mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
	for my $file_name (qw/bbs bbs_log bbs_member patrol prison prison_member prisoner violator old_member/) {
		my $output_file = "$logdir/$i/$file_name.cgi";
		next if -f $output_file;
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		close $fh;
		chmod $chmod, $output_file;
	}
	for my $file_name (qw/leader member/) {
		my $output_file = "$logdir/$i/$file_name.cgi";
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		close $fh;
		chmod $chmod, $output_file;
	}
	
	&add_npc_data($i);
	
	# create union file
	for my $j (1 .. $i-1) {
		my $file_name = "$logdir/union/${j}_${i}";
		$w{ "f_${j}_${i}" } = -99;
		$w{ "p_${j}_${i}" } = 2;

		next if -f "$file_name.cgi";
		open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ̧�ق����܂���");
		close $fh;
		chmod $chmod, "$file_name.cgi";
		
		open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ̧�ق����܂���");
		close $fh2;
		chmod $chmod, "${file_name}_log.cgi";
		
		open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ̧�ق����܂���");
		close $fh3;
		chmod $chmod, "${file_name}_member.cgi";
	}
	
	unless (-f "$htmldir/$i.html") {
		open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ̧�ق����܂���");
		close $fh_h;
	}

	$cs{name}[$i]     = $npc_country_name;
	$cs{color}[$i]    = $npc_country_color;
	$cs{member}[$i]   = 0;
	$cs{win_c}[$i]    = 999;
	$cs{tax}[$i]      = 99;
	$cs{strong}[$i]   = 99999;
	$cs{food}[$i]     = 999999;
	$cs{money}[$i]    = 999999;
	$cs{soldier}[$i]  = 999999;
	$cs{state}[$i]    = 5;
	$cs{capacity}[$i] = 6; # ���S��NPC���ɂ������ꍇ�� ���̐����� 0 �ɂ���
	$cs{is_die}[$i]   = 0;
	
	my @lines = &get_countries_mes();
	if ($w{country} > $#lines) {
		open my $fh9, ">> $logdir/countries_mes.cgi";
		print $fh9 "���J�i���l�ԋ����A�̑�i����K�Ńm�`�J���m�O�j�����X�K�ǃC�c<>diabolos.gif<>\n";
		close $fh9;
	}
}
#=================================================
# �푈NPC��ׂ��쐬
#=================================================
sub add_npc_data {
	my $country = shift;
	
	my %npc_statuss = (
		max_hp => [999, 600, 400, 300, 99],
		max_mp => [999, 500, 200, 100, 99],
		at     => [999, 400, 300, 200, 99],
		df     => [999, 300, 200, 100, 99],
		mat    => [999, 400, 300, 200, 99],
		mdf    => [999, 300, 200, 100, 99],
		ag     => [999, 500, 300, 200, 99],
		cha    => [999, 400, 300, 200, 99],
		lea    => [666, 400, 250, 150, 99],
		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
	);
	my @npc_weas = (
	#	[0]����[1]����No	[2]�K�E�Z
		['��', [0],			[61..65],],
		['��', [1 .. 5],	[1 .. 5],],
		['��', [6 ..10],	[11..15],],
		['��', [11..15],	[21..25],],
		['��', [16..20],	[31..35],],
		['��', [21..25],	[41..45],],
		['��', [26..30],	[51..55],],
	);
	my $line = qq|\@npcs = (\n|;
	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;
		
		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}
		
		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;

		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	$line .= qq|);\n\n1;\n|;
	
	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}

#=================================================
# NPC���̍폜
#=================================================
sub delete_npc_country {
	if ($is_npc_win) {
		if ($m{country} eq $w{country}) {
			$w{win_countries} = $union ? $union : '';
			$m{country} = 0;
			$cs{war}[0] = $m{name};
			$m{shogo}   = '���V�g��';
		}
		else {
			$w{win_countries} = $m{country};
		}
		
		# ����\�҂ɓ��T
		for my $k (qw/war dom pro mil ceo/) {
			next if $cs{$k}[$w{country}] eq '';
			&send_item($cs{$k}[$w{country}], 3, int(rand(2)+19) );
		}
	}

	my @names = &get_country_members($w{country});
	require "./lib/move_player.cgi";
	
	for my $name (@names) {
		$name =~ tr/\x0D\x0A//d;
		&move_player($name, $w{country}, 0);
		&regist_you_data($name, 'country', 0);
		$is_npc_win ? &regist_you_data($name, 'shogo', '���V�g��') : &regist_you_data($name, 'shogo', $shogos[1][0]);
	}
	--$w{country};
	
	my @lines = ();
	open my $fh, "+< $logdir/countries_mes.cgi";
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	pop @lines if @lines > $w{country};
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#=================================================
# NPC���̌R�� ./lib/military.cgi�ŕp�x����
#=================================================
sub npc_military {
	my @keys = (qw/gou gou gou cho cho cho sen ds/);
	my $k = $keys[int(rand(@keys))];
	my $country = int(rand($w{country}-1)+1);
	return if $cs{is_die}[$country]; # �ŖS������͒D��Ȃ�
	&{'npc_military_'.$k}($country);
}
sub npc_military_gou { # ���D
	my $country = shift;
	my $v = &_npc_get_resource($country, 'food');
	&write_world_news("$cs{name}[$w{country}]��$npc_names[int(rand(@npc_names))]��$cs{name}[$country]�Ɋ�P�U�������{�B$v�̕��Ƃ����D���邱�Ƃɐ������܂���");
}
sub npc_military_cho { # ����
	my $country = shift;
	my $v = &_npc_get_resource($country, 'money');
	&write_world_news("$cs{name}[$w{country}]��$npc_names[int(rand(@npc_names))]��$cs{name}[$country]�̎������BٰĂ��h�����A$v��$e2j{money}�𗬏o�����邱�Ƃɐ������܂���");
}
sub npc_military_sen { # �R��
	my $country = shift;
	my $v = &_npc_get_resource($country, 'soldier');
	&write_world_news("$cs{name}[$w{country}]��$npc_names[int(rand(@npc_names))]��$cs{name}[$country]��$v�̕�����]���邱�Ƃɐ���!$cs{name}[$w{country}]�̕��Ɏ�荞�݂܂���");
}
sub npc_military_ds { # Dead Soldier ����̏���
	return if $cs{soldier}[$w{country}] > 500000;
	$cs{$k}[$w{country}] += 50000;
	&write_world_news("$cs{name}[$w{country}]��$npc_names[int(rand(@npc_names))]�����̍���莀��̕��m���Ăъo�܂��A$cs{name}[$w{country}]�̑����m����50000�������܂���");
}
sub _npc_get_resource {
	my($country, $k) = @_;

	my $v = int(rand(15000)+15000);
	$v *= 2 if $cs{strong}[$w{country}] < 30000;
	$v = $v > $cs{$k}[$country] ? $cs{$k}[$country] : $v;
	$cs{$k}[$country]    -= $v;
	$cs{$k}[$w{country}] += $v;
	
	return $v;
}

#=================================================
# NPC���̐푈 ./lib/_war_result.cgi�ŕp�x����
#=================================================
sub npc_war {
	if ($cs{strong}[$w{country}] < 50000) {
		  rand(6)  < 1 ? &npc_use_pet_fenrir
		: rand(10) < 1 ? &npc_use_pet_prisoner
		: rand(20) < 1 ? &npc_use_pet_pesto
		: rand(15) < 1 ? &npc_use_pet_loptr
		: rand(40) < 1 ? &npc_use_pet_meteo
		:                &npc_get_strong
		;
	}
	else {
		  rand(3)  < 1 ? &npc_use_pet_fenrir
		: rand(15) < 1 ? &npc_use_pet_prisoner
		: rand(20) < 1 ? &npc_use_pet_pesto
		: rand(20) < 1 ? &npc_use_pet_loptr
		: rand(50) < 1 ? &npc_use_pet_meteo
		:                &npc_get_strong
		;
	}
}
sub npc_use_pet_fenrir { # ̪���
	return if $touitu_strong < 20000;
	$w{game_lv} += 1 if $w{game_lv} < 90;
	for my $i (1..$w{country}-1) {
		next if $cs{is_die}[$i];
		next if $cs{strong}[$i] < 1000;
		$cs{strong}[$i] -= $touitu_strong * 0.6 > $cs{strong}[$w{country}] ? int(rand(400)+400) : int(rand(200)+200);
	}
	
	$touitu_strong * 0.6 > $cs{strong}[$w{country}] ? 
		&write_world_news("$cs{name}[$w{country}]��$npc_names[0]�̖��_�̑M��!�e����$e2j{strong}������܂���"):
		&write_world_news("$cs{name}[$w{country}]��$npc_names[4]�̔j�����!�e����$e2j{strong}������܂���");
		
}
sub npc_use_pet_loptr { # ����
	$w{game_lv} -= 1 if $w{game_lv} > 80;
	&write_world_news("$cs{name}[$w{country}]������(NPC)�̎א_�̍ق�!");
	&disaster;
}
sub npc_use_pet_pesto { # �߽�
	$w{game_lv} -= 1 if $w{game_lv} > 75;
	for my $i (1..$w{country}) {
		$cs{state}[$i] = 5;
	}
	&write_world_news("<b>$cs{name}[$w{country}]��$npc_names[int(rand(@npc_names))]���ғł��T���U�炵�e����$e2j{state}�� $country_states[5] �ɂȂ�܂���</b>");
}
sub npc_use_pet_meteo { # �õ
	$w{game_lv} -= 2 if $w{game_lv} > 85;
	for my $i (1..$w{country}) {
		for my $j ($i+1..$w{country}) {
			$w{"f_${i}_${j}"}=int(rand(20));
			$w{"p_${i}_${j}"}=2;
		}
	}
	&write_world_news("<b>$cs{name}[$w{country}]��$npc_names[int(rand(@npc_names))]���õ���������E�����J��ƂȂ�܂���</b>");
}
sub npc_use_pet_prisoner { # �S��
	$w{game_lv} -= 1 if $w{game_lv} > 85;
	my @ks = (qw/war dom pro mil ceo/);
	my $k = $ks[int(rand(@ks))];

	for my $i (1 .. $w{country}-1) {
		next if $cs{$k}[$i] eq '';
		next if $cs{$k}[$i] eq $m{name};
		
		&regist_you_data($cs{$k}[$i], 'lib', 'prison');
		&regist_you_data($cs{$k}[$i], 'tp',  100);
		&regist_you_data($cs{$k}[$i], 'y_country',  $w{country});
		
		open my $fh, ">> $logdir/$w{country}/prisoner.cgi" or &error("$logdir/$w{country}/prisoner.cgi ���J���܂���");
		print $fh "$cs{$k}[$i]<>$i<>\n";
		close $fh;
	}
	&write_world_news("<b>$cs{name}[$w{country}]��$npc_names[int(rand(@npc_names))]���s�C���Ȍ�������e���� $e2j{$k} ��$cs{name}[$w{country}]�̘S���ɗH����܂���</b>");
}
sub npc_get_strong { # �D��
	# ����������Ȃ��Ƃ�
	for my $k (qw/food money soldier/) {
		return if $cs{$k}[$w{country}] < 100000;
	}
	
	my $country = 1;
	if ($cs{strong}[$w{country}] < 40000) { # ��ԍ��͂���������I��
		my $max_value = $cs{strong}[1];
		for my $i (2 .. $w{country}-1) {
			if ($cs{strong}[$i] > $max_value) {
				$country = $i;
				$max_value = $cs{strong}[$i];
			}
		}
	}
	else {
		$country = int(rand($w{country}-1)+1);
	}
	
	return if $cs{is_die}[$country];        # �ŖS������͒D��Ȃ�
	return if $cs{strong}[$country] < 1000; # ����1000�����͒D��Ȃ�
	
	# ���̍��̑���̖��O������ю擾
	my $name = '';
	open my $fh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��ǂݍ��߂܂���");
	rand($.) < 1 and $name = $_ while <$fh>;
	close $fh;
	$name =~ tr/\x0D\x0A//d;
	
	my $v = int(rand(300)+300);

	$cs{strong}[$w{country}] += $v;
	$cs{strong}[$country]    -= $v;
	&write_world_news(qq|$cs{name}[$w{country}]��$npc_names[int(rand(@npc_names))]��$cs{name}[$country]�ɐN�U�A$name�̕��������j�� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����Ƃɐ���</font>�����悤�ł�|);

	$cs{is_die}[$w{country}] = 0 if $cs{is_die}[$w{country}];
}


#=================================================
# �����l�����x��NPC���Ɏd�����Ȃ��悤�ɐ���
#=================================================
sub is_move_npc_country {
	my @lines = ();
	open my $fh, "+< $logdir/$w{country}/old_member.cgi" or &error("$logdir/$w{country}/old_member.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		if ($line eq $m{name}) {
			close $fh;
			$mes .= "�ߋ���NPC���֎d�������l�́A���΂炭NPC���֎d�����邱�Ƃ͋�����܂���<br>";
			return 0;
		}
		push @lines, "$line\n";
		last if @lines+1 >= $max_npc_old_member;
	}
	unshift @lines, "$m{name}\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if ($m{name} eq $cs{ceo}[$m{country}]) {
		$mes .= "$c_m��$e2j{ceo}�����C����K�v������܂�<br>";
		&begin;
		return 0;
	}
	
	# ��\�߲��0
	for my $k (qw/war dom mil pro/) {
		$m{$k.'_c'} = int($m{$k.'_c'} * 0);
	}
	&mes_and_world_news("�����ɍ��𔄂�n���܂���", 1);

	return 1;
}



1;
