#================================================
# �ް�(bj.cgi)�ł悭�g������ Created by Merino
#================================================

#================================================
# �� + ���E �f�[�^�������� ./log/countries.cgi�ɏ�������
#================================================
sub write_cs {
	&error("���ް��̏������݂Ɏ��s���܂���") if $cs{name}[1] eq '';

	# �ϐ��ǉ�����ꍇ�͔��p��߰������s�����Ēǉ�(���s���A���בւ���)
	my @keys = (qw/
		name bbs_name prison_name strong barrier tax food money soldier state is_die member capacity color
		win_c old_ceo ceo war dom mil pro war_c dom_c mil_c pro_c ceo_continue
		modify_war modify_dom modify_mil modify_pro
		extra extra_limit disaster disaster_limit
		new_commer
	/);
	# �����@�����́@��ǒl�@�ŗ��@�����Ɓ@���Ɨ\�Z�@�����m���@��ԁ@�ŖS�׸ށ@�����l���@����@���F
	# ���ꐔ�@����\�ҁ@��\�ҁ@�Q�d�@�������@��m�@�O�����@�Q�d�߲�ā@�������߲�ā@��m�߲�ā@�O�����߲�ā@��\�N��
	# �e���ݒ�푈�@�����@�R���@�O��
	# �ǉ����ʁ@�ǉ����ʊ����@���ʍЊQ�@���ʍЊQ�L������
	# �V�K��

	# -------------------
	# �����̍ő�l
	my $max_resource = $w{world} eq '15' ? 300000 : 999999; # ���E�[��E�E�Ȃ�500000�܂�]
	$cs{food}[$m{country}]    = $max_resource if $cs{food}[$m{country}]    > $max_resource;
	$cs{money}[$m{country}]   = $max_resource if $cs{money}[$m{country}]   > $max_resource;
	$cs{soldier}[$m{country}] = $max_resource if $cs{soldier}[$m{country}] > $max_resource;

	my $world_line = &_get_world_line; # ���E���
	my @lines = ($world_line);
	for my $i (1 .. $w{country}) {
		my $line;
		for my $k (@keys) {
			$line .= "$k;$cs{$k}[$i]<>";
		}
		push @lines, "$line\n";
	}

	open my $fh, "> $logdir/countries.cgi" or &error("���f�[�^���J���܂���");
	print $fh @lines;
	close $fh;
}

#================================================
# ���E���
#================================================
sub _get_world_line { # Get %w line
	# �ϐ��ǉ�����ꍇ�͔��p��߰������s�����Ēǉ�(���s���A���בւ���)
	my @keys = (qw/
		country year game_lv limit_time reset_time win_countries player world playing world_sub sub_time twitter_bot half_hour_time
	/);
	# ���̐��@�N�@��Փx�@��������@ؾ�Ă��ꂽ���ԁ@�O��̓��ꍑ(����)�@��ڲ԰�l���@���E��@��ڲ���l���@�T�u��@�T�u���ԁ@twitter�p�J�E���g�@�T�u���Ԃ�0.5���Ԕ�

	my $line = '';
	for my $k (@keys) {
		$line .= "$k;$w{$k}<>";
	}

	# -------------------
	# �F�D�x/���
	for my $i (1 .. $w{country}) {
		for my $j ($i+1 .. $w{country}) {
			my $f_c_c  = "f_${i}_${j}";
			my $p_c_c = "p_${i}_${j}";
			$line .= "$f_c_c;$w{$f_c_c}<>";
			$line .= "$p_c_c;$w{$p_c_c}<>";
		}
	}
	$line .= "\n";

	return $line;
}

