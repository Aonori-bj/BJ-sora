#=================================================
# 軍事 Created by Merino
#=================================================

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '国に属してないと行うことができません<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	elsif ($time < $w{reset_time}) {
		$mes .= '終戦期間中は戦争と軍事はできません<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "他に何か行いますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= '軍事を行います<br>どれを行いますか?<br>';
	}
	&menu('やめる','食料を強奪','資金を奪う','兵士を洗脳','内部偵察','偽計','待ち伏せ');
}
sub tp_1 {
	return if &is_ng_cmd(1..6);
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '6') {
		$mes .= "敵国からの軍事行為を見張ったり、敵国からの進軍を待ち伏せして撹乱させます($GWT分〜)<br>";
		$mes .= "どちらの待ち伏せをしますか?<br>";
		&menu('やめる', '軍事行為を見張る', '進軍を待ち伏せ');
	}
	else { # 1-5
		if    ($cmd eq '1') { $mes .= "相手国に忍び込み食料を奪います<br>" }
		elsif ($cmd eq '2') { $mes .= "相手国の資金ﾙｰﾄを撹乱しお金を流出させます<br>" }
		elsif ($cmd eq '3') { $mes .= "相手国の兵士を洗脳し、自国の兵士にします<br>" }
		elsif ($cmd eq '4') { $mes .= "相手国の内部の状態を詮索しに行きます<br>" }
		elsif ($cmd eq '5') { $mes .= "相手国に悪い噂\を流し友好度を下げます<br>" }
		$mes .= "どの国に向かいますか?($GWT分)<br>";
		&menu('やめる', @countries);
	}
}

