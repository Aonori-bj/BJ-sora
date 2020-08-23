#=================================================
# �푈���� Created by Merino
#=================================================
# war.cgi�ɂ����Ă��������ǂ����Ⴒ����ɂȂ肻���Ȃ̂ŕ���

# �~�o�l��
my $max_rescue = 1;

#=================================================
# ��������
#=================================================
sub war_draw {
	&c_up('draw_c');
	my $v = int( rand(11) + 10 );
	$m{rank_exp} -= int( (rand(16)+15) * $m{value} );
	$m{exp} += $v;

	$mes .= "$m{name}�ɑ΂���]����������܂���<br>";
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
	
	my $is_rewrite = 0;
	if ($m{sol} > 0) {
		$cs{soldier}[$m{country}] += $m{sol};
		$is_rewrite = 1;
	}
	if ($y{sol} > 0) {
		$cs{soldier}[$y{country}] += $y{sol};
		$is_rewrite = 1;
	}

	&down_friendship;
	&refresh;
	&n_menu;
	&write_cs;
}

#=================================================
# ����
#=================================================
sub war_lose {
	&c_up('lose_c');
	my $v = int( rand(11) + 15 );
	&use_pet('war_result', 0);
	$m{rank_exp} -= int( (rand(21)+20) * $m{value} );
	$m{exp} += $v;

	$mes .= "�����S�łƂ����s���_�Ȕs�k�ׁ̈A$m{name}�ɑ΂���]����������������܂���<br>";
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
	
	$cs{soldier}[$y{country}] += $y{sol} if $y{sol} > 0;
	&down_friendship;

	# �A���œ��������ƍ��m��������
	&refresh;
	if ( ( $w{world} eq '8' && $cs{strong}[$y{country}] <= 3000 ) || ( $w{world} eq '12' && $m{renzoku_c} > rand(4) ) || $m{renzoku_c} > rand(7) + 2 ) {
		&write_world_news("$c_m��$m{name}��$c_y�̘S���ɗH����܂���");
		&add_prisoner;
	}

	&write_cs;
	&n_menu;
}