#================================================
# ��ڲ԰�ް���������
#================================================
# turn value stock y_***** �͎����̽ð���Ɗ֌W�Ȃ��̂Ŏ��R�Ɏ��񂵂Ă悢
sub write_user {
	&error("��ڲ԰�ް��̏������݂Ɏ��s���܂���") if !$id || !$m{name};

	$m{ltime} = $time;
	$m{ldate} = $date;

	# -------------------
	# top��۸޲�ؽĂɕ\��
	if ($time > $m{login_time} + $login_min * 60) {
		$m{login_time} = $time;

		open my $fh2, ">> $logdir/login.cgi";
		print $fh2 "$time<>$m{name}<>$m{country}<>$m{shogo}<>$m{mes}<>$m{icon}<>\n";
		close $fh2;
	}

	# -------------------
	# �ð���̍ő�l
	for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
		$m{$k} = 999 if $m{$k} > 999;
	}
	$m{money}  = 4999999 if $m{money} > 4999999;
	$m{coin}   = 2500000 if $m{coin}  > 2500000;

	# -------------------
	# �ϐ��ǉ�����ꍇ�͔��p��߰������s�����Ēǉ�(���s���A���בւ���(login_time�ȊO))
	my @keys = (qw/
		login_time ldate start_time mail_address name pass magic_word lib tp lib_r tp_r wt act sex shogo sedai vote vote_year
		country job seed lv exp rank rank_exp super_rank rank_name unit sol sol_lv medal money coin skills renzoku renzoku_c total_auction skills_sub skills_sub2 skills_sub3 money_limit
		max_hp hp max_mp mp at df mat mdf ag cha lea wea wea_c wea_lv wea_name gua egg egg_c pet pet_c shuffle master master_c boch_pet
		marriage lot is_full next_salary icon icon_pet icon_pet_lv icon_pet_exp mes mes_win mes_lose mes_touitsu ltime gacha_time gacha_time2 offertory_time trick_time breed_time silent_time
		rest_a rest_b rest_c

		turn stock value is_playing bank
		y_max_hp y_hp y_max_mp y_mp y_at y_df y_mat y_mdf y_ag y_cha y_lea y_wea y_wea_name y_skills
		y_name y_country y_rank y_sol y_unit y_sol_lv y_icon y_mes_win y_mes_lose y_pet y_value y_gua
		y_rest_a y_rest_b y_rest_c

		nou_c sho_c hei_c gai_c gou_c cho_c sen_c gik_c kou_c tei_c mat_c cas_c tou_c shu_c col_c mon_c
		win_c lose_c draw_c hero_c huk_c met_c war_c dom_c mil_c pro_c esc_c res_c fes_c war_c_t dom_c_t mil_c_t pro_c_t boch_c storm_c
		shogo_t icon_t breed breed_c depot_bonus akindo_guild silent_kind silent_tail guild_number disp_casino chat_java disp_top disp_news disp_chat disp_ad disp_daihyo salary_switch no_boss incubation_switch disp_gacha_time delete_shield
		valid_blacklist pet_icon_switch tutorial_switch
		c_turn c_stock c_value c_type cataso_ratio
		no1_c money_overflow random_migrate ceo_c tam_c ban_c wt_c wt_c_latest

		sox_kind sox_no exchange_count
	/);
	# ۸޲ݎ��ԁ@�X�V�����@�쐬�����@���O�@�߽ܰ�ށ@ײ���؁@���ݸ��߲�ā@�҂����ԁ@��J�x�@���ʁ@�̍��@����@���[�@
	# �������@�E�Ɓ@�푰�@���ف@�o���l�@�ݸ�@�ݸ�o���l�@����@���m���@�m�C�@�M�́@�����@��݁@�Z(����)�@�A���U�߂����@�A�����ā@
	# �ő�HP�@HP�@�ő�MP�@MP�@�́@���@���́@���h�@�f���@���́@�����@����@����ϋv�@�������ف@�h��@���ꕐ�햼�@�Ϻށ@�Ϻސ����@�߯ā@�V���b�t���t���O�@
	# ��������@��ށ@�a���菊���t�׸ށ@���̋��^�@���݁@ү���ށ@������́@������́@�����́@�X�V���ԁ@�������� ��������2 �ΑK���ԁ@��������������ԁ@�����֎~����
	# ��݁@�į��@��ح��@��ڲ���׸ށ@�����ް� �c
	# �_�Ɓ@���Ɓ@�����@�O���@���D�@����@���]�@�U�v�@��@�@�ҕ��@���Ɂ@�����@�C�s�@���Z��@�����@�E���@�~�o�@�Ձ@�����p�@�{�b�`
	# �푈�����@�푈�����@�푈�����@����@�����@�ŖS�@�푈�@�����@�R���@�O���@
	# �^�̍��@�^���݁@��ĉ��P�@��ĉ��Q�@�a�菊�{�[�i�X�@���l�M���h�@�ΐl���ɕ\���@��JAVA�\��
	# ���ɗp �c
	# �B���n���x
	# _c�̓J�E���g(count)�̗�, y_�͑���(you)�̗�

	my $line;
	for my $k (@keys) {
		$line .= $k =~ /^y_(.+)$/ ? "$k;$y{$1}<>" : "$k;$m{$k}<>";
	}

	open my $fh, "> $userdir/$id/user.cgi";
	print $fh "$line\n";
	print $fh "$addr<>$host<>$agent<>\n";
	close $fh;
}


