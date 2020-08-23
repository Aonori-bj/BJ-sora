$is_battle = 2;  # �����׸�2
sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
#================================================
# �푈 Created by Merino
#================================================
# $m{value} �ɂ� ���m�̔{��

# ��R�ł��̎��̑���̾�́B��Ԑ擪�������f��p�̾��(�����\)
my @answers = ('�f��!', '�]�ނƂ��낾!', '�Ԃ蓢���ɂ��Ă����!', '��������!', '�悩�낤!', '�������낤!', '����ɂȂ낤!', '�������Ă���!');

# �w�`��(�����s�B���O�̕ύX�\)
my @war_forms = ('�U���w�`','�h��w�`','�ˌ��w�`');


#================================================
# ���p����
#================================================
sub is_satisfy {
	if ($time < $w{reset_time}) {
		$mes .= '�I����ԂȂ̂Ő푈�𒆎~���܂�<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (!defined $cs{strong}[$y{country}]) {
		$mes .= '�U�߂Ă��鍑�͏��ł��Ă��܂����̂ŁA�푈�𒆎~���܂�<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub tp_100 {
	$mes .= "$c_y�ɒ����܂���<br>";
	
	my $is_ambush = &_get_war_you_data; # �҂���������Ă��ꍇ�߂�l����
	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};

	# ���E��ݐ�����
	$m{turn} = int( rand(6)+7 );
	if ($m{value} > 1) {
		$m{turn} += 3;
		$y{sol} = int($rank_sols[$y{rank}]);
	}
	else {
		$y{sol} = int($rank_sols[$y{rank}] * $m{value});
	}

	# ��������Ȃ�
	if ($y{sol} > $cs{soldier}[$y{country}]) {
		$mes .= "$c_y�͕��s���̂悤���c<br>�ً}�Ɋ񂹏W�߂̍��������W���ꂽ<br>";
		$cs{strong}[$y{country}] -= int(rand(100)+100);
		$cs{strong}[$y{country}] = 1 if $cs{strong}[$y{country}] < 1;
		$y{sol_lv} = int( rand(10) + 45 );
		&write_cs;
	}
	else {
		$cs{soldier}[$y{country}] -= $y{sol};
		$y{sol_lv} = 80;
	}

	# �҂�����
	if ($pets[$m{pet}][2] ne 'no_ambush' && $is_ambush) {
		$mes .= "$c_y��$y{name}������$y{sol}��$units[$y{unit}][1]���҂��������Ă��܂���!<br>";
		if ($y{unit} eq '11') { # �ÎE����
			my $v = int( $m{sol} * (rand(0.2)+0.2) );
			$m{sol} -= $v;
			$m{sol_lv} = int( rand(15) + 15 ); # 15 �` 29
			$mes .= "$units[$y{unit}][1]�ɂ��ÎE�ŁA$v�̕�������܂���!<br>";
		}
		elsif ($y{unit} eq '14') { # ���e����
			$m{sol_lv} = int( rand(10) + 5 ); # 5 �` 14
			$mes .= "$units[$y{unit}][1]�ɂ�錶�p�ŁA���m�B�͍������傫���m�C��������܂���!<br>";
		}
		else {
			$m{sol_lv} = int( rand(15) + 10 ); # 10 �` 24
			$mes .= "�҂������ɂ�蕺�m�B�͍������傫���m�C��������܂���!<br>";
		}
		&write_world_news("$c_m��$m{name}��$c_y�ɍU�ߍ���$y{name}�̑҂������ɂ����܂���");

		my $yid = unpack 'H*', $y{name};
		if (-d "$userdir/$yid") {
			open my $fh, ">> $userdir/$yid/ambush.cgi";
			print $fh "$m{name}/$ranks[$m{rank}]/$units[$m{unit}][1]/����$m{lea}($date)<>";
			close $fh;
		}
	}
	else {
		$m{sol_lv} = 80;
		$mes .= "$c_y����$y{name}������$y{sol}�̕����o�Ă��܂���<br>";
	}

	# ���R�n�߯�
	if ($pets[$m{pet}][2] eq 'war_begin') {
		&use_pet('war_begin');
	}
	# �������Ă��鍑����̉��R
	elsif ($union) {
		my $v = int( $m{sol} * (rand(0.1)+0.1) );
		$m{sol} += $v;
		$mes .= "�Ȃ�ƁA$cs{name}[$union]����$v���̉��R���삯����!<br>";
	}
	
	$m{tp} += 10;
	&n_menu;
}