#=================================================
# �ދp
#=================================================
sub war_escape {
	$mes .= "$m{name}�ɑ΂���]����������܂���<br>";
	$m{rank_exp} -= int( (rand(6)+5) * $m{value} );

	$cs{soldier}[$m{country}] += $m{sol};
	$cs{soldier}[$y{country}] += $y{sol};

	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# ����
#=================================================
sub war_win {
	my $is_single = shift;

	# �D�����ް�:�K���������ق���׽�B������A�v���̎��͊K�����Ⴂ�ق���׽
	my $v = $w{world} eq '2' || $w{world} eq '3' ? (@ranks - $m{rank}) * 10 + 10 : $m{rank} * 8 + 10;

	# ��������Ȃ�����׽������ϲŽ
	$v += ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 10;

	# ����ɂ��D���͑���
	if ($w{world} eq '5' || $w{world} eq '6') { # �\�N�A����
		$v *= 2.5;
	}
	elsif ($w{world} eq '3') { # �v��:�㍑�L��
		my $sum = 0;
		for my $i (1 .. $w{country}) {
			$sum += $cs{win_c}[$i];
		}
		$v *= 2.5 if $cs{win_c}[$m{country}] <= $sum / $w{country};
	}
	elsif ($w{world} eq '2') { # ������:����Ⴂ�l�L��
		if ($m{sedai} < 5) {
			$v *= 3;
		}
		elsif ($m{sedai} < 10) {
			$v *= 2.5;
		}
	}
	else {
		$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
	}
	
	# ��풆�Ȃ�2�{
	my $p_c_c = 'p_' . &union($m{country}, $y{country});
	$v *= 2 if $w{$p_c_c} eq '2';
	
	$v = $v * $m{value} * (rand(0.4)+0.8);
	$v = &use_pet('war_result', $v);
	
	# �D���͏��
	if ($v !~ /^(\d)\1+$/) { # ��ۖ�(����۽�g�p���Ȃ�)
		if ($m{value} < 1) { # �������s
			$v = $v > 200 ? int(rand(100)+100) : int($v);
		}
		else { # �ʏ�E����
			if ($time + 2 * 24 * 3600 > $w{limit_time}) { # ��������c��P��
				$v = $v > 1500 ? int(rand(500)+1000) : int($v);
			}
			else {
				$v = $v > 600  ? int(rand(200)+400) : int($v);
			}
			
			# ����������߂Â��Ă�������׽
			$v += $time + 4 * 24 * 3600 > $w{limit_time} ? 40
			    : $time + 8 * 24 * 3600 > $w{limit_time} ? 20
			    :                                          5
			    ;
		}
	}
	
	# �ŖS���̏ꍇ����
	if ($cs{is_die}[$y{country}]) {
		$v = int($v * 0.5);
		&_penalty
	}
	else {
		$cs{soldier}[$m{country}] += $m{sol};
	}
	# ���̓f�[�^�}
	$cs{strong}[$m{country}] += $v;
	$cs{strong}[$y{country}] -= $v;
	$cs{strong}[$y{country}] = 0  if $cs{strong}[$y{country}] < 0;
	
	$mes .= "$c_y����$v��$e2j{strong}��D���܂���<br>";
	
	if ($is_single) {
		&write_world_news(qq|$c_m��$m{name}��$c_y�ɐN�U�A$y{name}�ƈ�R�����̖���������� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����ɐ���</font>�����悤�ł�|);
	}
	else {
		$m{value} < 1
			? &write_world_news(qq|���҂���$c_y�ɐN�U�A$y{name}�̕��������j�� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����Ƃɐ���</font>�����悤�ł�|)
			: &write_world_news(qq|$c_m��$m{name}��$c_y�ɐN�U�A$y{name}�̕��������j�� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����Ƃɐ���</font>�����悤�ł�|)
			;
	}

	&down_friendship;
	&c_up('win_c');
	++$m{medal};
	my $vv = int( (rand(21)+20) * $m{value} );
	$vv = &use_pet('war_win', $vv);
	$m{exp}      += $vv;
	$m{rank_exp} += int( (rand(11)+20) * $m{value} );
	$m{egg_c}    += int(rand(6)+5) if $m{egg};

	$mes .= "$m{name}�ɑ΂���]�����傫���オ��܂���<br>";
	$mes .= "$vv��$e2j{exp}����ɓ���܂���<br>";
	
	# ڽ���
	&_rescue if -s "$logdir/$y{country}/prisoner.cgi";

	&refresh;

	# �Í�
	if ($w{world} eq $#world_states) {
		if ($cs{strong}[$m{country}] >= $touitu_strong || $cs{strong}[$w{country}] <= 0) {
			&_touitu;
		}
		elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
		elsif ( rand(4) < 1  || ($cs{strong}[$w{country}] < 30000 && rand(3) < 1) ) {
			require './lib/vs_npc.cgi';
			&npc_war;
		}
	}
	# �I��
	elsif ($w{world} eq '14') {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1) {
			&_touitu;
		}
	}
	# ����
	elsif ($cs{strong}[$m{country}] >= $touitu_strong) {
		&_touitu;
	}
	# �ŖS
	elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
		&_metubou;
	}
	# ����
	elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 && !($w{world} eq '10' || $w{world} eq '14') ) {
		&_hukkou;
	}
	# �S��
	elsif ($w{world} eq '8' && $cs{strong}[$y{country}] <= 3000 && rand(3) < 1) {
		my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 100  );
		&write_world_news("<b>سާ���݂̑嗒�I$cs{name}[$m{country}]��$cs{name}[$y{country}]��$e2j{$kkk}�� $vvv �D���܂���</b>");
	}

	&daihyo_c_up('war_c'); # ��\�n���x
	&write_cs;

	&n_menu;
}

#=================================================
# �S���ɒ��Ԃ�����Ȃ�~�o
#=================================================
sub _rescue {
	my $is_rescue = 0;
	my @lines = ();
	my $count = 0;
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country) = split /<>/, $line;
		if ($count < $max_rescue && ($country eq $m{country} || $union eq $country) ) {
			$mes .= "$c_y�ɕ߂炦���Ă���$name���~�o���܂���<br>";
			$is_rescue = 1;
			&write_world_news("$c_m��$m{name}��$c_y�ɕ߂炦���Ă���$name�̋~�o�ɐ������܂���");
			
			# ڽ����׸ލ쐬
			my $y_id = unpack 'H*', $name;
			if (-d "$userdir/$y_id") {
				open my $fh2, "> $userdir/$y_id/rescue_flag.cgi" or &error("$userdir/$y_id/rescue_flag.cgi̧�ق����܂���");
				close $fh2;
			}
			++$count;
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rescue) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
}

