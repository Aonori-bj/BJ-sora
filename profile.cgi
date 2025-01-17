#!/usr/bin/perl
require 'config.cgi';
require 'config_game.cgi';
require "$datadir/skill.cgi";
require "$datadir/profile.cgi";
#================================================
# ｽﾃｰﾀｽ & ﾌﾟﾛﾌｨｰﾙ表示 Created by Merino
#================================================

&decode;
&header;
&header_profile;
&read_cs;

if    ($in{mode} eq 'profile') { &profile; }
elsif ($is_mobile) { &status_mobile if $in{mode} eq 'status'; }
else { &status_pc; }

&footer;
exit;

#================================================
# 携帯ｽﾃｰﾀｽ画面
#================================================
sub status_mobile {
	%m = &get_you_datas($in{id}, 1);

	my %collection_pars = &collection_pars;
	my $skill_par = &skill_par;
	my $shogo_par = &shogo_par;
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;
	
	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= "[$skills[$m_skill][2]]$skills[$m_skill][1]<br>";
	}

	print qq|<br>更新日時 $m{ldate}<hr>|;
	print qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon};
	print qq|$m{name}<br>|;
	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		print qq|結婚相手 <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	print qq|<font color="$cs{color}[$m{country}]">$cs{name}[$m{country}]</font> $ranks[$m{rank}]<br>|;
	print qq|$units[$m{unit}][1]<br>|;
	print qq|称号 $m{shogo}<br>| if $m{shogo};
	print qq|Lv.<b>$m{lv}</b>|;
	print qq|資金 <b>$m{money}</b> G<br>|;
	print qq|<font color="#9999CC">武器:[$weas[$m{wea}][2]]$weas[$m{wea}][1]★<b>$m{wea_lv}</b></font><br>| if $m{wea};
	print qq|<font color="#99CCCC">ﾍﾟｯﾄ:$pets[$m{pet}][1]</font><br>| if $m{pet};
	print qq|<font color="#99CC99">ﾀﾏｺﾞ:$eggs[$m{egg}][1]</font><br>| if $m{egg};

	my $m_st = &m_st;
	print <<"EOM";
		<b>$m{sedai}</b>世代目<br>
		$sexes[ $m{sex} ] [$jobs[$m{job}][1]]<br>
		勲章 <b>$m{medal}</b>個<br>
		ｶｼﾞﾉｺｲﾝ <b>$m{coin}</b>枚<br>
		<hr>
		【ｽﾃｰﾀｽ】強さ:$m_st<br>
		$e2j{max_hp} [<b>$m{max_hp}</b>]/ＭＰ [<b>$m{max_mp}</b>]/<br>
		$e2j{at} [<b>$m{at}</b>]/$e2j{df} [<b>$m{df}</b>]/<br>
		$e2j{mat} [<b>$m{mat}</b>]/$e2j{mdf} [<b>$m{mdf}</b>]/<br>
		$e2j{ag} [<b>$m{ag}</b>]/$e2j{cha} [<b>$m{cha}</b>]/<br>
		$e2j{lea} [<b>$m{lea}</b>]<br>
		<hr>
		【覚えている技】<br>
		 $skill_info
		<hr>
		【熟練度】<br>
		農業 <b>$m{nou_c}</b>/商業 <b>$m{sho_c}</b>/徴兵 <b>$m{hei_c}</b>/外交 <b>$m{gai_c}</b>/待伏 <b>$m{mat_c}</b>/<br>
		強奪 <b>$m{gou_c}</b>/諜報 <b>$m{cho_c}</b>/洗脳 <b>$m{sen_c}</b>/偽計 <b>$m{gik_c}</b>/偵察 <b>$m{tei_c}</b>/<br>
		修行 <b>$m{shu_c}</b>/討伐 <b>$m{tou_c}</b>/闘技 <b>$m{col_c}</b>/ｶｼﾞﾉ <b>$m{cas_c}</b>/魔物 <b>$m{mon_c}</b>/<br>
		統一 <b>$m{hero_c}</b>/復興 <b>$m{huk_c}</b>/滅亡 <b>$m{met_c}</b>/<br>
		<hr>
		【代表\者ﾎﾟｲﾝﾄ】<br>
		戦争 <b>$m{war_c}</b>/内政 <b>$m{dom_c}</b>/軍事 <b>$m{mil_c}</b>/外交 <b>$m{pro_c}</b>/
		<hr>
		【戦歴】<br>
		<b>$war_c</b>戦 <b>$m{win_c}</b>勝 <b>$m{lose_c}</b>負 <b>$m{draw_c}</b>引<br>
		勝率 <b>$win_par</b>%
		<hr>
		【ｺﾝﾌﾟﾘｰﾄ率】<br>
		称号<b>$shogo_par</b>%<br>
		ｽｷﾙ<b>$skill_par</b>%<br>
		武器<b>$collection_pars{1}</b>%<br>
		ﾀﾏｺﾞ<b>$collection_pars{2}</b>%<br>
		ﾍﾟｯﾄ<b>$collection_pars{3}</b>%<br>
