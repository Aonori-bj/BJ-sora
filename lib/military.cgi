#=================================================
# 軍事 Created by Merino
#=================================================

$gik_limit = 10; # 偽計の上限

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '国に属してないと行うことができません<br>仕官するには「国情報」→「仕官」から行ってみたい国を選んでください<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	elsif ($time < $w{reset_time}) {
		$mes .= '終戦期間中は戦争と軍事はできません<br>';
		if ($m{value} eq 'military_ambush'){
			open my $fh, "+< $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgiﾌｧｲﾙが開けません");
			eval { flock $fh, 2; };
			seek  $fh, 0, 0;
			truncate $fh, 0;
			close $fh;
		}
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
	if($m{gou_c} >= 50 && $m{cho_c} >= 50 && $m{sen_c} >= 50){
		&menu('やめる','食料を強奪','資金を奪う','兵士を洗脳','内部偵察','偽計','攻城','待ち伏せ','食料を強奪(長期)','資金を奪う(長期)','兵士を洗脳(長期)');
	}else{
		&menu('やめる','食料を強奪','資金を奪う','兵士を洗脳','内部偵察','偽計','攻城','待ち伏せ');
	}
}
sub tp_1 {
	if($m{gou_c} >= 50 && $m{cho_c} >= 50 && $m{sen_c} >= 50){
		return if &is_ng_cmd(1..10);
	}else{
		return if &is_ng_cmd(1..7);
	}

	$m{tp} = $cmd * 100;
	if ($cmd eq '7') {
		$mes .= "敵国からの軍事行為を見張ったり、敵国からの進軍を待ち伏せして撹乱させます($GWT分〜)<br>";
		$mes .= "どちらの待ち伏せをしますか?<br>";
		&menu('やめる', '軍事行為を見張る', '進軍を待ち伏せ');
	}
	else { # 1-6 8-10
		if    ($cmd eq '1')  { $mes .= "相手国に忍び込み食料を奪います<br>"; }
		elsif ($cmd eq '2')  { $mes .= "相手国の資金ﾙｰﾄを撹乱しお金を流出させます<br>"; }
		elsif ($cmd eq '3')  { $mes .= "相手国の兵士を洗脳し、自国の兵士にします<br>"; }
		elsif ($cmd eq '4')  { $mes .= "相手国の内部の状態を詮索しに行きます<br>"; }
		elsif ($cmd eq '5')  { $mes .= "相手国に悪い噂\を流し友好度を下げます<br>"; }
		elsif ($cmd eq '6')  { $mes .= "相手国の城壁を破壊し、防御力を下げます<br>"; }
		elsif ($cmd eq '8')  { $mes .= "相手国に忍び込み大目に食料を奪います<br>"; $GWT *= 2.5; }
		elsif ($cmd eq '9')  { $mes .= "相手国の資金ﾙｰﾄを撹乱し大目にお金を流出させます<br>"; $GWT *= 2.5; }
		elsif ($cmd eq '10') { $mes .= "相手国の兵士を大目に洗脳し、自国の兵士にします<br>"; $GWT *= 2.5; }
		$mes .= "どの国に向かいますか?($GWT分)<br>";
		&menu('やめる', @countries);
	}
}