#=================================================
# ����
#=================================================
sub _touitu {
	&c_up('hero_c');
	if ($union) {
		$w{win_countries} = "$m{country},$union";
		++$cs{win_c}[$union];
	}
	else {
		$w{win_countries} = $m{country};
	}
	++$cs{win_c}[$m{country}];
	
	if ($w{world} eq $#world_states) {
		if ($m{country} eq $w{country} || $union eq $w{country}) { # NPC�����̏���
			&mes_and_world_news("<em>�����B�̗���҂Ƃ���$world_name�嗤���x�z���邱�Ƃɐ������܂���</em>",1);
			&write_legend('touitu', "�[���ł��ڊo�߂�$cs{name}[$w{country}]�̖ҎҒB��$m{name}��M���Ƃ�$world_name�嗤���x�z����");
			$is_npc_win = 1;
		}
		else {
			&mes_and_world_news("<em>���E���Ăѕ��󂵁A$world_name�嗤�ɂЂƂƂ��̈��炬�����Ƃ���܂���</em>",1);
			&write_legend('touitu', "$c_m��$m{name}�Ƃ��̒��ԒB�����E���Ăѕ��󂵁A$world_name�嗤�ɂЂƂƂ��̈��炬�����Ƃ����");
		}
	}
	else {
		if ($union) {
			$mes .= "<em>$world_name�嗤�𓝈ꂵ�܂���</em>";
			&write_world_news("<em>$c_m$cs{name}[$union]������$m{name}��$world_name�嗤�𓝈ꂵ�܂���</em>",1);
			&write_legend('touitu', "$c_m$cs{name}[$union]������$m{name}��$world_name�嗤�𓝈ꂷ��")
		}
		else {
			&mes_and_world_news("<em>$world_name�嗤�𓝈ꂵ�܂���</em>",1);
			&write_legend('touitu', "$c_m��$m{name}��$world_name�嗤�𓝈ꂷ��");
		}
	}

	require "./lib/reset.cgi";
	&reset;

	$m{lib} = 'world';
	$m{tp}  = 100;
	
}

#=================================================
# ����
#=================================================
sub _hukkou {
	&c_up('huk_c');
	$cs{is_die}[$m{country}] = 0;
	&mes_and_world_news("<b>$c_m�𕜋������邱�Ƃɐ������܂���</b>", 1);
	
	--$w{game_lv};
#	--$w{game_lv} if $time + 7 * 24 * 3600 > $w{limit_time};
}

#=================================================
# �ŖS
#=================================================
sub _metubou {
	&c_up('met_c');
	$cs{strong}[$y{country}] = 0;
	$cs{is_die}[$y{country}] = 1;
	&mes_and_world_news("<b>$c_y��łڂ��܂���</b>", 1);

	# ����Down
	for my $k (qw/food money soldier/) {
		$cs{$k}[$y{country}] = int( $cs{$k}[$y{country}] * ( rand(0.3)+0.3 ) );
	}
	
	# ����ԕω�
	for my $i (1 .. $w{country}) {
		$cs{state}[$i] = int(rand(@country_states));
	}
}
#=================================================
# �ŖS�����獑�͂�D�悵�����̔���
#=================================================
sub _penalty {
	# �ЊQ
	if ( ($w{world} eq '13' && rand(3) < 1) || rand(12) < 1 ) {
		&disaster;
	}
}

#=================================================
# �F�D�xDown
#=================================================
sub down_friendship {
	my $c_c = &union($m{country}, $y{country});
	$w{'f_'.$c_c} -= 1;
	if ($w{'p_'.$c_c} ne '2' && $w{'f_'.$c_c} < 10) {
		$w{'p_'.$c_c} = 2;
		&write_world_news("<b>$c_m��$m{name}�̐i�R�ɂ��$c_y�ƌ���ԂɂȂ�܂���</b>");
	}
	$w{'f_'.$c_c} = int(rand(20)) if $w{'f_'.$c_c} < 1;
}


1; # �폜�s��
