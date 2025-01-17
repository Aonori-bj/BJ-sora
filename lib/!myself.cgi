require "$datadir/skill.cgi";
require "$datadir/pet.cgi";
#=================================================
# ｽﾃｰﾀｽ画面 Created by Merino
#=================================================

# ﾒﾆｭｰ ◎追加/変更/削除/並べ替え可能
my @menus = (
	['やめる',		'main'],
	['ｺﾚｸｼｮﾝﾙｰﾑ',	'myself_collection'],
	['ｽｷﾙ継承',		'myself_skill'],
	['称号を変更',	'myself_shogo'],
	['ｾﾘﾌを変更',	'myself_mes'],
	['自己紹介',	'myself_profile'],
	['商人のお店',	'myself_shop'],
	['ﾏｲﾋﾟｸﾁｬ',		'myself_picture'],
	['ﾏｲﾌﾞｯｸ',		'myself_book'],
	['商人の銀行',	'myself_bank'],
	['個人設定',	'myself_config'],
);


#================================================
sub begin {
	$layout = 2;
	$is_mobile ? &my_status_mobile : &my_status_pc;
	&menu(map{ $_->[0] }@menus);
}
sub tp_1 {
	# ﾍﾟｯﾄ使用
	if ($in{mode} eq 'use_pet' && $m{pet} && $pets[$m{pet}][2] eq 'myself') {
		&refresh;
		&n_menu;

		# ﾏﾓﾉﾉﾀﾈの場合
		if ($m{pet} >= 128 && $m{pet} <= 130) {
			$mes .= "$pets[$m{pet}][1]は、$m{name}のことをじっと見ている…<br>";
			$m{lib} = 'add_monster';
			$m{tp}  = 100;
		}
		else {
			&{ $pets[$m{pet}][3] };
			$mes .= "役目を終えた $pets[$m{pet}][1] は光の彼方へ消えていった…<br>";
			$m{pet} = 0;
		}
	}
	else {
		&b_menu(@menus);
	}
}


#================================================
# 携帯用ｽﾃｰﾀｽ表示
#================================================
sub my_status_mobile {
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;

	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= "[$skills[$m_skill][2]]$skills[$m_skill][1] 消費$e2j{mp} $skills[$m_skill][3]<br>";
	}

	my $sub_at  = '';
	my $sub_mat = '';
	my $sub_ag  = '';
	if ($m{wea}) {
		$mes .= qq|<hr>【武器情報】<br><ul>|;
		$mes .= qq|<li>名前:$weas[$m{wea}][1]|;
		$mes .= qq|<li>属性:$weas[$m{wea}][2]|;
		$mes .= qq|<li>強さ:$weas[$m{wea}][3]|;
		$mes .= qq|<li>耐久:$weas[$m{wea}][4]|;
		$mes .= qq|<li>重さ:$weas[$m{wea}][5]</ul><hr>|;
		if    ($weas[$m{wea}][2] =~ /無|剣|斧|槍/) { $sub_at  = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /風|炎|雷/)    { $sub_mat = "+$weas[$m{wea}][3]"; $sub_ag = "-$weas[$m{wea}][5]"; }
	}

	if ($m{pet}) {
		$mes .= qq|【ﾍﾟｯﾄ情報】<br><ul>|;
		$mes .= qq|<li>名前:$pets[$m{pet}][1]|;
		$mes .= qq|<li>効果:$pet_effects[$m{pet}]</ul>|;
		if ($pets[$m{pet}][2] eq 'myself') {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="ﾍﾟｯﾄを使用する" class="button1"></form>|;
		}
		$mes .= qq|<hr>|;
	}

	my $m_st = &m_st;
	$mes .=<<"EOM";
		<b>$m{sedai}</b>世代目<br>
		$sexes[ $m{sex} ] [$jobs[$m{job}][1]]<br>
		勲章 <b>$m{medal}</b>個<br>
		ｶｼﾞﾉｺｲﾝ <b>$m{coin}</b>枚<br>
		宝ｸｼﾞ【$m{lot}】<br>
		<hr>
		【ｽﾃｰﾀｽ】強さ:$m_st<br>
		$e2j{max_hp} [<b>$m{max_hp}</b>]/$e2j{max_mp} [<b>$m{max_mp}</b>]/<br>
		$e2j{at} [<b>$m{at}</b>$sub_at]/$e2j{df} [<b>$m{df}</b>]/<br>
		$e2j{mat} [<b>$m{mat}</b>$sub_mat]/$e2j{mdf} [<b>$m{mdf}</b>]/<br>
		$e2j{ag} [<b>$m{ag}</b>$sub_ag]/$e2j{cha} [<b>$m{cha}</b>]/<br>
		$e2j{lea} [<b>$m{lea}</b>]<br>
		<hr>
		【覚えている技】<br>
		 $skill_info
		<hr>
		【熟練度】<br>
		農業 <b>$m{nou_c}</b>/商業 <b>$m{sho_c}</b>/徴兵 <b>$m{hei_c}</b>/外交 <b>$m{gai_c}</b>/待伏 <b>$m{mat_c}</b>/<br>
		強奪 <b>$m{gou_c}</b>/諜報 <b>$m{cho_c}</b>/洗脳 <b>$m{sen_c}</b>/偽計 <b>$m{gik_c}</b>/偵察 <b>$m{tei_c}</b>/<br>
		修行 <b>$m{shu_c}</b>/討伐 <b>$m{tou_c}</b>/闘技 <b>$m{col_c}</b>/ｶｼﾞﾉ <b>$m{cas_c}</b>/<br>
		統一 <b>$m{hero_c}</b>/復興 <b>$m{huk_c}</b>/滅亡 <b>$m{met_c}</b>/<br>
		<hr>
		【代表\者ﾎﾟｲﾝﾄ】<br>
		戦争 <b>$m{war_c}</b>/内政 <b>$m{dom_c}</b>/軍事 <b>$m{mil_c}</b>/外交 <b>$m{pro_c}</b>/
		<hr>
		【戦歴】<br>
		<b>$war_c</b>戦 <b>$m{win_c}</b>勝 <b>$m{lose_c}</b>負 <b>$m{draw_c}</b>引<br>
		勝率 <b>$win_par</b>%