#================================================
sub tp_110 {
	$is_battle = 2;
	$m{act} += int(rand($m{turn})+$m{turn});
	
	$mes .= "����̍��̌��E��݂� $m{turn} ��݂ł�<br>";
	$mes .= "$m{name}�R $m{sol}�l VS $y{name}�R $y{sol}�l<br>";
	$mes .= '�U�ߍ��ސw�`��I��ł�������<br>';
	&menu(@war_forms,'�ދp');
	
	$m{tp} += 10;
	&write_cs;
}

#================================================
sub tp_120 { &tp_190; } # tp120���Ƒދp��
sub tp_130 { &tp_190; } # tp130���ƈ�R�ł���
sub tp_140 { # ��R�ł�
	require './lib/battle.cgi';

	if ($m{hp} <= 0) {
		$mes .= "��R�ł��ɔs��w������������$m{name}�̕����͐�ӂ�r�����A�G�R����̒ǌ��������S�ł��܂����c<br>";
		&write_world_news("$c_m��$m{name}��$c_y�ɐN�U�A$y{name}�ƈ�R�����������邪�s�k�������͔s�������悤�ł�");
		&war_lose;
	}
	elsif ($y{hp} <= 0) {
		$mes .= "�G�R��$y{name}�̔s�k�ɐ�ӂ�r�����܂����I���������������ȂǓG�ł͂���܂���<br>�G�R��ǌ����A���Ȃ�̔�Q��^���܂����I<br>";
		&war_win(1);
	}
}

#================================================
# ٰ���ƭ� ��ݏI�������������邩�܂�
#================================================
sub loop_menu {
	$is_battle = 2;
	$mes .= "�c��$m{turn} ���<br>";
	$mes .= "$m{name}�R $m{sol}�l VS $y{name}�R $y{sol}�l<br>";
	$mes .= '�U�ߍ��ސw�`��I��ł�������<br>';
	&menu(@war_forms);
}