#=================================================
# 待ち伏せ
#=================================================
sub tp_700 {
	#require './lib/_rampart.cgi'; # 城壁
	if ($cmd eq '1') {
		$mes .= "敵国からの軍事行為がないか自国を巡回し監視します<br>";
		$mes .= "待ち伏せの有効時間は最高で$max_ambush_hour時間までです<br>";
		$mes .= "次に行動できるのは$GWT分後です<br>";
		$m{tp} += 10;
		$m{value} = 'military_ambush';

		# 戦争と同じ仕組みでもいいけど、相手のｽﾃｰﾀｽが必要ないのと、ﾌｧｲﾙｵｰﾌﾟﾝ１回ですむので。
		open my $fh, ">> $logdir/$m{country}/patrol.cgi" or &error("$logdir/$m{country}/patrol.cgiﾌｧｲﾙが開けません");
		print $fh "$time<>$m{name}<>\n";
		close $fh;

		#&before_action('icon_pet_exp', $GWT);
		#&gain_mil_barrier(1);
		&wait;
	}
	elsif ($cmd eq '2') {
		$mes .= "敵国からの進軍を待ち伏せします<br>";
		$mes .= "待ち伏せの有効時間は最高で$max_ambush_hour時間です<br>";
		$mes .= "次に行動できるのは$GWT分後です<br>";
		$m{value} = 'ambush';
		$m{tp} += 10;

		#&before_action('icon_pet_exp', $GWT);
		#&gain_mil_barrier(1);
		&wait;
	}
	else {
		&begin;
	}
}
sub tp_710 {
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

	# 軍事待ち伏せの時、巡回ファイルから自分を除く処理
	if ($m{value} ne 'ambush') {
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

		#&run_tutorial_quest('tutorial_mil_ambush_1');
	}elsif (-s "$userdir/$id/war.cgi") {
		open my $fh, "+< $userdir/$id/war.cgi" or &error("$userdir/$id/war.cgiﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $result) = split /<>/, $line;

			if ($result eq '0') {
				$mes .= "$nameを撃退しました<br>";
			}
			elsif ($result eq '1') {
				$mes .= "$nameに敗北しました<br>";
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
=pod
		unless (&gain_mil_barrier(chomp($head_line))) {
			my($name, $result) = split /<>/, $head_line;
			if ($result eq '0') {
				$mes .= "$nameを撃退しました<br>";
			}
			elsif ($result eq '1') {
				$mes .= "$nameに敗北しました<br>";
			}
		}
=cut
	}

	&special_money($m{turn} * 500);
	&c_up('mat_c') for 1 .. $m{turn};
	&military_master_c_up('mat_c');
	&use_pet('mat') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '32');

	#require './lib/_rampart.cgi'; # 城壁
	#&gain_mil_barrier(0);

	&tp_1100;
}

#=================================================
# 軍事ｾｯﾄ
#=================================================
sub tp_100 { &exe1("食料を強奪しに") }
sub tp_200 { &exe1("資金ﾙｰﾄを撹乱しに") }
sub tp_300 { &exe1("兵士を洗脳しに") }
sub tp_400 { &exe1("内部情勢を偵察しに") }
sub tp_500 { &exe1("偽計をしに") }
sub tp_600 { &exe1('攻城をしに') }
sub tp_800 { &exe1("食料を大目に強奪しに") }
sub tp_900 { &exe1("資金ﾙｰﾄを大目に撹乱しに") }
sub tp_1000 { &exe1("兵士を大目に洗脳しに") }
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
		if (($w{world} eq '15' || ($w{world} eq '19' && $w{world_sub} eq '15'))) {
			$y{country} = int(rand($w{country}))+1;
			if ($cs{is_die}[&get_most_strong_country]){
				my $loop = 0;
				while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
					if($loop > 30) {
						$y{country} = &get_most_strong_country;
					}
					$y{country} = int(rand($w{country}))+1;
					$loop++;
				}
			}else {
				$y{country} = &get_most_strong_country if rand(3) < 1 || $cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union;
			}
		} elsif ($w{world} eq $#world_states - 5) {
			$y{country} = int(rand($w{country}))+1;
			my $loop = 0;
			while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
				if($loop > 30) {
					$y{country} = &get_most_strong_country;
				}
				$y{country} = int(rand($w{country}))+1;
				$loop++;
			}
		}

		$GWT *= 2.5 if $m{tp} >= 810 && $m{tp} <= 1010;
		$mes .= "$_[0]$cs{name}[$y{country}]に向かいました<br>";
		$mes .= "$GWT分後に到着する予\定です<br>";

		$m{renzoku_c} = $y{country} eq $m{renzoku} ? $m{renzoku_c} + 1 : 1;
		$m{renzoku} = $y{country};

		#&before_action('icon_pet_exp', $GWT);
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
sub tp_610 { &form1('攻城を行う') }
sub tp_810 { &form1('食料を奪う(長期)') }
sub tp_910 { &form1('諜報を行う(長期)') }
sub tp_1010 { &form1('洗脳を行う(長期)') }
sub form1 {
	$mes .= "$c_yに到着しました<br>";

	$m{tp} += 10;
	$m{value} = int(rand(20))+5;#$config_test ? 0 : int(rand(20))+5;
	$m{value} += int(rand(10)+1);#$config_test ? 0 : int(rand(10)+1); # ゲームバランスを考えて初期値ﾌﾞｰｽﾄはそのまま
	$m{value} += 30 if $y{country} && ($pets[$m{pet}][2] ne 'no_ambush' || ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) && &is_patrol($_[0]);
	if ($m{pet} == -1) { # ﾕｰﾚｲの埋め込み処理
		$m{pet_c}--;
		if ($m{pet_c} <= 0) {
			$m{pet} = 0;
			$m{pet_c} = 0;
		}
	}

	$m{stock} = 0;
	$m{turn} = 0;
	$mes .= "敵兵の気配【 $m{value}% 】<br>";
	$mes .= 'どうしますか?<br>';
	&menu($_[0],'引きあげる');
#	$m{value} += int(rand(10)+1); merino の消し忘れ？
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
sub tp_620 { &exe2 }
sub tp_820 { &exe2 }
sub tp_920 { &exe2 }
sub tp_1020 { &exe2 }
sub exe2 {
	if ($cmd eq '0') { # 実行
		if ( $m{value} > rand(110)+35 ) { # 失敗 単純にrand(100)にすると30%くらいで見つかってしまうので rand(110)+30に変更
			$mes .= "敵兵に見つかってしまった!!<br>";
			$m{tp} = 1900;
			&n_menu;
		}
		else { # 成功
			++$m{turn};
			$m{tp} += 10;
			&{ 'tp_'.$m{tp} };
			if($m{tp} == 420 && $m{turn} < 7){
				my $tei_sp = rand($m{tei_c} / 500);
				$m{value} += $tei_sp > 5 ? int(rand(5)+1): int(rand(10-$tei_sp)+1);
			} else {
				$m{value} += int( $m{unit} eq '17' ? (rand(10)+1)*(0.7+rand(0.3)) : rand(10)+1 ); # 隠密は上昇気配値0〜8？ 通常部隊は1〜10
			}
			&loop_menu;
			$m{tp} -= 10;
		}
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
			my $tmp_tp = $m{tp};
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
			$m{tp} = 1100;
			if ($tmp_tp eq '120' || $tmp_tp eq '220' || $tmp_tp eq '320' ||
				$tmp_tp eq '820' || $tmp_tp eq '920' || $tmp_tp eq '1020') {
				#&run_tutorial_quest('tutorial_mil_1');
			}
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
sub get_mil_success {
	my $v = int( ($m{"$_[0]_c"} + $m{$_[1]}) * $m{turn} * rand($_[3]) );
	$v  = int(rand(500)+$_[2]-500) if $v > $_[2];
	$v *= 2 if $w{world} eq '3' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '3' || $w{world_sub} eq '5'));
	$v *= 2 if $cs{extra}[$m{country}] eq '2' && $cs{extra_limit}[$m{country}] >= $time;
	$m{stock} += $v;
	return $v;
}
sub get_mil_message {
	if ($m{stock} > $cs{$_[0]}[$y{country}]) {
		$mes .= "$c_yの$_[3]";
		$m{stock} = $cs{$_[0]}[$y{country}];
	} else {
		$mes .= "$_[2]";
	}
	$mes .= "<br>[ 連続$m{turn}回成功 ﾄｰﾀﾙ$_[1] $m{stock} ]<br>";
}
sub tp_130 { # 強奪成功
	my $v = &get_mil_success('gou', 'at', 3000, 4);
	&get_mil_message('food', '強奪', "$vの食料強奪に成功しました!", "食料が尽きました!");
}
sub tp_230 { # 諜報成功
	my $v = &get_mil_success('cho', 'mat', 3000, 4);
	&get_mil_message('money', '諜報', "$vの資金流出に成功しました!", "$e2j{money}が尽きました!");
}
sub tp_330 { # 洗脳成功
	my $v = &get_mil_success('sen', 'cha', 2500, 4);
	&get_mil_message('soldier', '洗脳', "$v人の兵士洗脳に成功しました!", "兵士がもういません!");
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
	my $v = $m{turn} <= 1 ? 1:
	      	$m{gik_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{gik_c}) / 2900);
	$v = $gik_limit if $v > $gik_limit;
	$mes .= "嘘の情報を流すのに成功しました!<br>[ 連続$m{turn}回成功 ﾄｰﾀﾙ偽計 $v% ]<br>";
}
sub tp_630{ # 攻城
	my $v = $m{turn} <= 1 ? 1:
	      	$m{kou_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{kou_c}) / 2900);
	$mes .= "城壁を破壊するのに成功しました!<br>[ 連続$m{turn}回成功 ﾄｰﾀﾙ攻城 $v% ]<br>";
}
sub tp_830 { # 強奪成功
	my $v = &get_mil_success('gou', 'at', 4500, 6);
	&get_mil_message('food', '強奪', "$vの食料強奪に成功しました!", "食料が尽きました!");
}
sub tp_930 { # 諜報成功
	my $v = &get_mil_success('cho', 'mat', 4500, 6);
	&get_mil_message('money', '諜報', "$vの資金流出に成功しました!", "$e2j{money}が尽きました!");
}
sub tp_1030 { # 洗脳成功
	my $v = &get_mil_success('sen', 'cha', 4000, 6);
	&get_mil_message('soldier', '洗脳', "$v人の兵士洗脳に成功しました!", "兵士がもういません!");
}