EOM
}

#================================================
# PC用ｽﾃｰﾀｽ表示
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
		$mes .= qq|<hr>【武器情報】<br>|;
		$mes .= qq|<table class="table1" cellpadding="3"><tr>|;
		$mes .= qq|<th>名前</th><td>$weas[$m{wea}][1]</td>|;
		$mes .= qq|<th>属性</th><td>$weas[$m{wea}][2]</td>|;
		$mes .= qq|<th>強さ</th><td>$weas[$m{wea}][3]</td>|;
		$mes .= qq|<th>耐久</th><td>$weas[$m{wea}][4]</td>|;
		$mes .= qq|<th>重さ</th><td>$weas[$m{wea}][5]</td>|;
		$mes .= qq|</tr></table><hr size="1">|;
		if    ($weas[$m{wea}][2] =~ /無|剣|斧|槍/) { $sub_at  = "▲$weas[$m{wea}][3]"; $sub_ag = "▼$weas[$m{wea}][5]"; }
		elsif ($weas[$m{wea}][2] =~ /風|炎|雷/)    { $sub_mat = "▲$weas[$m{wea}][3]"; $sub_ag = "▼$weas[$m{wea}][5]"; }
	}

	if ($m{pet}) {
		$mes .= qq|【ﾍﾟｯﾄ情報】<br>|;
		$mes .= qq|<table class="table1" cellpadding="3">|;
		$mes .= qq|<tr><th>名前</th><td>$pets[$m{pet}][1]</td>|;
		$mes .= qq|<th>効果</th><td>$pet_effects[$m{pet}]</td></tr>|;
		$mes .= qq|</table>|;
		if ($pets[$m{pet}][2] eq 'myself') {
			$mes .= qq|<br><form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="mode" value="use_pet">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="submit" value="ﾍﾟｯﾄを使用する" class="button1"></form>|;
		}
		$mes .= qq|<hr size="1">|;
	}

	my $m_st = &m_st;
	$mes .= <<"EOM";
		【ｽﾃｰﾀｽ】強さ：$m_st<br>
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
		【覚えている技】<br>
		<table class="table1" cellpadding="3">
		<tr><th>属性</th><th>技名</th><th>消費$e2j{mp}</th></tr>
		$skill_info
		</table>

		<hr size="1">
		【熟練度】<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>農業</th><td align="right">$m{nou_c}</td>
			<th>商業</th><td align="right">$m{sho_c}</td>
			<th>徴兵</th><td align="right">$m{hei_c}</td>
			<th>外交</th><td align="right">$m{gai_c}</td>
			<th>待伏</th><td align="right">$m{mat_c}</td>
		</tr>
		<tr>
			<th>強奪</th><td align="right">$m{gou_c}</td>
			<th>諜報</th><td align="right">$m{cho_c}</td>
			<th>洗脳</th><td align="right">$m{sen_c}</td>
			<th>偽計</th><td align="right">$m{gik_c}</td>
			<th>偵察</th><td align="right">$m{tei_c}</td>
		</tr>
		<tr>
			<th>修行</th><td align="right">$m{shu_c}</td>
			<th>討伐</th><td align="right">$m{tou_c}</td>
			<th>闘技</th><td align="right">$m{col_c}</td>
			<th>ｶｼﾞﾉ</th><td align="right">$m{cas_c}</td>
			<th>魔物</th><td align="right">$m{mon_c}</td></tr>
		<tr>
			<th>統一</th><td align="right">$m{hero_c}</td>
			<th>復興</th><td align="right">$m{huk_c}</td>
			<th>滅亡</th><td align="right">$m{met_c}</td>
			<th>　</th><td align="right">　</td>
			<th>　</th><td align="right">　</td>
		</tr>
		</table>

		<hr size="1">
		【代表\者ﾎﾟｲﾝﾄ】<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>戦争</th><td align="right">$m{war_c}</td>
			<th>内政</th><td align="right">$m{dom_c}</td>
			<th>軍事</th><td align="right">$m{mil_c}</td>
			<th>外交</th><td align="right">$m{pro_c}</td>
		</tr>
		</table>

		<hr size="1">
		【戦歴】<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>戦回</th><td align="right">$war_c</td>
			<th>勝ち</th><td align="right">$m{win_c}</td>
			<th>負け</th><td align="right">$m{lose_c}</td>
			<th>引分</th><td align="right">$m{draw_c}</td>
			<th>勝率</th><td align="right">$win_par %</td>
		</tr>
		</table>
EOM
}


1; # 削除不可
