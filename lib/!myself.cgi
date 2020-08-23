require "$datadir/skill.cgi";
require "$datadir/pet.cgi";
#=================================================
# �ð����� Created by Merino
#=================================================

# �ƭ� ���ǉ�/�ύX/�폜/���בւ��\
my @menus = (
	['��߂�',		'main'],
	['�ڸ���ٰ�',	'myself_collection'],
	['��ٌp��',		'myself_skill'],
	['�̍���ύX',	'myself_shogo'],
	['��̂�ύX',	'myself_mes'],
	['���ȏЉ�',	'myself_profile'],
	['���l�̂��X',	'myself_shop'],
	['ϲ�߸��',		'myself_picture'],
	['ϲ�ޯ�',		'myself_book'],
	['���l�̋�s',	'myself_bank'],
	['�l�ݒ�',	'myself_config'],
);


#================================================
sub begin {
	$layout = 2;
	$is_mobile ? &my_status_mobile : &my_status_pc;
	&menu(map{ $_->[0] }@menus);
}
sub tp_1 {
	# �߯Ďg�p
	if ($in{mode} eq 'use_pet' && $m{pet} && $pets[$m{pet}][2] eq 'myself') {
		&refresh;
		&n_menu;

		# �����Ȃ̏ꍇ
		if ($m{pet} >= 128 && $m{pet} <= 130) {
			$mes .= "$pets[$m{pet}][1]�́A$m{name}�̂��Ƃ������ƌ��Ă���c<br>";
			$m{lib} = 'add_monster';
			$m{tp}  = 100;
		}
		else {
			&{ $pets[$m{pet}][3] };
			$mes .= "��ڂ��I���� $pets[$m{pet}][1] �͌��̔ޕ��֏����Ă������c<br>";
			$m{pet} = 0;
		}
	}
	else {
		&b_menu(@menus);
	}
}


#================================================
# �g�їp�ð���\��
#================================================
sub my_status_mobile {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;

	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= "[$skills[$m_skill][2]]$skills[$m_skill][1] ����$e2j{mp} $skills[$m_skill][3]<br>";
	}

	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_ag  = '';
	if ($m{wea}) {
		$mes .= qq|<hr>�y������z<br><ul>|;
		$mes .= qq|<li>���O:$weas[$m{wea}][1]|;
		$mes .= qq|<li>����:$weas[$m{wea}][2]|;
		$mes .= qq|<li>����:$weas[$m{wea}][3]|;
		$mes .= qq|<li>�ϋv:$weas[$m{wea}][4]|;
		$mes .= qq|<li>�d��:$weas[$m{wea}][5]</ul><hr>|;
		if    ($weas[$m{wea}][2] =~ /��|��|��|��/) { $sub_at  = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /��|��|��/)    { $sub_mat = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }
	}

	if ($m{pet}) {
		$mes .= qq|�y�߯ď��z<br><ul>|;
		$mes .= qq|<li>���O:$pets[$m{pet}][1]|;
		$mes .= qq|<li>����:$pet_effects[$m{pet}]</ul>|;
		if ($pets[$m{pet}][2] eq 'myself') {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="�߯Ă��g�p����" class="button1"></form>|;
		}
		$mes .= qq|<hr>|;
	}

	my $m_st = &m_st;
	$mes .=<<"EOM";
		<b>$m{sedai}</b>�����<br>
		$sexes[ $m{sex} ] [$jobs[$m{job}][1]]<br>
		�M�� <b>$m{medal}</b>��<br>
		���ɺ�� <b>$m{coin}</b>��<br>
		��ށy$m{lot}�z<br>
		<hr>
		�y�ð���z����:$m_st<br>
		$e2j{max_hp} [<b>$m{max_hp}</b>]/$e2j{max_mp} [<b>$m{max_mp}</b>]/<br>
		$e2j{at} [<b>$m{at}</b>$sub_at]/$e2j{df} [<b>$m{df}</b>]/<br>
		$e2j{mat} [<b>$m{mat}</b>$sub_mat]/$e2j{mdf} [<b>$m{mdf}</b>]/<br>
		$e2j{ag} [<b>$m{ag}</b>$sub_ag]/$e2j{cha} [<b>$m{cha}</b>]/<br>
		$e2j{lea} [<b>$m{lea}</b>]<br>
		<hr>
		�y�o���Ă���Z�z<br>
		 $skill_info
		<hr>
		�y�n���x�z<br>
		�_�� <b>$m{nou_c}</b>/���� <b>$m{sho_c}</b>/���� <b>$m{hei_c}</b>/�O�� <b>$m{gai_c}</b>/�ҕ� <b>$m{mat_c}</b>/<br>
		���D <b>$m{gou_c}</b>/���� <b>$m{cho_c}</b>/���] <b>$m{sen_c}</b>/�U�v <b>$m{gik_c}</b>/��@ <b>$m{tei_c}</b>/<br>
		�C�s <b>$m{shu_c}</b>/���� <b>$m{tou_c}</b>/���Z <b>$m{col_c}</b>/���� <b>$m{cas_c}</b>/<br>
		���� <b>$m{hero_c}</b>/���� <b>$m{huk_c}</b>/�ŖS <b>$m{met_c}</b>/<br>
		<hr>
		�y��\\���߲�āz<br>
		�푈 <b>$m{war_c}</b>/���� <b>$m{dom_c}</b>/�R�� <b>$m{mil_c}</b>/�O�� <b>$m{pro_c}</b>/
		<hr>
		�y����z<br>
		<b>$war_c</b>�� <b>$m{win_c}</b>�� <b>$m{lose_c}</b>�� <b>$m{draw_c}</b>��<br>
		���� <b>$win_par</b>%
