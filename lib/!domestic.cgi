#=================================================
# 内政 Created by Merino
#=================================================

# 税率：下の70の数字を増やすと難易度が簡単に、減らすと難易度が難しくなるよ
sub tax { ($cs{tax}[$m{country}] + 70) * 0.01 };

# 小規模の時間
my $GWT_s = int($GWT * 0.6);

# 大規模の時間
my $GWT_b = int($GWT * 2);


#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		if ($m{act} >= 100) {
			$mes .= "休息をとります<br>次に行動できるのは $GWT分後です";
			$m{act} = 0;
			&refresh;
			&wait;
			return 0;
		}
		else {
			$mes .= '国に属してないと行うことができません<br>';
			&refresh;
			&n_menu;
			return 0;
		}
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
		$mes .= '内政を行い自国の資源を増やします<br>どれを行いますか?<br>';
	}
	
	&menu('やめる','農業','商業','徴兵','長期内政');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	if    ($cmd eq '1') { $mes .= "穀物を採取して国の$e2j{food}を増やします<br>"; }
	elsif ($cmd eq '2') { $mes .= "国民からお金を徴税をして$e2j{money}を増やします<br>"; }
	elsif ($cmd eq '3') { $mes .= "兵士を募集して国の$e2j{soldier}を増やします<br>※1人につき1G<br>"; }
	elsif ($cmd eq '4') { $mes .= "農業,商業,徴兵をまとめて行います<br>"; $GWT_s *= 3; $GWT_b *= 3; $GWT *= 3; }

	$m{tp} = $cmd * 100;
	$mes .= 'どのくらい行いますか?<br>';
	
	&menu('やめる', "小規模($GWT_s分)", "中規模($GWT分)", "大規模($GWT_b分)");
}

#=================================================
# 内政
#=================================================
sub tp_100 { &exe1('穀物を採取します<br>') }
sub tp_200 { &exe1('お金を徴税します<br>') }
sub tp_300 { &exe1('兵士を雇用します<br>') }
sub exe1 {
	return if &is_ng_cmd(1..3);
	$GWT = $cmd eq '1' ? $GWT_s
		 : $cmd eq '3' ? $GWT_b
		 :               $GWT
		 ;
	
	$m{tp} += 10;
	$m{turn} = $cmd;
	$mes .= "$_[0]結果は$GWT分後<br>";
	&wait;
}
#=================================================
# 長期内政
#=================================================
sub tp_400 {
	return if &is_ng_cmd(1..3);

	$GWT = $cmd eq '1' ? $GWT_s * 3
		 : $cmd eq '3' ? $GWT_b * 3
		 :               $GWT   * 3
		 ;
	
	if ($m{nou_c} >= 5 && $m{sho_c} >= 5 && $m{hei_c} >= 5) {
		$m{tp} += 10;
		$m{turn} = $cmd;
		$mes .= "$_[0]結果は$GWT分後<br>";
		&wait;
	}
	else {
		$mes .= "長期内政を行うには、農業,商業,徴兵の熟練度が5回以上でないとできません<br>";
		&begin;
	}
}


#=================================================
# 農業結果
#=================================================
sub tp_110 {
	my $v = ($m{nou_c} + $m{mat}) * $m{turn} * 10;
	$v  = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '1') {
		$v *= 1.5; # 豊作
	}
	elsif ($cs{state}[$m{country}] eq '3') {
		$v *= 0.5; # 暴風
	}
	$v = &use_pet('nou', $v);
	$v = int($v);
	
	$cs{food}[$m{country}] += $v;
	$mes .= "穀物を $v 採取しました<br>";
	
	&c_up('nou_c') for (1..$m{turn});
	
	return if $m{tp} eq '410';
	&after1;
}
#=================================================
# 商業結果
#=================================================
sub tp_210 {
	my $v = ($m{sho_c} + $m{cha}) * $m{turn} * 10;
	$v = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '2') {
		$v *= 1.5; # 景気
	}
	elsif ($cs{state}[$m{country}] eq '4') {
		$v *= 0.5; # 不況
	}
	$v = &use_pet('sho', $v);
	$v = int($v);

	$cs{money}[$m{country}] += $v;
	$mes .= "お金を $v 徴税しました<br>";

	&c_up('sho_c') for (1..$m{turn});

	return if $m{tp} eq '410';
	&after1;
}
#=================================================
# 徴兵結果
#=================================================
sub tp_310 {
	my $v = ($m{hei_c} + $m{cha}) * $m{turn} * 10;
	$v = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '5') {
		$v *= 0.5; # 飢饉
	}
	$v = &use_pet('hei', $v);
	$v = int($v);

	$v = $m{money} if $v > $m{money};
	$v = 0 if 0 > $m{money};
	$m{money} -= $v;

	$cs{soldier}[$m{country}] += $v;
	$mes .= "兵士を $v 人雇用しました<br>";

	&c_up('hei_c') for (1..$m{turn});

	return if $m{tp} eq '410';
	
	# 徴兵はお金がかかるので、経験値と評価をちょっとﾌﾟﾗｽ
	$m{turn} += 2;
	&after1;
}
#=================================================
# 長期内政結果
#=================================================
sub tp_410 {
	&tp_110;
	&tp_210;
	&tp_310;
	$m{turn} *= 4;
	&after1;
}

#=================================================
# 終了処理
#=================================================
sub after1 {
	my $v = int( (rand(3)+4) * $m{turn} );
	$v = &use_pet('domestic', $v);
	$m{exp} += $v;
	$m{rank_exp} += int( (rand($m{turn}) + $m{turn}) * 2);
	$m{egg_c} += int(rand(3)+3) if $m{egg};
	
	$mes .= "$m{name}に対する評価が上がりました<br>";
	$mes .= "$v の$e2j{exp}を手に入れました<br>";

	# 疲労回復
	$m{act} = 0;
	$mes .= '疲労が回復しました<br>';
	
	&special_money if $w{world} eq '1';

	&daihyo_c_up('dom_c'); # 代表熟練度
	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# 功労金
#=================================================
sub special_money {
	my $v = int($m{rank} * 150 * $m{turn});
	$m{money} += $v;
	$mes .= "今までの功績が認められ $v Gの功労金があたえられた<br>";
}





1; # 削除不可