sub tp_190 {
	if ($cmd >= 0 && $cmd <= 2) {
		--$m{turn};
		$mes .= "�c��$m{turn}���<br>";
		&_crash;
		
		if ($m{sol} <= 0 && $y{sol} <= 0) {
			$mes .= "���R�Ƃ��ɉ�œI���Q���󂯐퓬�p�����s�\\�ƂȂ�܂���<br>$e2j{strong}�͗��w�c�Ƃ��ω��Ȃ�<br>";
			$m{value} < 1
				? &write_world_news("���҂���$c_y�ɐN�U�A$y{name}�̕����ɑj�܂ꌃ��̖��A���R��ł����悤�ł�")
				: &write_world_news("$c_m��$m{name}��$c_y�ɐN�U�A$y{name}�̕����ɑj�܂ꌃ��̖��A���R��ł����悤�ł�")
				;

			&war_draw;
		}
		elsif ($m{sol} <= 0) {
			$mes .= '�䂪�R�͑S�ł��܂����B�P�ނ��܂��c<br>';
			$m{value} < 1
				? &write_world_news("���҂���$c_y�ɐN�U�A$y{name}�̕����̑O�ɔs�ނ����悤�ł�")
				: &write_world_news("$c_m��$m{name}��$c_y�ɐN�U�A$y{name}�̕����̑O�ɔs�ނ����悤�ł�")
				;

			&war_lose;
		}
		elsif ($y{sol} <= 0) {
			$mes .= '�G���������j���܂���!!�䂪�R�̏����ł�!<br>';
			&war_win;
		}
		elsif ($m{turn} <= 0) {
			$mes .= "�퓬���E��݂𒴂��Ă��܂����c����ȏ�͐킦�܂���<br>$e2j{strong}�͗��w�c�Ƃ��ω��Ȃ�<br>";
			$m{value} < 1
				? &write_world_news("���҂���$c_y�ɐN�U���A$y{name}�̕����ɑj�܂�퓬���E���ް�����悤�ł�")
				: &write_world_news("$c_m��$m{name}��$c_y�ɐN�U���A$y{name}�̕����ɑj�܂�퓬���E���ް�����悤�ł�")
				;

			&war_draw;
		}
		else {
			$mes .= '�U�ߍ��ސw�`��I��ł�������<br>';
			
			# ��R�ł��o���m��
			if ( ($pets[$m{pet}][2] eq 'war_single' && int(rand($m{turn}+3)) == 0) || int(rand($m{turn}+15)) == 0 ) {
				&menu(@war_forms,'��R�ł�');
				$m{tp} = 130;
			}
			elsif ($m{turn} < 4)  {
				&menu(@war_forms);
			}
			else {
				&menu(@war_forms,'�ދp');
				$m{tp} = 120;
			}
		}
	}
	elsif ($cmd eq '3' && $m{tp} eq '120') {
		$m_mes = '�S�R�ދp!!';
		
		if ($m{turn} < 5) {
			$mes .= '�G�R�ɓ����ޘH���ǂ���A���͂�P�ނ͕s�\\�ł�<br>';
			$m{tp} = 190;
			&loop_menu;
		}
		# �ދp�ł���m��
		elsif ( int(rand($m{turn})) == 0) {
			$mes .= '�c�O�ł������𒆎~���ދp���܂�<br>';
			$m{value} < 1
				? &write_world_news("���҂���$c_y�ɐN�U���A$y{name}�̕����ƌ��B�]�V�Ȃ��P�ނ����͗l")
				: &write_world_news("$c_m��$m{name}��$c_y�ɐN�U���A$y{name}�̕����ƌ��B�]�V�Ȃ��P�ނ����͗l")
				;

			&war_escape;
		}
		else {
			$mes .= '�ދp�Ɏ��s���܂���<br>';
			$m{tp} = 190;
			&loop_menu;
		}
	}
	elsif ($cmd eq '3' && $m{tp} eq '130') {
		$m_mes = "$y{name}�ƈ�R�ł��肢����!";

		my $v = int(rand(@answers));

		if ($v <= 0) {
			$y_mes = $answers[$v];
			$mes .= '��R�ł���f���܂���<br>';
			&loop_menu;
			$m{tp} = 190;
		}
		else {
			$y_mes = $answers[$v];
			
			$mes .= "$y{name}�Ɉ�R�ł���\\�����݁A���̐킢�̏��s���˂�����R�������s�Ȃ�����!<br>";
			$m{tp} = 140;
			&n_menu;
		}
	}
	else {
		&loop_menu;
		$m{tp} = 190;
	}
}