#================================================
# ���̑�
#================================================
# �҂����Ԃ�b�ɕϊ� + ����
sub wait {
	$m{wt} = $GWT * 60;
	$m{wt_c} += $m{wt};
	&n_menu;

	$m{is_playing} = 0;
	--$w{playing};
	$w{playing} = 0 if $w{playing} < 0;
	&write_cs;
}

# �ʏ펞�̗��p����
sub is_satisfy { 1 }

# �l��ؾ��
sub refresh {
	$m{lib} = '';
	$m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
}

#================================================
# ��J��Ԃ̂Ƃ��̗��p����
#================================================
sub is_act_satisfy {
	if ($m{act} >= 100) {
		$mes .= '��J�����܂��Ă��܂��B��x�������s���Ă�������<br>';
		&refresh;
		&n_menu;
		return 1;
	}
	return 0;
}

#================================================
# ����މ��������B���҂��Ă���l�ƈႤ�ꍇ�� 1(true) ���Ԃ�&begin(�����ƭ��\��)
#================================================
sub is_ng_cmd {
	my @check_cmds = @_;

	for $check_cmd (@check_cmds) {
		return 0 if $cmd eq $check_cmd;
	}
	&begin;
	return 1;
}

#================================================
# Ҳ��ƭ��Ȃǂ̏��� main.cgi country.cgi myself.cgi shopping.cgi
#================================================
sub b_menu {
	my @menus = @_;

	if (!$m{is_playing} && $w{playing} >= $max_playing) {
		$mes .= qq|<font color="#FFFF00">��ڲ�K���� $w{playing}/$max_playing�l</font><br>���΂炭���҂���������|;
		&begin;
	}
	elsif (defined $menus[$cmd]) {
		$m{lib} = $menus[$cmd][1];
		$m{tp}   = 1;
		require "./lib/$m{lib}.cgi";

		# lib���s����ok�Ȃ�begin�ƭ�
		&begin if &is_satisfy;

		unless ($m{is_playing}) {
			$m{is_playing} = 1;
			++$w{playing};
			&write_cs;
		}
	}
	else {
		&begin;
	}
}
#================================================
# �ƭ������
#================================================
sub menu {
	my @menus = @_;
	my $rest = $m{wt} > 0 ? 1 : 0;
	if ($is_smart) {
		$menu_cmd .= qq|<table boder=0 cols=4 width=110 height=110>|;
		for my $i (0 .. $#menus) {
			if($i % 4 == 0){
				$menu_cmd .= qq|<tr>|;
			}
			next if $menus[$i] eq '';
			my $mline = '';
			my $mpos = 0;
			while (1) {
				my $char_num = 10;
				if ($mpos + $char_num >= length($menus[$i])) {
					$mline .= substr($menus[$i], $mpos);
					last;
				}
				my $last_char = substr($menus[$i], $mpos + $char_num - 1, 2);
				$last_char =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2', $1)/ge;
				my $first1 = substr($last_char, 0, 1);
				my $first2 = substr($last_char, 3, 1);
				if ($first1 eq '%' && $first2 ne '%') {
					$char_num--;
				}
				$mline .= substr($menus[$i], $mpos, $char_num) . "&#13;&#10;";
				$mpos += $char_num;
			}
			$menu_cmd .= qq|<td><form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button1s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#			$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # �S�����̃R�}���h���͂ł��邱�Ƃ�`���� ��񂾐�� $m{wt} �����肷�邱��
			$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # ���������Ȃ����߂̈ꎞ�L�[
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|</td>|;
			if($i % 4 == 3){
				$menu_cmd .= qq|</tr>|;
			}
		}
		if($#menus % 4 != 3){
			$menu_cmd .= qq|</tr>|;
		}
		$menu_cmd .= qq|</table>|;

	}
	elsif ($is_appli) {
		$menu_cmd .= qq|<div align="left" id="commands">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			$menu_cmd .= qq|<form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$menus[$i]" class="button2s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#			$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # �S�����̃R�}���h���͂ł��邱�Ƃ�`���� ��񂾐�� $m{wt} �����肷�邱��
			$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # ���������Ȃ����߂̈ꎞ�L�[
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|<br class="cmd_br" />| if ($i+1) % 7 == 0;
		}
		$menu_cmd .= qq|<br class="cmd_br" /></div>|;
	}
	else{
		$menu_cmd .= qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			$menu_cmd .= qq|<option value="$i">$menus[$i]</option>|;
		}
		$menu_cmd .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#		$menu_cmd .= qq|<input type="hidden" name="rest" value="$rest">| if $rest; # �S�����̃R�}���h���͂ł��邱�Ƃ�`���� ��񂾐�� $m{wt} �����肷�邱��
		$menu_cmd .= qq|<input type="hidden" name="magic_word" value="$magic_word">| if $magic_word; # ���������Ȃ����߂̈ꎞ�L�[
		$menu_cmd .= $is_mobile ? qq|<br><input type="submit" value="�� ��" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<br><input type="submit" value="�� ��" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
	}