#=================================================
# 引き上げ
#=================================================
sub tp_140 { # 強奪
	my $v = &exe3('food', 'gou');
	&mes_and_world_news("$c_yに奇襲攻撃を実施。$vの兵糧を強奪することに成功しました");
}
sub tp_240 { # 諜報
	my $v = &exe3('money', 'cho');
	&mes_and_world_news("$c_yの資金調達ﾙｰﾄを撹乱し、$vの$e2j{money}を流出させることに成功しました");
}
sub tp_340 { # 洗脳
	my $v = &exe3('soldier', 'sen');
	&mes_and_world_news("$c_yの$vの兵を洗脳することに成功!$c_mの兵に取り込みました");
}
sub tp_840 { # 強奪
	my $v = &exe3('food', 'gou');
	&mes_and_world_news("$c_yに奇襲攻撃を実施。$vの兵糧を強奪することに成功しました");
}
sub tp_940 { # 諜報
	my $v = &exe3('money', 'cho');
	&mes_and_world_news("$c_yの資金調達ﾙｰﾄを撹乱し、$vの$e2j{money}を流出させることに成功しました");
}
sub tp_1040 { # 洗脳
	my $v = &exe3('soldier', 'sen');
	&mes_and_world_news("$c_yの$vの兵を洗脳することに成功!$c_mの兵に取り込みました");
}
sub exe3 {
	my $k = shift;
	my $l = shift;

	&c_up("${l}_c") for 1 .. $m{turn};
	&military_master_c_up("${l}_c");
	$m{stock} = &use_pet($l, $m{stock}) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '33');
	#$m{stock} = &seed_bonus($l, $m{stock});

	# 策士は奪軍事力1.1倍
	$m{stock} = int($m{stock} * 1.1) if  $cs{mil}[$m{country}] eq $m{name};
	# 君主は奪軍事力1.05倍、暴君時ならば1.2倍
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		my $ceo_value = ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05;
		$m{stock} = int($m{stock} * $ceo_value);
	}
