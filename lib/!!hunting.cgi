require "$datadir/hunting.cgi";
#=================================================
# 討伐 Created by Merino
#=================================================

# ｱｲﾃﾑ拾う確率(分の1)
my $get_item_par = 200;

my $new_sedai = 5;

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "討伐するのに$e2j{hp}が少なすぎます<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	$m{turn} = 0;
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= '魔物を討伐しに行きます<br>';
	$mes .= 'どこに向かいますか?<br>';

	my $m_st = &m_st;
	my @menus = ('やめる');
	for my $i (0..$#places) {
		next if $i == 0 && $m{sedai} > $new_sedai;
		push @menus, "$places[$i][2]" if $m_st * 2 >= $places[$i][1] || $pets[$m{pet}][2] eq 'hunt_lv';
	}

	&menu(@menus);
}
sub tp_1 {
	if ($cmd) {
		$m{stock} = $cmd-1;
		&_get_hunt_you_data;
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
	}
}

#=================================================
# Get 相手データ
#=================================================
sub _get_hunt_you_data {
	my $line = '';
	open my $fh, "< $logdir/monster/$m{stock}.cgi" or &error("$logdir/monster/$m{stock}.cgiﾌｧｲﾙがありません");
	rand($.) < 1 and $line = $_ while <$fh>;
	close $fh;

	my @datas = split /<>/, $line;
	my $i = 0;
	for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon/) {
		$y{$k} = $datas[$i];
		++$i;
	}
	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};
	$y{icon} = $default_icon unless -f "$icondir/$y{icon}";

	if ( rand($m{cha}) < rand($y{cha}) ) {
		$m{tp} = 200;
		$mes .= "$y{name} が襲いかかってきました<br>";
		&n_menu;
	}
	else {
		$m{tp} = 100;
		$mes .= "$y{name} がいます<br>";
		&menu('戦う','逃げる');
	}
}

#=================================================
# 戦う or 逃げる
#=================================================
sub tp_100 {
	if ($cmd eq '0') {
		$mes .= "$y{name} と戦います<br>";
		$m{tp} = 200;
		&n_menu;
	}
	elsif ( rand($m{ag}) > rand($y{ag}) ) {
		$mes .= '逃げました<br>';
		&begin;
	}
	else {
		$mes .= '逃げられませんでした。戦闘態勢に入ります<br>';
		$m{tp} = 200;
		&n_menu;
	}
}

#=================================================
# 戦闘
#=================================================
sub tp_200 {
	require './lib/battle.cgi';

	# 負け
	if ($m{hp} <= 0) {
		$m{act} += 12;
		&refresh;
		&n_menu;
	}
	# 勝ち
	elsif ($y{hp} <= 0) {
		# ﾄｰﾀﾙｽﾃｰﾀｽが自分より弱者だと経験値少なめ
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = $st_lv eq '2' ? int( rand(10) + 10)
			  : $st_lv eq '0' ? int( rand(3)  + 1)
			  :                 int( rand(5)  + 5)
			  ;
		$v = int( rand(10) + 10) if $m{stock} == 0;
		my $vv = int( ($m{stock}+1) * 70 + $y_st * 0.1);

		&c_up('tou_c');
		$v  = &use_pet('hunting', $v);
		$vv = &use_pet('hunt_money', $vv);
		$m{exp} += $v;
		$m{act} += 6;
		$m{egg_c} += int(rand($m{stock})+1+$m{stock}) if $m{egg};
		$m{money} += $vv;
		$mes .= "$v の$e2j{exp}と $vv Gを手に入れました<br>";

		# ｱｲﾃﾑｹﾞｯﾄ(特殊ﾍﾟｯﾄ職業だと取得率up)
		$get_item_par *= 0.4 if $pets[$m{pet}][2] eq 'get_item' || $jobs[$m{job}][1] eq '遊び人';
		&_get_item if int(rand($get_item_par)) == 0;

		$mes .= '討伐を続けますか?<br>';
		&menu('続ける','やめる');
		$m{tp} += 10;
	}
}

#=================================================
# 継続 or やめる
#=================================================
sub tp_210 {
	if ($cmd eq '0') {
		&_get_hunt_you_data;
	}
	else {
		$mes .= '討伐を終了します<br>';
		&refresh;
		&n_menu;
	}
}

#=================================================
# ｱｲﾃﾑ(ﾀﾏｺﾞ)拾う処理
#=================================================
sub _get_item {
	my @egg_nos = @{ $places[$m{stock}][3] };
	my $egg_no = $egg_nos[int(rand(@egg_nos))];

	$mes .= qq|<font color="#FFCC00">$eggs[$egg_no][1]を拾いました!</font><br>|;
	if ($m{is_full}) {
		$mes .= "しかし、預かり所がいっぱいなので$eggs[$egg_no][1]をあきらめました<br>";
	}
	else {
		$mes .="$eggs[$egg_no][1]を預かり所に送りました!<br>";
		&send_item($m{name}, 2, $egg_no);
	}
}



1; # 削除不可