#	return $menu_cmd if $rest; # �S������ $menu_cmd ���\������Ȃ����[�g��ʂ�̂ŁA�Ƃ肠�����S�����̃R�}���h�͂����ŕԂ镶����� $mes �ɑ����ĕ\������
=pod
	if($is_smart){
		$menu_cmd .= qq|<div>|;
#		$menu_cmd .= qq|<div style="float:right;">|;
		for my $i (0 .. $#menus) {
			next if $menus[$i] eq '';
			my $mline = '';
			my $mpos = 0;
			while (1) {
				my $char_num = 10;
				if ($mpos + $char_num >= length($menus[$i])) {
					$mline .= substr($menus[$i], $mpos);
					last;
				}
				my $last_char = substr($menus[$i], $mpos + $char_num - 1, 2);
				$last_char =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2', $1)/ge;
				my $first1 = substr($last_char, 0, 1);
				my $first2 = substr($last_char, 3, 1);
				if ($first1 eq '%' && $first2 ne '%') {
					$char_num--;
				}
				$mline .= substr($menus[$i], $mpos, $char_num) . "&#13;&#10;";
				$mpos += $char_num;
			}
			$menu_cmd .= qq|<form method="$method" action="$script" class="cmd_form">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button2s"><input type="hidden" name="cmd" value="$i">|;
#			$menu_cmd .= qq|<input type="submit" value="$menus[$i]" class="button2s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
#			print "$i ", ($i+1) % 4, " " , ($i+1) % 6, "<br>";

#			$menu_cmd .= qq|</div>| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
			$menu_cmd .= qq|<br class="smart_br" />| if ($i+1) % 4 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr" />| if ($i+1) % 4 == 0;
			$menu_cmd .= qq|<br class="tablet_br" />| if ($i+1) % 7 == 0;
#			$menu_cmd .= qq|<hr class="tablet_hr" />| if ($i+1) % 7 == 0;
#			$menu_cmd .= qq|<hr class="smart_hr">| if (($i+1) % 4 == 0) || (($i+1) % 7 == 0);
		}
		$menu_cmd .= qq|</div>|;
#		$menu_cmd .= qq|<br style="display:none;">|;
	}
=cut

}
#================================================
# Next�ƭ�
#================================================
sub n_menu {
	$menu_cmd  = qq|<form method="$method" action="$script">|;
	$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= $is_mobile ? qq|<input type="submit" value="Next" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="Next" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
}
#================================================
# �g�їpPager ���֑O�� shopping_hospital.cgi
#================================================
sub pager_next {
	my $page = shift;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="cmd" value="$cmd"><input type="hidden" name="page" value="$page">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�����߰��" class="button1"></form>|;
}
sub pager_back {
	my $page = shift;
	$page = 0 if $page < 0;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="cmd" value="$cmd"><input type="hidden" name="page" value="$page">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�O���߰��" class="button1"></form>|;
}

#================================================
# �n���x����
#================================================
sub c_up { # count up
	my $c = shift;
	++$m{$c};

	# �A����c_up�����p�Ƃ��ĸ�۰��قȑޔ�ϐ��Ɣ���ɕK�v�Ȕz��쐬
	if ($cash_c ne $c) {
		$cash_c = $c;
		@cash_shogos = ();
		for my $shogo (@shogos) {
			my($k) = keys %{ $shogo->[1] }; # �Ȃ���each����2��ڂ��Ƃ�Ȃ��c
			push @cash_shogos, [$shogo->[0], $shogo->[1]->{$k}, $shogo->[2]] if $c eq $k;
		}
	}

	for my $cash_shogo (@cash_shogos) {
		if ($cash_shogo->[1] eq $m{$c}) {
			&mes_and_world_news("$cash_shogo->[0]�̏̍���^�����܂���", 1);
			$m{money} += $cash_shogo->[2];
			$mes .= "$cash_shogo->[2]G�̕񏧋����󂯎��܂���<br>";
		}
	}
}