#	$m{stock} = int($m{stock} * 1.05) if  $cs{ceo}[$m{country}] eq $m{name};
	$m{stock} = int($m{stock} * 1.1) if  $m{unit} eq '17';
	$m{stock} = int($m{stock} * 0.3) if  $m{unit} eq '18';

	# 各国設定
	#$m{stock} = int($m{stock} * &get_modify('mil'));
	# 獣化
	#$m{stock} = &seed_bonus('red_moon', $m{stock});

	my $v = $m{stock} > $cs{$k}[$y{country}] ? int($cs{$k}[$y{country}]) : int($m{stock});
	$cs{$k}[$y{country}] -= $v;
	$cs{$k}[$m{country}] += $v;

	&write_cs;

	&special_money(int($v * 0.1));
	#&write_yran($l, $v, 0,
					#{}"${l}_t", $v, 1) if $v > 0;	#←ここのインデント何これ？　by あおのり
	return $v;
}

# ----------------------------
sub tp_440 { # 偵察
	my $bbs_name = $cs{bbs_name}[$y{country}] eq '' ? "$cs{name}[$y{country}]作戦会議室" : $cs{bbs_name}[$y{country}];
	$mes .= "【$c_yの情報】$bbs_name<br>";
	$mes .= "$e2j{food}：$cs{food}[$y{country}] <br>"       if $m{turn} >= 1;
	$mes .= "$e2j{money}：$cs{money}[$y{country}] <br>"     if $m{turn} >= 2;
	$mes .= "$e2j{soldier}：$cs{soldier}[$y{country}] <br>" if $m{turn} >= 3;
	$mes .= "$e2j{tax}：$cs{tax}[$y{country}]% <br>"        if $m{turn} >= 4;
	$mes .= "$e2j{state}：$country_states[ $cs{state}[$y{country}] ]<br>" if $m{turn} >= 5;
	$mes .= "$e2j{strong}：$cs{strong}[$y{country}] <br>"   if $m{turn} >= 6;
	$mes .= "城壁：$cs{barrier}[$y{country}]% <br>"             if $m{turn} >= 7;
	$mes .= "上記の情報を$c_mの会議室に報告しますか?<br>";
	&menu('やめる','報告する');
	$m{tp} += 10;
}
sub tp_450 {
	my $bbs_name = $cs{bbs_name}[$y{country}] eq '' ? "$cs{name}[$y{country}]作戦会議室" : $cs{bbs_name}[$y{country}];

	&c_up('tei_c') for 1 .. $m{turn};
	&military_master_c_up('tei_c');
	&use_pet('tei') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '36');
	&special_money($m{turn} * 500);

	my $lcomment = "$bbs_name<br>";
	my $need_count = 7;
	if ($m{turn} > $need_count) {
		$m{turn} += $m{turn} - $need_count if $w{world} eq '3' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '3' || $w{world_sub} eq '5'));
		#&write_yran('tei', $m{turn}-$need_count, 1);
		$mes .= "$c_yの会議室（$bbs_name）の情報をいくつか盗み聞きできた<br>";

		my $count = $need_count;
		my @bbs_logs = ();
		open my $fh, "< $logdir/$y{country}/bbs.cgi" or &error("BBSログが読み込めません");
		while (my $line = <$fh>) {
			my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
			$mes .= "$bcomment<br>";
			$lcomment .= "$bcomment<br>";
			last if ++$count > $m{turn};
		}
		close $fh;
	}

	# BBSに追記
	if ($cmd eq '1') {
		my $w_name = $m{name};
		$w_name = '名無し' if $w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16');
		my $comment = "【$c_y】";
		$comment .= "$e2j{food}：$cs{food}[$y{country}]/"       if $m{turn} >= 1;
		$comment .= "$e2j{money}：$cs{money}[$y{country}]/"     if $m{turn} >= 2;
		$comment .= "$e2j{soldier}：$cs{soldier}[$y{country}]/" if $m{turn} >= 3;
		$comment .= "$e2j{tax}：$cs{tax}[$y{country}]%/"        if $m{turn} >= 4;
		$comment .= "$e2j{state}：$country_states[ $cs{state}[$y{country}] ]/" if $m{turn} >= 5;
		$comment .= "$e2j{strong}：$cs{strong}[$y{country}]/"   if $m{turn} >= 6;
		$comment .= "城壁：$cs{barrier}[$y{country}]%/"         if $m{turn} >= 7;
		$comment .= "<br>$bbs_nameの会話を立ち聞きしました"     if $m{turn} > 7;

		my $comment2 = '';
		$comment2 .= $lcomment if $m{turn} > $need_count;

		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/bbs.cgi" or &error("$logdir/$m{country}/bbs.cgi ﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		push @lines, $_ while <$fh>;
		pop @lines if @lines > 50;
		unshift @lines, "$time<>$date<>$w_name<>$m{country}<>$m{shogo}<>$addr<>$comment<>$m{icon}<>$m{icon_pet}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		if($comment2){
			unless (-f "$logdir/$m{country}/bbs_log_$y{country}.cgi") {
				open my $fh2, "> $logdir/$m{country}/bbs_log_$y{country}.cgi" or &error("$logdir/$m{country}/bbs_log_$y{country}.cgi ﾌｧｲﾙが開けません");
				close $fh2;
			}

			my @lines2 = ();
			open my $fh2, "+< $logdir/$m{country}/bbs_log_$y{country}.cgi" or &error("$logdir/$m{country}/bbs_log_$y{country}.cgi ﾌｧｲﾙが開けません");
			eval { flock $fh2, 2; };
			push @lines2, $_ while <$fh2>;
			if(@lines2 > 50){
				pop @lines2;
			}
			unshift @lines2, "$time<>$date<>$w_name<>$m{country}<>$m{shogo}<>$addr<>$comment2<>$m{icon}<>\n";
			seek  $fh2, 0, 0;
			truncate $fh2, 0;
			print $fh2 @lines2;
			close $fh2;
		}

		$mes .= "$c_mの会議室に報告しました<br>";
	}
	else {
		$mes .= "$m{name}の胸の内に秘めておくことにしました<br>";
	}

	$m{tp} = 1100;
	&n_menu;
}