#================================================
# �w�`�팋��
#================================================
sub _crash {
	my $y_cmd = int(rand(3));
	
	$m_mes = $war_forms[$cmd];
	$y_mes = $war_forms[$y_cmd];
	
	my $result = 'draw';
	if ($cmd eq '0') {
		$result = $y_cmd eq '1' ? 'win'
				: $y_cmd eq '2' ? 'lose'
				:				  'draw'
				;
	}
	elsif ($cmd eq '1') {
		$result = $y_cmd eq '2' ? 'win'
				: $y_cmd eq '0' ? 'lose'
				:				  'draw'
				;
	}
	elsif ($cmd eq '2') {
		$result = $y_cmd eq '0' ? 'win'
				: $y_cmd eq '1' ? 'lose'
				:				  'draw'
				;
	}
	
	my $m_attack = ($m{sol}*0.1 + $m{lea}*2) * $m{sol_lv} * 0.01 * $units[$m{unit}][4] * $units[$y{unit}][5];
	my $y_attack = ($y{sol}*0.1 + $y{lea}*2) * $y{sol_lv} * 0.01 * $units[$y{unit}][4] * $units[$m{unit}][5];

	if (&is_tokkou($m{unit}, $y{unit})) {
		$is_m_tokkou = 1;
		$m_attack *= 1.3;
		$y_attack *= 0.5;
	}
	if (&is_tokkou($y{unit}, $m{unit})) {
		$is_y_tokkou = 1;
		$m_attack *= 0.5;
		$y_attack *= 1.3;
	}
	$m_attack = $m_attack < 150 ? int( rand(50)+100 ) : int( $m_attack * (rand(0.3) +0.9) );
	$y_attack = $y_attack < 150 ? int( rand(50)+100 ) : int( $y_attack * (rand(0.3) +0.9) );
	
	if ($result eq 'win') {
		$m_attack = int($m_attack * 1.3);
		$y_attack = int($y_attack * 0.5);
		
		$m{sol_lv} += int(rand(5)+10);
		$y{sol_lv} -= int(rand(5)+10);

		$mes .= qq|�����R��Q$y_attack <font color="#FF0000">���G�R��Q$m_attack</font><br><br>|;
	}
	elsif ($result eq 'lose') {
		$m_attack = int($m_attack * 0.5);
		$y_attack = int($y_attack * 1.3);
		$m{sol_lv} -= int(rand(5)+10);
		$y{sol_lv} += int(rand(5)+10);
	
		$mes .= qq|<font color="#FF0000">�����R��Q$y_attack</font> ���G�R��Q$m_attack<br><br>|;
	}
	else {
		$m{sol_lv} += int(rand(3)+5);
		$y{sol_lv} += int(rand(3)+5);
	
		$mes .= qq|�����R��Q$y_attack ���G�R��Q$m_attack<br><br>|;
	}
	
	$m{sol} -= $y_attack;
	$y{sol} -= $m_attack;
	$m{sol} = 0 if $m{sol} < 0;
	$y{sol} = 0 if $y{sol} < 0;

	$m{sol_lv} = $m{sol_lv} < 10  ? int( rand(11) )
			   : $m{sol_lv} > 100 ? 100
			   :					$m{sol_lv}
			   ;
	$y{sol_lv} = $y{sol_lv} < 10  ? int( rand(11) )
			   : $y{sol_lv} > 100 ? 100
			   :					$y{sol_lv}
			   ;
}


#================================================
# �K���Ɠ������������炢�̑���������_���ŒT���B������Ȃ��ꍇ�͗p�ӂ��ꂽNPC
#================================================
sub _get_war_you_data {
	my @lines = &get_country_members($y{country});
	
	if (@lines >= 1) {
		my $retry = $w{world} eq '8' && $cs{strong}[$y{country}] <= 3000      ? 0 # ���E��y�S�ǁz�U�߂����̍��͂�3000�ȉ��̏ꍇ�͋���NPC
				  : $w{world} eq $#world_states && $y{country} eq $w{country} ? 1 # ���E��y�Í��z�U�߂�����NPC���Ȃ���ڲ԰ϯ�ݸނ͂P��
				  :																5 # ���̑���ڲ԰ϯ�ݸނ��ō��T��ق���ײ����
				  ;
		my %sames = ();
		for my $i (1 .. $retry) {
			my $c = int(rand(@lines));
			next if $sames{$c}++; # �����l�Ȃ玟
			
			$lines[$c] =~ tr/\x0D\x0A//d; # = chomp �]���ȉ��s�폜
			
			my $y_id = unpack 'H*', $lines[$c];
			
			# ���Ȃ��ꍇ��ؽĂ���폜
			unless (-f "$userdir/$y_id/user.cgi") {
				require "./lib/move_player.cgi";
				&move_player($lines[$c], $y{country},'del');
				next;
			}
			
			my %you_datas = &get_you_datas($y_id, 1);
			
			next if $you_datas{lib} eq 'prison'; # �S���̐l�͏���
			next if $you_datas{lib} eq 'war'; # �푈�ɏo�Ă���l�͏���
			
			# �҂��������Ă���l��������
			if ( $you_datas{value} eq 'ambush' && $max_ambush_hour * 3600 + $you_datas{ltime} > $time) {
				# set %y
				while (my($k,$v) = each %you_datas) {
					next if $k =~ /^y_/;
					$y{$k} = $v;
				}
				$y_mes = $you_datas{mes};
				return 1;
			}
			# �K���Ɠ������߂��l�B���̐�����0�ɂ���΂�苭���̋߂�����傫������ΐF�X�ȑ���
			elsif ( 2 >= rand(abs($m{rank}-$you_datas{rank})+2) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
				# set %y
				while (my($k,$v) = each %you_datas) {
					next if $k =~ /^y_/;
					$y{$k} = $v;
				}
				$y_mes = $you_datas{mes};
				return 0;
			}
		}
	}
	
	# �ެ�޳ or NPC
	$pets[$m{pet}][2] eq 'no_shadow' || int(rand(3)) == 0 || $w{world} eq '8'
		? &_get_war_npc_data : &_get_war_shadow_data;
}