#================================================
# ��\���߲�ı���
#================================================
sub daihyo_c_up {
	my $c = shift;
	++$m{$c};

	my($k) = $c =~ /^(.+)_c$/;
	if ($cs{$k}[$m{country}] eq $m{name}) {
		$cs{$c}[$m{country}] = $m{$c};
	}
	elsif (!&is_daihyo && $m{$c} > $cs{$c}[$m{country}] && $m{$c} >= 10) {
		&mes_and_world_news(qq|<font color="#FF9999">�������̍��ւ̍v�����F�߂��$cs{name}[$m{country}]��\\��$e2j{$k}�ɔC������܂�����</font>|,1);
		$cs{$k}[$m{country}] = $m{name};
		$cs{$c}[$m{country}] = $m{$c};
	}
}



#================================================
# ���ɂ���v���C���[���擾
#================================================
sub get_country_members {
	my $country = shift;
	&error("��No[ $country ] ���̍������݂��Ȃ���") unless -d "$logdir/$country";

	my @lines = ();
	open my $fh, "< $logdir/$country/member.cgi" or &error("��$country�v���C���[�f�[�^���J���܂���");
	push @lines, $_ while <$fh>;
	close $fh;

	return @lines;
}


#================================================
# ����ڲ԰�ɱ��т�X��
#================================================
sub send_item {
	my($send_name, $kind, $item_no, $item_c, $item_lv) = @_;
	my $send_id = unpack 'H*', $send_name;
	$item_c  ||= 0;
	$item_lv ||= 0;

	if (-f "$userdir/$send_id/depot.cgi") {
		open my $fh, ">> $userdir/$send_id/depot.cgi";
		print $fh "$kind<>$item_no<>$item_c<>$item_lv<>\n";
		close $fh;

		open my $fh2, "> $userdir/$send_id/depot_flag.cgi";
		close $fh2;
	}
}

#================================================
# ����ڲ԰�ɂ����𑗋�
#================================================
sub send_money {
	my($send_name, $from_name, $money, $is_shop_sale) = @_;
	my $send_id = unpack 'H*', $send_name;
	$is_shop_sale||= 0;

	if (-f "$userdir/$send_id/money.cgi") {
		open my $fh, ">> $userdir/$send_id/money.cgi";
		print $fh "$from_name<>$money<>$is_shop_sale<>\n";
		close $fh;
	}
}


#================================================
# �\������ƭ���ɂ���������
#================================================
sub mes_and_world_news {
	my $message = shift;
	$mes .= "$message<br>";
	  $message =~ /^<b>/  ? &write_world_news("<b>$c_m��$m{name}��</b>$message", @_)
	: $message =~ /^<i>/  ? &write_world_news("<i>$c_m��$m{name}��</i>$message", @_)
	: $message =~ /^<em>/ ? &write_world_news("<em>$c_m��$m{name}��</em>$message", @_)
	:					    &write_world_news("$c_m��$m{name}��$message", @_)
	;
}
sub mes_and_send_news {
	my $message = shift;
	$mes .= "$message<br>";
	  $message =~ /^<b>/  ? &write_send_news("<b>$c_m��$m{name}��</b>$message", @_)
	: $message =~ /^<i>/  ? &write_send_news("<i>$c_m��$m{name}��</i>$message", @_)
	: $message =~ /^<em>/ ? &write_send_news("<em>$c_m��$m{name}��</em>$message", @_)
	:					    &write_send_news("$c_m��$m{name}��$message", @_)
	;
}