# ----------------------------
sub tp_540 { # 偽計
	&c_up('gik_c') for 1 .. $m{turn};
	&military_master_c_up('gik_c');
	&use_pet('gik') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '37');
	my $v = $m{turn} <= 1 ? 1:
	      	$m{gik_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{gik_c}) / 2900);
	$v = $gik_limit if $v > $gik_limit;
	#$v = &seed_bonus('gik', $v);
	#&write_yran('gik', $v, 1) if $v > 0;
	for my $i (1 .. $w{country}) {
		next if $y{country} eq $i;

		my $u  = &union($y{country}, $i);
		$w{"f_$u"} -= $v;

		if ($w{"f_$u"} < rand(10)) {
			if ($w{"p_$u"} eq '1' && $w{world} ne '6') {
				$w{"p_$u"} = 0;
				&mes_and_world_news("<b>偽計により$c_yと$cs{name}[$i]との同盟を決裂させました</b>");
				require './lib/shopping_offertory_box.cgi';
				&get_god_item(1);
				if ($w{world} eq $#world_states-4) {
					require './lib/fate.cgi';
					&super_attack('breakdown');
				}
			}

			$w{"f_$u"} = int(rand(10));
		}
	}

	&special_money($m{turn} * 500);
	$mes .= "$c_yと他国の友好度を$v%下げるのに成功しました<br>";
	$m{tp} = 1100;

	#&run_tutorial_quest('tutorial_gikei_1');

	&n_menu;
	&write_cs;
}

# ----------------------------
sub tp_640 { # 攻城
	&c_up('kou_c') for 1 .. $m{turn};
	&military_master_c_up('kou_c');
#	&use_pet('kou') unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '37'); # 37 ﾍﾟﾃﾝ
	my $v = $m{turn} <= 1 ? 1:
	      	$m{kou_c} > 2000 ? int($m{turn} * 1.4):
		int($m{turn} * (2000 + $m{kou_c}) / 2900);
	$v *= 1.3 if  $cs{mil}[$m{country}] eq $m{name};
	#$v = &seed_bonus('kou', $v);
	$v = int($v);
	#&write_yran('kou', $v, 1) if $v > 0;

	# 城壁データ±
	#require './lib/_rampart.cgi'; # 城壁
	#&change_barrier($y{country}, -$v);

	#&special_money($m{turn} * 500);
	$mes .= "$c_yの城壁を$v%破壊するのに成功しました<br>";
	$m{tp} = 1100;

	&n_menu;
	&write_cs;
}

#=================================================
# 失敗
#=================================================
sub tp_1900 {
	$m{act} += $m{turn};

	# 連続で同じ国だと高確率でﾀｲｰﾎ
	&refresh;
	my $renzoku = $m{unit} eq '18' ? $m{renzoku_c} * 2: $m{renzoku_c};
	if ( (($w{world} eq '11' || ($w{world} eq '19' && $w{world_sub} eq '11')) && $renzoku > rand(4) ) || $renzoku > rand(7) + 2 || ($cs{is_die}[$m{country}] && $renzoku == 1 && rand(9) < 1) || ($cs{is_die}[$m{country}] && $renzoku == 2 && rand(8) < 1)) {
		&write_world_news("$c_mの$m{name}が軍事任務に失敗し$c_yの$cs{prison_name}[$y{country}]に幽閉されました");
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
sub tp_1100 {
	$m{act} += $m{turn};

	my $v = int( (rand(3)+3) * $m{turn} );
	$v = &use_pet('military', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '161');
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
	if ( $w{world} eq $#world_states) {
		require './lib/vs_npc.cgi';
#		if (rand(12) < $npc_mil || ($cs{strong}[$w{country}] < 50000 && rand(4) < $npc_mil) ){ # (1/12) + (1/4) - ( (1/12) * (1/4) ) = 0.3125
#		if (rand(14) < 1 || ($cs{strong}[$w{country}] < 50000 && rand(5) < 1) ) { # (1/14) + (1/5) - ( (1/14) * (1/5) ) = 0.25714285714
#		if (rand(13) < 1 || ($cs{strong}[$w{country}] < 50000 && rand(4) < 1) ) { # (1/13) + (1/4) - ( (1/13) * (1/4) ) = 0.307692308
		if (rand(6) < 1 || ($cs{strong}[$w{country}] < 50000 && rand(3) < 1) ) { # (1/13) + (1/4) - ( (1/13) * (1/4) ) = 0.307692308
		   &npc_military;
		}
	}

	&after_success_action('military');

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

sub military_master_c_up {
	# まず無条件に +1 しそこから4ﾎﾟﾁ毎にさらに +1
	if ($m{master_c} eq $_[0]) { &c_up($_[0]) for 0 .. (int($m{turn} / 4)); }
}

sub special_money {
	return unless $w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1');
	$m{money} += $_[0];
	$mes .= "今までの功績が認められ $_[0] Gの功労金があたえられた<br>";
}

1; # 削除不可