#=================================================
# 待ち伏せ
#=================================================
sub tp_600 {
	if ($cmd eq '1') {
		$mes .= "敵国からの軍事行為がないか自国を巡回し監視します<br>";
		$mes .= "待ち伏せの有効時間は最高で$max_ambush_hour時間までです<br>";
		$mes .= "次に行動できるのは$GWT分後です<br>";
		$m{tp} += 10;
		
		# 戦争と同じ仕組みでもいいけど、相手のｽﾃｰﾀｽが必要ないのと、ﾌｧｲﾙｵｰﾌﾟﾝ１回ですむので。
		open my $fh, ">> $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgiﾌｧｲﾙが開けません");
		print $fh "$time<>$m{name}<>\n";
		close $fh;
		
		&wait;
	}
	elsif ($cmd eq '2') {
		$mes .= "敵国からの進軍を待ち伏せします<br>";
		$mes .= "待ち伏せの有効時間は最高で$max_ambush_hour時間です<br>";
		$mes .= "次に行動できるのは$GWT分後です<br>";
		$m{value} = 'ambush';
		$m{tp} += 10;
		&wait;
	}
	else {
		&begin;
	}
}
sub tp_610 {
	$m{turn} = 1;
	$mes .= "待ち伏せを終了しました<br>";
	
	# 待ち伏せにひっかかった数
	if (-s "$userdir/$id/ambush.cgi") {
		open my $fh, "+< $userdir/$id/ambush.cgi" or &error("$userdir/$id/ambush.cgiファイルが読み込めません");
		eval { flock $fh, 2 };
		my $line = <$fh>;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
		
		my @lines = split /<>/, $line;
		$mes .= join ",<br>", @lines;
		$mes .= "<br>を待ち伏せで撃退しました!<br>";
		$m{turn} = @lines;
	}

	&c_up('mat_c') for 1 .. $m{turn};
	&use_pet('mat');
	&tp_1000;
	
	# 軍事待ち伏せの時、巡回ファイルから自分を除く処理
	unless ($m{value} eq 'ambush') {
		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($pat_time,$name) = split /<>/, $line;
			next if $name eq $m{name};
			push @lines, $line;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}


#=================================================
# 軍事ｾｯﾄ
#=================================================
sub tp_100 { &exe1("食料を強奪しに") }
sub tp_200 { &exe1("資金ﾙｰﾄを撹乱しに") }
sub tp_300 { &exe1("兵士を洗脳しに") }
sub tp_400 { &exe1("内部情勢を偵察しに") }
sub tp_500 { &exe1("偽計をしに") }
sub exe1 {
	return if &is_ng_cmd(1..$w{country});
	
	if ($m{country} eq $cmd) {
		$mes .= '自国は選べません<br>';
		&begin;
	}
	elsif ($union eq $cmd) {
		$mes .= '同盟国は選べません<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd]) {
		$mes .= '滅亡している国は選べません<br>';
		&begin;
	}
	else {
		$m{tp} += 10;
		$y{country} = $cmd;
		
		# 世界情勢「迷走」
		if ($w{world} eq '16') {
			$y{country} = int(rand($w{country}))+1;
			$y{country} = &get_most_strong_country if rand(3) < 1 || $cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union;
		}
		
		$mes .= "$_[0]$cs{name}[$y{country}]に向かいました<br>";
		$mes .= "$GWT分後に到着する予\定です<br>";
		
		if ($y{country} eq $m{renzoku}) {
			++$m{renzoku_c};
		}
		else {
			$m{renzoku} = $y{country};
			$m{renzoku_c} = 1;
		}
		
		&wait;
	}
}

#=================================================
# 軍事処理
#=================================================
sub tp_110 { &form1('食料を奪う') }
sub tp_210 { &form1('諜報を行う') }
sub tp_310 { &form1('洗脳を行う') }
sub tp_410 { &form1('情勢を探る') }
sub tp_510 { &form1('悪い噂\を流す') }
sub form1 {
	$mes .= "$c_yに到着しました<br>";
	$m{tp} += 10;
	$m{value} = int(rand(20))+5;
	$m{value} += 30 if $y{country} && $pets[$m{pet}][2] ne 'no_ambush' && &is_patrol($_[0]);
	$m{stock} = 0;
	$m{turn} = 0;
	$mes .= "敵兵の気配【 $m{value}% 】<br>";
	$mes .= 'どうしますか?<br>';
	&menu($_[0],'引きあげる');
	$m{value} += int(rand(10)+1);
}


#=================================================
# ﾙｰﾌﾟｺﾏﾝﾄﾞ 失敗するかやめない限り続く(tp固定)
#=================================================
sub loop_menu {
	$mes .= "敵兵の気配【 $m{value}% 】<br>";
	$mes .= 'どうしますか?';
	&menu('続ける', 'やめる');
}
sub tp_120 { &exe2 }
sub tp_220 { &exe2 }
sub tp_320 { &exe2 }
sub tp_420 { &exe2 }
sub tp_520 { &exe2 }
sub exe2 {
	if ($cmd eq '0') { # 実行
		if ( $m{value} > rand(110)+35 ) { # 失敗 単純にrand(100)にすると30%くらいで見つかってしまうので rand(110)+30に変更
			$mes .= "敵兵に見つかってしまった!!<br>";
			
			$m{tp} = 900;
			&n_menu;
		}
		else { # 成功
			++$m{turn};
			$m{tp} += 10;
			&{ 'tp_'.$m{tp} };
			&loop_menu;
			$m{tp} -= 10;
		}
		$m{value} += int(rand(10)+1);
	}
	elsif ($cmd eq '1') { # 退却
		$mes .= '引き上げることにします<br>';
		
		if ($m{turn} <= 0) { # 何もしないで引き上げ
			&refresh;
			&n_menu;
		}
		elsif ($m{tp} eq '420') { # 内部偵察
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
		}
		else {
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
			$m{tp} = 1000;
			&n_menu;
		}
	}
	else {
		&loop_menu;
	}
}

#=================================================
# 成功
#=================================================
sub tp_130 { # 強奪成功
	my $v = int( ($m{gou_c} + $m{at}) * $m{turn} * rand(4) );
	$v  = int(rand(500)+2000) if $v > 2500;
	$v *= 2 if $w{world} eq '4' || $w{world} eq '6';
	$m{stock} += $v;
	
	if ($m{stock} > $cs{food}[$y{country}]) {
		$mes .= "$c_yの食料が尽きました!<br>";
		$m{stock} = $cs{food}[$y{country}];
	}
	else {
		$mes .= "$vの食料強奪に成功しました!<br>";
	}
	$mes .= "[ 連続$m{turn}回成功 ﾄｰﾀﾙ強奪 $m{stock} ]<br>";

}
sub tp_230 { # 諜報成功
	my $v = int( ($m{cho_c} + $m{mat}) * $m{turn} * rand(4) );
	$v  = int(rand(500)+2000) if $v > 2500;
	$v *= 2 if $w{world} eq '4' || $w{world} eq '6';
	$m{stock} += $v;

	if ($m{stock} > $cs{money}[$y{country}]) {
		$mes .= "$c_yの$e2j{money}が尽きました!<br>";
		$m{stock} = $cs{money}[$y{country}];
	}
	else {
		$mes .= "$vの資金流出に成功しました!<br>";
	}
	$mes .= "[ 連続$m{turn}回成功 ﾄｰﾀﾙ諜報 $m{stock} ]<br>";
}
sub tp_330 { # 洗脳成功
	my $v = int( ($m{sen_c} + $m{cha}) * $m{turn} * rand(4) );
	$v  = int(rand(500)+1500) if $v > 2000;
	$v *= 2 if $w{world} eq '4' || $w{world} eq '6';
	$m{stock} += $v;

	if ($m{stock} > $cs{soldier}[$y{country}]) {
		$mes .= "$c_yの兵士がもういません!<br>";
		$m{stock} = $cs{soldier}[$y{country}];
	}
	else {
		$mes .= "$v人の兵士洗脳に成功しました!<br>";
	}

	$mes .= "[ 連続$m{turn}回成功 ﾄｰﾀﾙ洗脳 $m{stock} ]<br>";
}
sub tp_430{ # 偵察
	$mes .= $m{turn} eq '1' ? "$e2j{food}の情報を手に入れました!<br>"
		  : $m{turn} eq '2' ? "$e2j{money}の情報を手に入れました!<br>"
		  : $m{turn} eq '3' ? "$e2j{soldier}の情報を手に入れました!<br>"
		  : $m{turn} eq '4' ? "$e2j{tax}の情報を手に入れました!<br>"
		  : $m{turn} eq '5' ? "$e2j{state}の情報を手に入れました!<br>"
		  : $m{turn} eq '6' ? "$e2j{strong}の情報を手に入れました!<br>"
		  : $m{turn} >   7  ? "会議室の会話を聞きました!<br>"
		  :                   "城内部へと向かってみます<br>"
		  ;
}
sub tp_530{ # 偽計
	my $v = $m{turn} >= 2 ? int($m{turn} * 0.85) : 1;
	$mes .= "嘘の情報を流すのに成功しました!<br>[ 連続$m{turn}回成功 ﾄｰﾀﾙ偽計 $v% ]<br>";
}


#=================================================
# 引き上げ
#=================================================
sub tp_140 { # 強奪
	&c_up('gou_c') for 1 .. $m{turn};
	$m{stock} = &use_pet('gou', $m{stock});
	my $v = &exe3('food');
	
	&mes_and_world_news("$c_yに奇襲攻撃を実施。$vの兵糧を強奪することに成功しました");
}
sub tp_240 { # 諜報
	&c_up('cho_c') for 1 .. $m{turn};
	$m{stock} = &use_pet('cho', $m{stock});
	my $v = &exe3('money');
	
	&mes_and_world_news("$c_yの資金調達ﾙｰﾄを撹乱し、$vの$e2j{money}を流出させることに成功しました");
}
sub tp_340 { # 洗脳
	&c_up('sen_c') for 1 .. $m{turn};
	$m{stock} = &use_pet('sen', $m{stock});
	my $v = &exe3('soldier');
	
	&mes_and_world_news("$c_yの$vの兵を洗脳することに成功!$c_mの兵に取り込みました");
}
sub exe3 {
	my $k = shift;
	
	my $v = $m{stock} > $cs{$k}[$y{country}] ? int($cs{$k}[$y{country}]) : int($m{stock});
	$cs{$k}[$y{country}] -= $v;
	$cs{$k}[$m{country}] += $v;
	
	&write_cs;
	return $v;
}

# ----------------------------
sub tp_440 { # 偵察
	$mes .= "【$c_yの情報】<br>";
	$mes .= "$e2j{food}：$cs{food}[$y{country}] <br>"       if $m{turn} >= 1;
	$mes .= "$e2j{money}：$cs{money}[$y{country}] <br>"     if $m{turn} >= 2;
	$mes .= "$e2j{soldier}：$cs{soldier}[$y{country}] <br>" if $m{turn} >= 3;
	$mes .= "$e2j{tax}：$cs{tax}[$y{country}]% <br>"        if $m{turn} >= 4;
	$mes .= "$e2j{state}：$country_states[ $cs{state}[$y{country}] ]<br>" if $m{turn} >= 5;
	$mes .= "$e2j{strong}：$cs{strong}[$y{country}] <br>"   if $m{turn} >= 6;
	$mes .= "上記の情報を$c_mの会議室に報告しますか?<br>";
	&menu('やめる','報告する');
	$m{tp} += 10;
}	
sub tp_450 {
	&c_up('tei_c') for 1 .. $m{turn};
	&use_pet('tei');
	
	if ($m{turn} > 7) {
		$mes .= "$c_yの会議室の情報をいくつか盗み聞きできた<br>";
		
		my $count = 7;
		my @bbs_logs = ();
		open my $fh, "< $logdir/$y{country}/bbs.cgi" or &error("BBSログが読み込めません");
		while (my $line = <$fh>) {
			my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
			$mes .= "$bcomment<br>";
			last if ++$count > $m{turn};
		}
		close $fh;
	}

	# BBSに追記
	if ($cmd eq '1') {
		my $comment = "【$c_y】";
		$comment .= "$e2j{food}：$cs{food}[$y{country}]/"       if $m{turn} >= 1;
		$comment .= "$e2j{money}：$cs{money}[$y{country}]/"     if $m{turn} >= 2;
		$comment .= "$e2j{soldier}：$cs{soldier}[$y{country}]/" if $m{turn} >= 3;
		$comment .= "$e2j{tax}：$cs{tax}[$y{country}]%/"        if $m{turn} >= 4;
		$comment .= "$e2j{state}：$country_states[ $cs{state}[$y{country}] ]/" if $m{turn} >= 5;
		$comment .= "$e2j{strong}：$cs{strong}[$y{country}]/"   if $m{turn} >= 6;

		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/bbs.cgi" or &error("$logdir/$m{country}/bbs.cgi ﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		push @lines, $_ while <$fh>;
		pop @lines;
		unshift @lines, "$time<>$date<>$m{name}<>$m{country}<>$m{shogo}<>$addr<>$comment<>$m{icon}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		$mes .= "$c_mの会議室に報告しました<br>";
	}
	else {
		$mes .= "$m{name}の胸の内に秘めておくことにしました<br>";
	}

	$m{tp} = 1000;
	&n_menu;
}

# ----------------------------
sub tp_540 { # 偽計
	&c_up('gik_c') for 1 .. $m{turn};
	&use_pet('gik');
	my $v = $m{turn} >= 2 ? int($m{turn} * 0.85) : 1;
	for my $i (1 .. $w{country}) {
		next if $y{country} eq $i;
		
		my $u  = &union($y{country}, $i);
		$w{"f_$u"} -= $v;
		
		if ($w{"f_$u"} < rand(10)) {
			if ($w{"p_$u"} eq '1' && $w{world} ne '7') {
				$w{"p_$u"} = 0;
				&mes_and_world_news("<b>偽計により$c_yと$cs{name}[$i]との同盟を決裂させました</b>");
			}
			
			$w{"f_$u"} = int(rand(10));
		}
	}
	
	$mes .= "$c_yと他国の友好度を$v%下げるのに成功しました<br>";
	$m{tp} = 1000;
	&n_menu;
	&write_cs;
}



#=================================================
# 失敗
#=================================================
sub tp_900 {
	$m{act} += $m{turn};

	# 連続で同じ国だと高確率でﾀｲｰﾎ
	&refresh;
	if ( ($w{world} eq '12' && $m{renzoku_c} > rand(4) ) || $m{renzoku_c} > rand(7) + 2 ) {
		&write_world_news("$c_mの$m{name}が軍事任務に失敗し$c_yの牢獄に幽閉されました");
		&add_prisoner;
	}
	else { # 退却成功
		$mes .= "なんとか敵兵を振り切ることができました<br>";
		&n_menu;
	}
	my $v = int( (rand(4)+1) );
	$m{exp} += $v;
	$m{rank_exp}-= int(rand(6)+5);
	$mes .= "$vの$e2j{exp}を手に入れました<br>";
	$mes .= "任務に失敗したため、$m{name}に対する評価が下がりました<br>";
}


#=================================================
# 成功
#=================================================
sub tp_1000 {
	$m{act} += $m{turn};

	my $v = int( (rand(3)+3) * $m{turn} );
	$v = &use_pet('military', $v);
	$m{exp} += $v;
	$mes .= "$vの$e2j{exp}を手に入れました<br>";
	$m{egg_c} += int(rand($m{turn})+$m{turn}) if $m{egg};

	if ($m{turn} >= 5) {
		$mes .= "任務に大成功!$m{name}に対する評価が大きく上がりました<br>";
		$m{rank_exp} += $m{turn} * 3;
	}
	else {
		$mes .= "任務に成功!$m{name}に対する評価が上がりました<br>";
		$m{rank_exp} += int($m{turn} * 1.5);
	}
	
	&daihyo_c_up('mil_c'); # 代表熟練度
	
	if ( $w{world} eq $#world_states && ( rand(12) < 1 || ($cs{strong}[$w{country}] < 50000 && rand(4) < 1) ) ) {
		require './lib/vs_npc.cgi';
		&npc_military;
	}

	&write_cs;
	&refresh;
	&n_menu;
}


#=================================================
# 軍事待ち伏せの見張りがいる？
#=================================================
sub is_patrol {
	my $military_kind = shift;
	my %sames = ();
	my @lines = ();
	open my $fh, "+< $logdir/$y{country}/patrol.cgi" or &error("$logdir/$y{country}/patrol.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($pat_time,$name) = split /<>/, $line;
		next if $time > $pat_time + $max_ambush_hour * 3600;
		next if ++$sames{$name} > 1;
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	# 所属人数に対してどれくらい巡回しているか
	my $p = $w{world} eq $#world_states && $y{country} eq $w{country} ? 80 : 30;
	if (@lines > 0 && (@lines / ($cs{member}[$y{country}]+1) * 100) >= rand($p) ) {
		my $a = @lines;
		my $line = $lines[rand(@lines)];
		my($pat_time,$name) = split /<>/, $line;
		&mes_and_world_news("$c_yに軍事行為を実行。巡回していた$nameの監視の目が光りました");
		
		my $yid = unpack 'H*', $name;
		if (-d "$userdir/$yid") {
			open my $fh, ">> $userdir/$yid/ambush.cgi";
			print $fh "$m{name}$military_kind($date)<>";
			close $fh;
		}

		return 1;
	}
	return 0;
}


1; # 削除不可
