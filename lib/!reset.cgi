#================================================
# ��ؾ�� Created by Merino
#================================================

# �����Փx�F[��� 60 �` 40 �ȒP]
my $game_lv = int( rand(11) + 45 );

# �������(��)
my $limit_touitu_day = int( rand(6)+10 );


#================================================
# �������߂����ꍇ
#================================================
sub time_limit  {
	&write_world_news("<b>$world_name�嗤�𓝈ꂷ��҂͌���܂���ł���</b>");
	&write_legend('touitu', "$world_name�嗤�𓝈ꂷ��҂͌���܂���ł���");
	$w{win_countries} = '';

	$w{world} = int(rand($#world_states)) unless $w{year} =~ /6$/; # �Í������ؾ�Ă͏��ύX���Ȃ�(�Í��������邽�߂ɏ�͂��̂܂�)
	&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>") unless $w{year} =~ /5$/;
	&reset;
	
	if ($w{world} eq '0') { # ���a
		$w{reset_time} += 3600 * 24 * 2;
	}
	elsif ($w{world} eq '7') { # ����
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			push @win_cs, [$i, $cs{win_c}[$i]];
		}
		@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;
		
		# ��̏ꍇ�͈�ԍ��͏���
		shift @win_cs if @win_cs % 2 == 1;
		
		my $half_c = int(@win_cs*0.5-1);
		for my $i (0 .. $half_c) {
			my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
			$w{'p_'.$c_c} = 1;
		}
	}

	&write_cs;
}

#================================================
# ���ް�ؾ�ď���
#================================================
sub reset {
	# ���E� �Í�����
	if ($w{year} =~ /6$/) {
		require './lib/vs_npc.cgi';
		&delete_npc_country;
		$w{world} = int(rand($#world_states));
	}

	# �d���ł���l��
	my $ave_c = int($w{player} / $w{country}) + 2;
	
	# set world
	$w{year}++;
	$w{game_lv} = $game_lv;
	$w{reset_time} = $time + 3600 * 24;
	$w{limit_time} = $time + 3600 * 24 * $limit_touitu_day;

	my($c1, $c2) = split /,/, $w{win_countries};

	# set countries
	for my $i (1 .. $w{country}) {
		# ���ꍑ�̏ꍇ��NPC���
		$cs{strong}[$i]   = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(6) + 10) * 1000;
		$cs{food}[$i]     = int(rand(30) + 5) * 1000;
		$cs{money}[$i]    = int(rand(30) + 5) * 1000;
		$cs{soldier}[$i]  = int(rand(30) + 5) * 1000;
		$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
		$cs{capacity}[$i] = $ave_c;
		$cs{is_die}[$i]   = 0;
		
		for my $j ($i+1 .. $w{country}) {
			$w{ "f_${i}_${j}" } = int(rand(40));
			$w{ "p_${i}_${j}" } = 0;
		}
		
		if ($w{year} % $reset_ceo_cycle_year == 0) {
			$cs{old_ceo}[$i] = $cs{ceo}[$i];
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}
	
	if ($w{year} % $reset_ceo_cycle_year == 0) {
		&write_world_news("<b>�e����$e2j{ceo}�̔C���������ƂȂ�܂���</b>");
	}
	
	# ���E� �Í��˓�
	if ($w{year} =~ /6$/) {
		require './lib/vs_npc.cgi';
		&add_npc_country;
	}
}




1; # �폜�s��
