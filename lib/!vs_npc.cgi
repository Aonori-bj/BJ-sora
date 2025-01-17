#=================================================
# [暗黒]NPC戦用ﾌﾟﾛｸﾞﾗﾑ Created by Merino
#=================================================

# 何度も同じ人がNPC国に仕官しないように仕官ログ(人)
$max_npc_old_member = $w{player} * 0.2;

# NPC名(先頭5名は戦争したときに出現する)
my @npc_names = (qw/ﾃﾞｨｱﾎﾞﾛｽ(NPC) ﾗｳﾞｫｽ(NPC) ﾒｷﾞﾄﾞﾗ(NPC) ﾀﾞｰｸ(NPC) ﾐﾆﾎﾞﾛｽ(NPC) ﾛﾌﾟﾄ(NPC) ﾃﾞｽ(NPC) ｸﾗｲ(NPC) ﾗｽﾄ(NPC) ﾌﾟﾗｲﾄﾞ(NPC) ｼﾞｬｯｶﾙ(NPC) ｷｮｳ(NPC) ﾊﾞﾙｽ(NPC) ﾑｽｶ(NPC) ﾀﾞｰｽﾍﾞｰﾀﾞ(NPC) ｼﾞｬｽﾃｨｽ(NPC) ﾐﾆﾓﾝ(NPC) ｳﾞｧﾘｱｽ(NPC) ﾍﾙｽﾞｱｲ(NPC)  ﾍｳﾞﾝｽﾞﾍﾙ(NPC) ﾉﾛｲ(NPC) ﾃﾞﾋﾞﾙｽﾞ(NPC) ﾔﾐ(NPC) ﾄﾛﾙ(NPC) ｳﾗﾐ(NPC) ｷｰﾙ(NPC)/);
#                   0             1          2           3         4