EOM
}

#================================================
# PCｽﾃｰﾀｽ画面
#================================================
sub status_pc {
	%m = &get_you_datas($in{id}, 1);

	my %collection_pars = &collection_pars;
	my $skill_par = &skill_par;
	my $shogo_par = &shogo_par;
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;
	
	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= qq|<tr><td align="center">$skills[$m_skill][2]</td><td>$skills[$m_skill][1]</td></tr>|;
	}
	
	$m{name} .= "[$m{shogo}]" if $m{shogo};
	print qq|<table width="440" border="0" cellpadding="3" bgcolor="#CCCCCC"><tr><td bgcolor="#000000" align="left" valign="top">|;
	print qq|<table width="100%" border="0"><tr><td width="60%" valign="top" align="left"><tt>|;
	print qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;">| if $m{icon};
	print qq|$m{name}<br>|;
	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		print qq|結婚相手 <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}

	my $m_st = &m_st;
	print <<"EOM";
		<font color="$cs{color}[$m{country}]">$cs{name}[$m{country}]</font> $ranks[$m{rank}]<br>
		$units[$m{unit}][1]
		<hr size="1" width="90%">
			<font color="#9999CC">武器：[$weas[$m{wea}][2]]$weas[$m{wea}][1]★<b>$m{wea_lv}</b></font><br>
			<font color="#99CCCC">ﾍﾟｯﾄ：$pets[$m{pet}][1]</font><br>
			<font color="#99CC99">ﾀﾏｺﾞ：$eggs[$m{egg}][1]</font>
		</tt></td><td valign="top" align="left"><tt>
			<b>$m{sedai}</b>世代目 $sexes[ $m{sex} ]<br>
			Lv.<b>$m{lv}</b> [$jobs[$m{job}][1]]<br>
			<hr size="1">
			資金 <b>$m{money}</b>G<br>
			<hr size="1">
			勲　章　<b>$m{medal}</b>個<br>
			ｶｼﾞﾉｺｲﾝ <b>$m{coin}</b>枚<br>
			<p>更新日時 $m{ldate}</p>
		</tt></td></tr></table>
		<tt>

		【ｽﾃｰﾀｽ】強さ：$m_st<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>$e2j{max_hp}</th><td align="right">$m{max_hp}</td>
			<th>$e2j{at}</th><td align="right">$m{at}</td>
			<th>$e2j{df}</th><td align="right">$m{df}</td>
		</tr><tr>
			<th>ＭＰ</th><td align="right">$m{max_mp}</td>
			<th>$e2j{mat}</th><td align="right">$m{mat}</td>
			<th>$e2j{mdf}</th><td align="right">$m{mdf}</td>
		</tr><tr>
			<th>$e2j{lea}</th><td align="right">$m{lea}</td>
			<th>$e2j{ag}</th><td align="right">$m{ag}</td>
			<th>$e2j{cha}</th><td align="right">$m{cha}</td>
		</tr>
		</table>
		<hr size="1">
		【覚えている技】<br>
		<table class="table1" cellpadding="3">
		<tr><th>属性</th><th>技　名</th></tr>
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
			<th>魔物</th><td align="right">$m{mon_c}</td>
		</tr>
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
		
		<hr size="1">
		【ｺﾝﾌﾟﾘｰﾄ率】<br>
		<table class="table1" cellpadding="3">
			<tr><th>称号</th><td align="right"><b>$shogo_par</b>%<br></td></tr>
			<tr><th>ｽｷﾙ</th><td align="right"><b>$skill_par</b>%<br></td></tr>
			<tr><th>武器</th><td align="right"><b>$collection_pars{1}</b>%<br></td></tr>
			<tr><th>ﾀﾏｺﾞ</th><td align="right"><b>$collection_pars{2}</b>%<br></td></tr>
			<tr><th>ﾍﾟｯﾄ</th><td align="right"><b>$collection_pars{3}</b>%<br></td></tr>
		</table>
	</tt></td></tr></table>