#================================================
# �ߋ��̉h���A������񃍃O�������ݏ���
#================================================
#sub write_world_news     { &_write_news('world_news', @_) }
sub write_world_news     {
	my($message, $is_memory, $memory_name) = @_;
	if ($w{world} ne '17' || $message =~ /^</) { # �h���E��y���فz�ȊO�h�܂��͑傫�ȏo����
		&_write_news('world_news', @_);
	}
	elsif ($is_memory) { # ���E��y���فz�Ő���t���O���������ꍇ
		$message = &coloration_country($message);
		&write_memory($message, $memory_name);
	}
}
sub write_send_news      { &_write_news('send_news',  @_) }
sub write_blog_news      { &_write_news('blog_news',  @_) }
sub write_colosseum_news { &_write_news('colosseum_news',  @_) }
sub write_picture_news   { &_write_news('picture_news',  @_) }
sub write_book_news      { &_write_news('book_news',  @_) }
sub _write_news {
	my($file_name, $message, $is_memory, $memory_name) = @_;

	&write_world_big_news($message) if $message =~ /^</;
	$message = &coloration_country($message);

	my @lines = ();
	open my $fh, "+< $logdir/$file_name.cgi" or &error("$file_name.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	&write_memory($message, $memory_name) if $is_memory;
}
#================================================
# ���E�̗���
#================================================
sub write_world_big_news {
	my $message = shift;

	$message = &coloration_country($message);
	my @lines = ();
	open my $fh, "+< $logdir/world_big_news.cgi" or &error("$logdir/world_big_news.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

# ------------------
# ����������ΐF�t��
sub coloration_country {
	my $message = shift;
	return $message if $w{country} < 1;
	for my $i (0 .. $w{country}) {
		my $add_color_country = qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font>|;
		$message =~ s/\Q$cs{name}[$i]\E/$add_color_country/g;
	}
	return $message;
}

#================================================
# �Δ�
#================================================
sub write_legend {
	my($file_name, $message, $is_memory, $memory_name) = @_;

	my @lines = ();
	open my $fh, "+< $logdir/legend/$file_name.cgi" or &error("$logdir/legend/$file_name.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	$message = &coloration_country($message);
	unshift @lines, qq|$world_name��$w{year}�N�y$world_states[$w{world}]�z�F$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	&write_memory($message, $memory_name) if $is_memory;
}

#================================================
# �v���o���O�������ݏ���
#================================================
# �����ɖ��O������ꍇ�́A���̐l�̐���ɁA�Ȃ��ꍇ�͎����̐���ɏ������܂��
sub write_memory {
	my($message, $memory_name) = @_;
	$m_id = $memory_name ? unpack 'H*', $memory_name : $id;

	return unless -f "$userdir/$m_id/memory.cgi";

	my @lines = ();
	open my $fh, "+< $userdir/$m_id/memory.cgi" or &error("Memory̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, qq|$message <font size="1">($date)</font>\n|;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


#================================================
# �����Ƒ���̋�������  2:���� 1:���� 0:�ア
#================================================
sub st_lv {
	my $y_st = shift || &y_st;
	my $m_st =          &m_st;

	return $y_st > $m_st * 1.5 ? 2
		:  $y_st < $m_st * 0.5 ? 0
		:                        1
		;
}
sub y_st { int($y{max_hp} + $y{max_mp} + $y{at} + $y{df} + $y{mat} + $y{mdf} + $y{ag} + $y{cha}*0.5) }
sub m_st { int($m{max_hp} + $m{max_mp} + $m{at} + $m{df} + $m{mat} + $m{mdf} + $m{ag} + $m{cha}*0.5) }

#================================================
# �ЊQ �ŖS����m���A���Ďg�p��
#================================================
sub disaster {
	my @disasters = (['���R�ЊQ','food'],['�o�ϔj�]','money'],['��n�k','soldier']);
	my $v = int(rand(@disasters));
	for my $i (1 .. $w{country}) {
		next if $cs{ is_die }[$i];
		$cs{ $disasters[$v][1] }[$i] = int($cs{ $disasters[$v][1] }[$i] * 0.5);
	}
	&write_world_news("<b>���E���� $disasters[$v][0] ���N����܂���</b>");
}


#================================================
# �����ް���Get �߂�l�̓n�b�V��
#================================================
# �g����: &get_you_datas('����̖��O');
sub get_you_datas {
	my($name, $is_unpack) = @_;

	my $y_id = $is_unpack ? $name : unpack 'H*', $name;

	open my $fh, "< $userdir/$y_id/user.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
	my $line_data = <$fh>;
	my $line_info = <$fh>;
	close $fh;

	my($paddr, $phost, $pagent) = split /<>/, $line_info;

	my %you_datas = (
		addr	=> $paddr,
		host	=> $phost,
		agent	=> $pagent,
	);
	for my $hash (split /<>/, $line_data) {
		my($k, $v) = split /;/, $hash;
		next if $k =~ /^y_/;

		$you_datas{$k} = $v;
	}

	return %you_datas;
}

#================================================
# �����ް��ύX  �������Ɠ��Z��̏n���xUP���Ɏg�p
#================================================
# �g����: &regist_you_data('����̖��O', '�ύX�������ϐ�', '�l');
sub regist_you_data {
	my($name, $k, $v) = @_;
	return if $name eq '' || $k eq '';

	my $y_id = unpack 'H*', $name;
	return unless -f "$userdir/$y_id/user.cgi";

	open my $fh, "+< $userdir/$y_id/user.cgi" or &error("$userdir/$y_id/user.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my $line_info = <$fh>;
	$line =~ s/<>($k;).*?<>/<>$1$v<>/;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	print $fh $line_info;
	close $fh;
}


#================================================
# �S���ɒǉ�
#================================================
sub add_prisoner {
	$mes .= "$m{name}�́A�G�����Ɏ��͂܂�߂܂��Ă��܂���!<br>";
	$mes .= "�S���֘A�s����܂��B���ɍs���ł���̂�$GWT����ł�<br>";

	$m{lib} = 'prison';
	$m{renzoku_c} = $m{act} = 0;
	$m{tp} = 100;
	&wait;

	# �S��ؽĂɒǉ�
	open my $fh, ">> $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ���J���܂���");
	print $fh "$m{name}<>$m{country}<>\n";
	close $fh;

	require './lib/_bbs_chat.cgi';
	$this_file = "$logdir/$y{country}/bbs";
	$in{comment} = "$m{mes_lose}�y�N��z$m{name}���S���ɘA�s����܂���";
	$bad_time = 0;
	&write_comment;
}

#================================================
# ���͂���ԍ�����
#================================================
sub get_most_strong_country {
	my $country = 0;
	my $max_value = 0;
	for my $i (1 .. $w{country}) {
		next if $i eq $m{country};
		next if $i eq $union;
		if ($cs{strong}[$i] > $max_value) {
			$country = $i;
			$max_value = $cs{strong}[$i];
		}
	}
	return $country;
}

#================================================
# �A�C�e�����擾
# ��P�����Ƒ�Q���������Ŗ��O
# ��R�����܂ł��߯Ă��������ǉ� �ެݸ���߯Ă��������g���̂�
# ��S�����܂Ŏw�肷��ƑS�A�C�e�����ǉ�
# ��T�����̓A�C�e���̎�ނ��\�� �V���b�v�Ȃǈꕔ�ł͎�ނ���\���Ȃ̂�
# $kind �A�C�e���̎��(1���� 2�� 3�߯� 4�h��)
# $item_no �A�C�e���̔ԍ�
# $item_c �A�C�e���������l(�ϋv�l �z���l �� �Ȃ�)
# $item_lv �A�C�e���̃��x��(�� �Ȃ� �Ȃ� �Ȃ�)
# $flag 1 �Ŏ�ޕ\���I�t
# �V�����A�C�e�����ǉ������炱����ύX���邱��
#================================================
sub get_item_name {
	my($kind, $item_no, $item_c, $item_lv, $flag) = @_;

	my $result;
	if (defined($item_lv)) { # �S�����L���Ȃ�A�C�e�����
		$result = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
				  : $kind eq '2' ? "[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
				  : $kind eq '3' ? "[��]$pets[$item_no][1]��$item_c"
				  :                "[$guas[$item_no][2]]$guas[$item_no][1]"
			  ;
		$result = substr($result, 4) if $flag; # $flag ���L���Ȃ�A�C�e������\��
	}
	else { # �S�����L������Ȃ��Ȃ�A�C�e����
		$result = $kind eq '1' ? "$weas[$item_no][1]"
				  : $kind eq '2' ? "$eggs[$item_no][1]"
				  : $kind eq '3' ? (defined($item_c) ? "$pets[$item_no][1]��$item_c" : "$pets[$item_no][1]") # ��R�����L�������߯ĂȂ烌�x���t��
				  :                "$guas[$item_no][1]"
				  ;
	}
	return $result;
}

sub remove_pet { # �߯ĊO������
	$m{pet} = 0;
	$m{icon_pet} = '';
	$m{icon_pet_lv} = 0;
	$m{icon_pet_exp} = 0;
}

1; # �폜�s��