#=================================================
# NPC国の追加
#=================================================
sub add_npc_country {
	&write_world_news("<i>歴代の覇者達によって封印されていた魔界の結界が弱まり、悪夢が再び甦ろうとしている…</i>");
	$w{game_lv} = 99;
	$w{world} = $#world_states;
	
	# NPCの国の名前
	my @c_names = (qw/ﾃﾞｨｱﾎﾞﾛｽ帝国 ﾃﾞｽﾄﾗﾝｽ帝国 ｿﾞｰｱ帝国 邪神帝国 魔王の城 禁断の魔界 羅刹国 闇の魔結社/);
	my $npc_country_name  = $c_names[int(rand(@c_names))];
	
	# NPCの国色
	my $npc_country_color = '#FF00FF';

	++$w{country};
	my $i = $w{country};

	mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
	for my $file_name (qw/bbs bbs_log bbs_member patrol prison prison_member prisoner violator old_member/) {
		my $output_file = "$logdir/$i/$file_name.cgi";
		next if -f $output_file;
		open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
		close $fh;
		chmod $chmod, $output_file;
	}
	for my $file_name (qw/leader member/) {
		my $output_file = "$logdir/$i/$file_name.cgi";
		open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
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
		open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
		close $fh;
		chmod $chmod, "$file_name.cgi";
		
		open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
		close $fh2;
		chmod $chmod, "${file_name}_log.cgi";
		
		open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
		close $fh3;
		chmod $chmod, "${file_name}_member.cgi";
	}
	
	unless (-f "$htmldir/$i.html") {
		open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ﾌｧｲﾙが作れません");
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
	$cs{capacity}[$i] = 6; # 完全なNPC国にしたい場合は ←の数字を 0 にする
	$cs{is_die}[$i]   = 0;
	
	my @lines = &get_countries_mes();
	if ($w{country} > $#lines) {
		open my $fh9, ">> $logdir/countries_mes.cgi";
		print $fh9 "愚カナル人間共ヨ、偉大ナル我ガ闇ノチカラノ前ニ平伏スガ良イ…<>diabolos.gif<>\n";
		close $fh9;
	}
}
#=================================================
# 戦争NPCｷｬﾗを作成
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
	#	[0]属性[1]武器No	[2]必殺技
		['無', [0],			[61..65],],
		['剣', [1 .. 5],	[1 .. 5],],
		['槍', [6 ..10],	[11..15],],
		['斧', [11..15],	[21..25],],
		['炎', [16..20],	[31..35],],
		['風', [21..25],	[41..45],],
		['雷', [26..30],	[51..55],],
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
# NPC国の削除
#=================================================
sub delete_npc_country {
	if ($is_npc_win) {
		if ($m{country} eq $w{country}) {
			$w{win_countries} = $union ? $union : '';
			$m{country} = 0;
			$cs{war}[0] = $m{name};
			$m{shogo}   = '★堕天使†';
		}
		else {
			$w{win_countries} = $m{country};
		}
		
		# 国代表者に特典
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
		$is_npc_win ? &regist_you_data($name, 'shogo', '★堕天使†') : &regist_you_data($name, 'shogo', $shogos[1][0]);
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
# NPC国の軍事 ./lib/military.cgiで頻度調整
#=================================================
sub npc_military {
	my @keys = (qw/gou gou gou cho cho cho sen ds/);
	my $k = $keys[int(rand(@keys))];
	my $country = int(rand($w{country}-1)+1);
	return if $cs{is_die}[$country]; # 滅亡国からは奪わない
	&{'npc_military_'.$k}($country);
}
sub npc_military_gou { # 強奪
	my $country = shift;
	my $v = &_npc_get_resource($country, 'food');
	&write_world_news("$cs{name}[$w{country}]の$npc_names[int(rand(@npc_names))]が$cs{name}[$country]に奇襲攻撃を実施。$vの兵糧を強奪することに成功しました");
}
sub npc_military_cho { # 諜報
	my $country = shift;
	my $v = &_npc_get_resource($country, 'money');
	&write_world_news("$cs{name}[$w{country}]の$npc_names[int(rand(@npc_names))]が$cs{name}[$country]の資金調達ﾙｰﾄを撹乱し、$vの$e2j{money}を流出させることに成功しました");
}
sub npc_military_sen { # 軍事
	my $country = shift;
	my $v = &_npc_get_resource($country, 'soldier');
	&write_world_news("$cs{name}[$w{country}]の$npc_names[int(rand(@npc_names))]が$cs{name}[$country]の$vの兵を洗脳することに成功!$cs{name}[$w{country}]の兵に取り込みました");
}
sub npc_military_ds { # Dead Soldier 死霊の召喚
	return if $cs{soldier}[$w{country}] > 500000;
	$cs{$k}[$w{country}] += 50000;
	&write_world_news("$cs{name}[$w{country}]の$npc_names[int(rand(@npc_names))]が死の国より死霊の兵士を呼び覚まし、$cs{name}[$w{country}]の総兵士数が50000増加しました");
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
# NPC国の戦争 ./lib/_war_result.cgiで頻度調整
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
sub npc_use_pet_fenrir { # ﾌｪﾝﾘﾙ
	return if $touitu_strong < 20000;
	$w{game_lv} += 1 if $w{game_lv} < 90;
	for my $i (1..$w{country}-1) {
		next if $cs{is_die}[$i];
		next if $cs{strong}[$i] < 1000;
		$cs{strong}[$i] -= $touitu_strong * 0.6 > $cs{strong}[$w{country}] ? int(rand(400)+400) : int(rand(200)+200);
	}
	
	$touitu_strong * 0.6 > $cs{strong}[$w{country}] ? 
		&write_world_news("$cs{name}[$w{country}]の$npc_names[0]の魔神の閃光!各国の$e2j{strong}が削られました"):
		&write_world_news("$cs{name}[$w{country}]の$npc_names[4]の破壊光線!各国の$e2j{strong}が削られました");
		
}
sub npc_use_pet_loptr { # ﾛﾌﾟﾄ
	$w{game_lv} -= 1 if $w{game_lv} > 80;
	&write_world_news("$cs{name}[$w{country}]のﾛﾌﾟﾄ(NPC)の邪神の裁き!");
	&disaster;
}
sub npc_use_pet_pesto { # ﾍﾟｽﾄ
	$w{game_lv} -= 1 if $w{game_lv} > 75;
	for my $i (1..$w{country}) {
		$cs{state}[$i] = 5;
	}
	&write_world_news("<b>$cs{name}[$w{country}]の$npc_names[int(rand(@npc_names))]が猛毒を撒き散らし各国の$e2j{state}が $country_states[5] になりました</b>");
}
sub npc_use_pet_meteo { # ﾒﾃｵ
	$w{game_lv} -= 2 if $w{game_lv} > 85;
	for my $i (1..$w{country}) {
		for my $j ($i+1..$w{country}) {
			$w{"f_${i}_${j}"}=int(rand(20));
			$w{"p_${i}_${j}"}=2;
		}
	}
	&write_world_news("<b>$cs{name}[$w{country}]の$npc_names[int(rand(@npc_names))]がﾒﾃｵを唱え世界中が開戦となりました</b>");
}
sub npc_use_pet_prisoner { # 牢獄
	$w{game_lv} -= 1 if $w{game_lv} > 85;
	my @ks = (qw/war dom pro mil ceo/);
	my $k = $ks[int(rand(@ks))];

	for my $i (1 .. $w{country}-1) {
		next if $cs{$k}[$i] eq '';
		next if $cs{$k}[$i] eq $m{name};
		
		&regist_you_data($cs{$k}[$i], 'lib', 'prison');
		&regist_you_data($cs{$k}[$i], 'tp',  100);
		&regist_you_data($cs{$k}[$i], 'y_country',  $w{country});
		
		open my $fh, ">> $logdir/$w{country}/prisoner.cgi" or &error("$logdir/$w{country}/prisoner.cgi が開けません");
		print $fh "$cs{$k}[$i]<>$i<>\n";
		close $fh;
	}
	&write_world_news("<b>$cs{name}[$w{country}]の$npc_names[int(rand(@npc_names))]が不気味な光を放ち各国の $e2j{$k} が$cs{name}[$w{country}]の牢獄に幽閉されました</b>");
}
sub npc_get_strong { # 奪国
	# 資源が足らないとき
	for my $k (qw/food money soldier/) {
		return if $cs{$k}[$w{country}] < 100000;
	}
	
	my $country = 1;
	if ($cs{strong}[$w{country}] < 40000) { # 一番国力が高い国を選択
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
	
	return if $cs{is_die}[$country];        # 滅亡国からは奪わない
	return if $cs{strong}[$country] < 1000; # 国力1000未満は奪わない
	
	# その国の相手の名前をﾗﾝﾀﾞﾑ取得
	my $name = '';
	open my $fh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが読み込めません");
	rand($.) < 1 and $name = $_ while <$fh>;
	close $fh;
	$name =~ tr/\x0D\x0A//d;
	
	my $v = int(rand(300)+300);

	$cs{strong}[$w{country}] += $v;
	$cs{strong}[$country]    -= $v;
	&write_world_news(qq|$cs{name}[$w{country}]の$npc_names[int(rand(@npc_names))]が$cs{name}[$country]に侵攻、$nameの部隊を撃破し <font color="#FF00FF"><b>$v</b> の$e2j{strong}を奪うことに成功</font>したようです|);

	$cs{is_die}[$w{country}] = 0 if $cs{is_die}[$w{country}];
}


#=================================================
# 同じ人が何度もNPC国に仕官しないように制御
#=================================================
sub is_move_npc_country {
	my @lines = ();
	open my $fh, "+< $logdir/$w{country}/old_member.cgi" or &error("$logdir/$w{country}/old_member.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		if ($line eq $m{name}) {
			close $fh;
			$mes .= "過去にNPC国へ仕官した人は、しばらくNPC国へ仕官することは許されません<br>";
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
		$mes .= "$c_mの$e2j{ceo}を辞任する必要があります<br>";
		&begin;
		return 0;
	}
	
	# 代表ﾎﾟｲﾝﾄ0
	for my $k (qw/war dom mil pro/) {
		$m{$k.'_c'} = int($m{$k.'_c'} * 0);
	}
	&mes_and_world_news("悪魔に魂を売り渡しました", 1);

	return 1;
}



1;