#================================================
# NPC [0] �` [4] �� 5�l([0]���� >>> [4]�ア)
#================================================
sub _get_war_npc_data {
	&error("���荑($y{country})��NPC�f�[�^������܂���") unless -f "$datadir/npc_war_$y{country}.cgi";
	
	require "$datadir/npc_war_$y{country}.cgi";
	
	my $v = $m{lea} > 600 ? 0
		  : $m{lea} > 400 ? int(rand(2))
		  : $m{lea} > 250 ? int(rand(2)+1)
		  : $m{lea} > 120 ? int(rand(2)+2)
		  :                 int(rand(2)+3)
		  ;

	# ���ꍑ�̏ꍇ��NPC���
	my($c1, $c2) = split /,/, $w{win_countries};
	# ���͒Ⴂ�ꍇ�͋���NPC
	if ($cs{strong}[$y{country}] <= 3000) {
		$v = 0;
	}
	elsif ($c1 eq $y{country} || $c2 eq $y{country}) {
		$v += 1;
	}
	$v = $#npcs if $v > $#npcs;
	
	while ( my($k, $v) = each %{ $npcs[$v] }) {
		$y{$k} = $v;
	}
	$y{unit} = int(rand(@units));
	$y{icon} ||= $default_icon;
	$y{mes_win} = $y{mes_lose} = '';

	return 0;
}

#================================================
# ���޳
#================================================
sub _get_war_shadow_data {
	# ���͒Ⴂ�ꍇ��1.5�{
	my $pinch = $cs{strong}[$y{country}] <= 3000 ? 1.5 : 1;
	
	for my $k (qw/max_hp max_mp at df mat mdf ag cha lea/) {
		$y{$k} = int($m{$k} * $pinch);
	}
	for my $k (qw/wea skills mes_win mes_lose icon rank unit/) {
		$y{$k} = $m{$k};
	}
	$y{rank} += 2;
	$y{rank} = $#ranks if $y{rank} > $#ranks;

	# ���ꍑ�̏ꍇ��NPC���
	my($c1, $c2) = split /,/, $w{win_countries};
	$y{rank} -= 2 if $c1 eq $y{country} || $c2 eq $y{country};

	$y{name}  = '���޳�R�m(NPC)';
	
	return 0;
}


#================================================
# ���킪���U(�L��)���ǂ���
#================================================
sub is_tokkou {
	my($m_unit, $y_unit) = @_;
	
	for my $tokkou (@{ $units[$m_unit][6] }) {
		return 1 if $tokkou eq $y_unit;
	}
	return 0;
}


#================================================
# _war_result.cgi�ɏ������ʂ�n��
#================================================
sub war_win {
	my $is_single = shift;
	require "./lib/_war_result.cgi";
	&war_win($is_single);
}
sub war_lose {
	require "./lib/_war_result.cgi";
	&war_lose;
}
sub war_draw {
	require "./lib/_war_result.cgi";
	&war_draw;
}
sub war_escape {
	require "./lib/_war_result.cgi";
	&war_escape;
}


1; # �폜�s��