EOM
}

#================================================
# PC�p�ð���\��
#================================================
sub my_status_pc {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;

	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= qq|<tr><td align="center">$skills[$m_skill][2]</td><td>$skills[$m_skill][1]</td><td align="right">$skills[$m_skill][3]<br></td></tr>|;
	}

	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_ah  = '';
	if ($m{wea}) {
		$mes .= qq|<hr>�y������z<br>|;
		$mes .= qq|<table class="table1" cellpadding="3"><tr>|;
		$mes .= qq|<th>���O</th><td>$weas[$m{wea}][1]</td>|;
		$mes .= qq|<th>����</th><td>$weas[$m{wea}][2]</td>|;
		$mes .= qq|<th>����</th><td>$weas[$m{wea}][3]</td>|;
		$mes .= qq|<th>�ϋv</th><td>$weas[$m{wea}][4]</td>|;
		$mes .= qq|<th>�d��</th><td>$weas[$m{wea}][5]</td>|;
		$mes .= qq|</tr></table><hr size="1">|;
		if    ($weas[$m{wea}][2] =~ /��|��|��|��/) { $sub_at  = "��$weas[$m{wea}][3]"; $sub_ag = "��$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /��|��|��/)    { $sub_mat = "��$weas[$m{wea}][3]"; $sub_ag = "��$weas[$m{wea}][5]"; }
	}

	if ($m{pet}) {
		$mes .= qq|�y�߯ď��z<br>|;
		$mes .= qq|<table class="table1" cellpadding="3">|;
		$mes .= qq|<tr><th>���O</th><td>$pets[$m{pet}][1]</td>|;
		$mes .= qq|<th>����</th><td>$pet_effects[$m{pet}]</td></tr>|;
		$mes .= qq|</table>|;
		if ($pets[$m{pet}][2] eq 'myself') {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="�߯Ă��g�p����" class="button1"></form>|;
		}
		$mes .= qq|<hr size="1">|;
	}

	my $m_st = &m_st;
	$mes .= <<"EOM";
		�y�ð���z�����F$m_st<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>$e2j{max_hp}</th><td align="right">$m{max_hp}</td>
			<th>$e2j{at}</th><td align="right">$m{at}$sub_at</td>
			<th>$e2j{df}</th><td align="right">$m{df}</td>
		</tr><tr>
			<th>$e2j{max_mp}</th><td align="right">$m{max_mp}</td>
			<th>$e2j{mat}</th><td align="right">$m{mat}$sub_mat</td>
			<th>$e2j{mdf}</th><td align="right">$m{mdf}</td>
		</tr><tr>
			<th>$e2j{lea}</th><td align="right">$m{lea}</td>
			<th>$e2j{ag}</th><td align="right">$m{ag}$sub_ag</td>
			<th>$e2j{cha}</th><td align="right">$m{cha}</td>
		</tr>
		</table>
		<hr size="1">
		�y�o���Ă���Z�z<br>
		<table class="table1" cellpadding="3">
		<tr><th>����</th><th>�Z��</th><th>����$e2j{mp}</th></tr>
		$skill_info
		</table>

		<hr size="1">
		�y�n���x�z<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>�_��</th><td align="right">$m{nou_c}</td>
			<th>����</th><td align="right">$m{sho_c}</td>
			<th>����</th><td align="right">$m{hei_c}</td>
			<th>�O��</th><td align="right">$m{gai_c}</td>
			<th>�ҕ�</th><td align="right">$m{mat_c}</td>
		</tr>
		<tr>
			<th>���D</th><td align="right">$m{gou_c}</td>
			<th>����</th><td align="right">$m{cho_c}</td>
			<th>���]</th><td align="right">$m{sen_c}</td>
			<th>�U�v</th><td align="right">$m{gik_c}</td>
			<th>��@</th><td align="right">$m{tei_c}</td>
		</tr>
		<tr>
			<th>�C�s</th><td align="right">$m{shu_c}</td>
			<th>����</th><td align="right">$m{tou_c}</td>
			<th>���Z</th><td align="right">$m{col_c}</td>
			<th>����</th><td align="right">$m{cas_c}</td>
			<th>����</th><td align="right">$m{mon_c}</td></tr>
		<tr>
			<th>����</th><td align="right">$m{hero_c}</td>
			<th>����</th><td align="right">$m{huk_c}</td>
			<th>�ŖS</th><td align="right">$m{met_c}</td>
			<th>�@</th><td align="right">�@</td>
			<th>�@</th><td align="right">�@</td>
		</tr>
		</table>

		<hr size="1">
		�y��\\���߲�āz<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>�푈</th><td align="right">$m{war_c}</td>
			<th>����</th><td align="right">$m{dom_c}</td>
			<th>�R��</th><td align="right">$m{mil_c}</td>
			<th>�O��</th><td align="right">$m{pro_c}</td>
		</tr>
		</table>

		<hr size="1">
		�y����z<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>���</th><td align="right">$war_c</td>
			<th>����</th><td align="right">$m{win_c}</td>
			<th>����</th><td align="right">$m{lose_c}</td>
			<th>����</th><td align="right">$m{draw_c}</td>
			<th>����</th><td align="right">$win_par %</td>
		</tr>
		</table>
EOM
}


1; # �폜�s��
