$mes .= qq|宝ｸｼﾞ【$m{lot}】<br>| if $is_mobile && $m{lot};
#================================================
# 宝くじ Created by Merino
#================================================

# 宝くじの値段
my $need_money = 1000;

# 何日おきに当選発表するか(日)
my $lot_cycle_day = 7;

# 武器賞の賞品
my @wea_nos = (5,10,15,20,25,31,32);

# ﾀﾏｺﾞ賞の賞品
my @egg_nos = (35..41);


#================================================
# 利用条件
#================================================
sub is_satisfy {
	if ($w{player} < 30) { # ﾌﾟﾚｲﾔｰが30人未満
		$mes .= '準備中だよ<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	open my $fh, "+< $logdir/lot.cgi" or &error('宝くじﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $line = <$fh>;
	my($lot_next_time, $round, $atari1,$no1, $atari2,$no2, $atari3,$no3) = split /<>/, $line;
	$round++;
	$round  = $round > 9 ? 1 : $round;
	
	# 当選発表時間
	if ($time > $lot_next_time) {
		# 宝くじの景品設定
		$no1 = $wea_nos[int(rand(@wea_nos))];
		$no2 = $egg_nos[int(rand(@egg_nos))];
		$no3 = int(rand(21)+20) * 10000;
		
		$lot_next_time = int($time + 24 * 3600 * $lot_cycle_day);
		$atari1 = $round . sprintf("%03d", int(rand($w{player})) );
		$atari2 = $round . sprintf("%03d", int(rand($w{player})) );
		$atari3 = $round . sprintf("%03d", int(rand($w{player})) );
		$atari2 += 1 if $atari1 eq $atari2;
		$atari3 += 3 if $atari3 eq $atari1 || $atari3 eq $atari2;
		
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh "$lot_next_time<>$round<>$atari1<>$no1<>$atari2<>$no2<>$atari3<>$no3<>";
		close $fh;
		
		&write_send_news(qq|<font color="#FFCC00">【宝くじ当選発表\】<br>武器賞【$atari1】$weas[$no1][1]<br>ﾀﾏｺﾞ賞【$atari2】$eggs[$no2][1]<br>金貨賞【$atari3】$no3 G</font>|);
	}
	close $fh;
	
	# 当選者が来たよ賞品を送るよ
	if ($atari1 eq $m{lot}) {
		$mes .= "おお!当選おめでと!賞品の $weas[$no1][1] は預かり所に送っておいたよ<br>";
		&send_item($m{name}, 1, $no1, $weas[$no1][4], 10);
		$m{lot} = '';
	}
	elsif ($atari2 eq $m{lot}) {
		$mes .= "おお!当選おめでと!賞品の $eggs[$no2][1] は預かり所に送っておいたよ<br>";
		&send_item($m{name}, 2, $no2);
		$m{lot} = '';
	}
	elsif ($atari3 eq $m{lot}) {
		$mes .= "おお!当選おめでと!賞品の $no3 Gは送金しておいたよ<br>";
		&send_money($m{name}, '宝くじ屋', $no3);
		$m{lot} = '';
	}
	
	my($lmin,$lhour,$lday,$lmonth) = ( localtime($lot_next_time) )[1..4];
	++$lmonth;
	
	my $round_old = $round == 1 ? 9 : $round -1;
	$mes .= qq|<font color="#FFCC00">【第$round_old回の当選番号】<br>武器賞【$atari1：$weas[$no1][1]】<br>ﾀﾏｺﾞ賞【$atari2：$eggs[$no2][1]】<br>金貨賞【$atari3：$no3 G】<br></font>|;
	$mes .= "宝くじは１枚 $need_money Gだよ<br>";
	$mes .= "第$round回の当選発表\は $lmonth月$lday日$lhour時$lmin分頃だよ<br>";
	$mes .= '新しいのを買う場合は、今持っているくじを引き取るよ<br>' if $m{lot};
	
	&menu('やめる', '買う');
}

sub tp_1 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $need_money) {
		open my $fh, "< $logdir/lot.cgi" or &error('宝くじﾌｧｲﾙが読み込めません');
		my $line = <$fh>;
		close $fh;
		my($lot_next_time, $round) = (split /<>/, $line)[0..1];
		++$round;
		$round  = $round > 9 ? 1 : $round;
		
		my($lmin,$lhour,$lday,$lmonth) = ( localtime($lot_next_time) )[1..4];
		++$lmonth;
		
		$m{lot} = $round . sprintf("%03d", int(rand($w{player})) );
		$m{money} -= $need_money;
		
		$mes .= "まいど!<br>当選発表\は $lmonth月$lday日$lhour時$lmin分頃だよ<br>";
	}
	else {
		$mes .= "お金がなければ夢も買えやしないよ<br>";
	}
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}


1; # 削除不可