EOM
}

#================================================
# ﾌﾟﾛﾌｨｰﾙ
#================================================
sub profile {
	open my $fh, "< $userdir/$in{id}/profile.cgi" or &error("$userdir/$in{id}/profile.cgi ﾌｧｲﾙが読み込めません");
	my $line = <$fh>;
	close $fh;
	my %datas = ();
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$datas{$k} = $v;
	}
	
	print qq|<table class="table1" cellpadding="3" width="440">| unless $is_mobile;
	for my $profile (@profiles) {
		next if $datas{$profile->[0]} eq '';
		
		# ｵｰﾄﾘﾝｸ(BBSやCHATと違い編集可能なので、編集するときにﾘﾝｸﾀｸﾞが出てしまうので読み込みでｵｰﾄﾘﾝｸ処理)
		$datas{$profile->[0]} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
		$is_mobile ? $datas{$profile->[0]} =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $datas{$profile->[0]} =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		
		print $is_mobile ? qq|<hr><h2>$profile->[1]</h2><br>$datas{$profile->[0]}<br>|
			: qq|<tr><th align="left">$profile->[1]</th></tr><tr><td>$datas{$profile->[0]}</td></tr>|;
	}
	print qq|</table>| unless $is_mobile;
}


#================================================
# 各ｺﾝﾌﾟﾘｰﾄ率
#================================================
sub skill_par { # 技
	open my $fh, "< $userdir/$in{id}/skill.cgi" or &error("$userdir/$in{id}/skill.cgiﾌｧｲﾙが読み込めません");
	my $line = <$fh>;
	close $fh;
	$line =~ tr/\x0D\x0A//d;
	
	my @nos = split /,/, $line;
	pop @nos; # 先頭の空を除く
	
	my $comp_par = @nos <= 0 ? 0 : int(@nos / $#skills * 100);
	$comp_par = 100 if $comp_par > 100;
	return $comp_par;
}
sub shogo_par { # 称号
	my $count = 0;
	for my $i (1 .. $#shogos) {
		my($k, $v) = each %{ $shogos[$i][1] };
		++$count if $m{$k} >= $v;
	}
	my $comp_par = $count <= 0 ? 0 : int($count / ($#shogos-2) * 100);
	$comp_par = 100 if $comp_par > 100;
	return $comp_par;
}

sub collection_pars { # ｱｲﾃﾑ
	my %pars = ();
	my $kind = 1;
	open my $fh, "< $userdir/$in{id}/collection.cgi" or &error("$userdir/$in{id}/collection.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my @nos = split /,/, $line;
		pop @nos; # 先頭の空を除く
		
		if (@nos <= 0) {
			$pars{$kind} = 0;
		}
		elsif ($kind eq '1') {
			$pars{$kind} = int(@nos / $#weas * 100);
		}
		elsif ($kind eq '2') {
			$pars{$kind} = int(@nos / $#eggs * 100);
		}
		elsif ($kind eq '3') {
			$pars{$kind} = int(@nos / $#pets * 100);
		}
		$pars{$kind} = 100 if $pars{$kind} > 100;
		++$kind;
	}
	close $fh;
	
	return %pars;
}


