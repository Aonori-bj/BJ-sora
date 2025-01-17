my $this_file = "$logdir/colosseum/champ_$m{stock}.cgi";
#================================================
# 闘技場 Created by Merino
#=================================================
# $m{stock} がﾘｰｸﾞ $m{value} が ﾗｳﾝﾄﾞ数

# この回数以上防衛すると自動引退
my $limit_defence_c = 50;

# 石碑に記録
my $legend_defence_c = 25;

# ﾗｳﾝﾄﾞﾀｲﾄﾙ
my @round_titles = ('初戦','準決勝','決勝戦');

# 司会者のｾﾘﾌ(1+2の組み合わせ)
my @coms_1 = ('なかなかの','大逆転の','ｽﾋﾟｰﾃﾞｨｰな','素晴らしい','見ごたえのある','鬼気迫る','ｷﾞﾘｷﾞﾘの','一方的な','見事な','芸術的な','ｸﾚｲｼﾞｰな','大迫力の','よくわからない');
my @coms_2 = ('試合','勝負','戦い','攻撃','攻防','強さ','技','気迫','ﾍﾀﾚ','動き','一撃');

# ﾘｰｸﾞ(追加した場合『./log/colosseum/』に『champ_?.cgi』ﾌｧｲﾙを追加すること)
my @menus = (
#	[0]名前,[1]強さ制限,[2]防衛金,[3]出場金
	['ﾋﾟﾖﾋﾟﾖﾘｰｸﾞ',	800,	1000,	1000],
	['ﾋﾞｷﾞﾅｰﾘｰｸﾞ',	1500,	1000,	1000],
	['ﾍﾞﾃﾗﾝﾘｰｸﾞ',	3000,	2000,	2000],
	['ﾏｼﾞｼｬﾝﾘｰｸﾞ',	0,		2000,	2000],
	['ｿﾙｼﾞｬｰﾘｰｸﾞ',	0,		2000,	2000],
	['ﾁｬﾝﾋﾟｵﾝﾘｰｸﾞ',	0,		3000,	3000],
);

my %plus_needs = (
	'ﾏｼﾞｼｬﾝﾘｰｸﾞ'	=> ['武器の装備属性が『風、雷、炎』のみ',		sub{ $weas[$m{wea}][2] =~ /風|雷|炎/ }],
	'ｿﾙｼﾞｬｰﾘｰｸﾞ'	=> ['武器の装備属性が『剣、槍、斧』のみ',		sub{ $weas[$m{wea}][2] =~ /剣|槍|斧/ }],
);

#================================================
# 利用条件
#================================================
sub is_satisfy {
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "闘技場に参加するのに$e2j{hp}が少なすぎます<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	$m{tp} = 1 if $m{tp} > 1;
	$m{turn} = 0;
	my $m_st = &m_st;
	$mes .= "$m{name}の強さ[ $m_st ]<br>";
	$mes .= "ここは強者が集まる闘技場です<br>三戦連続で勝ち進むとﾁｬﾝﾋﾟｵﾝになり賞金が出ます<br>";
	$mes .= "ﾁｬﾝﾋﾟｵﾝになり、防衛することでもまた賞金がもらえます<br>";
	$mes .= "<hr>どのﾘｰｸﾞに挑戦しますか?<br>";
	for my $i (0 .. $#menus) {
		$mes .= $menus[$i][1] ? "$menus[$i][0]：強さ$menus[$i][1]まで<br>"
			  : "$menus[$i][0]：強さ無制限<br>";
	}
	
	&menu('やめる',map{ $_->[0] } @menus);
}

sub tp_1 {
	return if &is_ng_cmd(1..$#menus+1);
	
	--$cmd;
	$m{tp} = 100;
	$m{stock} = $cmd;
	$mes .= "$menus[$m{stock}][0] に出場するには、$menus[$m{stock}][3] Gかかります<br>";
	$mes .= "挑戦しますか?<br>";
	
	&champ_statuses($m{stock});
	
	&menu('やめる','挑戦する');
}


#================================================
# 出場ｾｯﾄ
#================================================
sub tp_100 {
	if ($cmd eq '1') {
		if ($menus[$m{stock}][1] <= 0 || &m_st <= $menus[$m{stock}][1]) {
			if (&is_champ) {
				$mes.="$m{name}選手は防衛者ですので挑戦することはできません<br>";
				&begin;
			}
			elsif ($m{money} >= $menus[$m{stock}][3]) {
				if (!defined $plus_needs{$menus[$m{stock}][0]} || &{ $plus_needs{$menus[$m{stock}][0]}[1] }) {
					$m{money} -= $menus[$m{stock}][3];
					$m{tp} = 110;
					$m{value} = 0;
					$mes .= "$menus[$m{stock}][0] に出場します!<br>";
					&n_menu;
				}
				else {
					$mes .= "$menus[$m{stock}][0]に出場できる条件は $plus_needs{$menus[$m{stock}][0]}[0] です<br>";
					&begin;
				}
			}
			else {
				$mes .= 'お金が足りません<br>';
				&begin;
			}
		}
		else {
			$mes .= "$menus[$m{stock}][0]に出場できるのは強さが$menus[$m{stock}][1]以下の選手だけです<br>";
			&begin;
		}
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
	}
}


#================================================
# 優勝 or 試合開始のｱﾅｳﾝｽ
#================================================
sub tp_110 {
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	my @lines = <$fh>;
	close $fh;
	
	# 防衛者数によりﾗｳﾝﾄﾞ数調整
	if ($m{value} <= 0) {
		$m{value} = @lines == 0 ? 3 # 防衛者がいないのでいきなり優勝
				  : @lines == 1 ? 2 # 決勝から
				  : @lines == 1 ? 1 # 準決勝から
				  :               0 # 初戦から
				  ;
	}
	
	if ($m{value} > 2) { # 優勝
		&c_up('col_c') for (1..$m{value});

		--$m{value};
		
		# 防衛者書き換え処理
		&_rewrite_champ;
		
		my $v = $menus[$m{stock}][2] * 10;
		$m{money} += $v;
		$mes.="$menus[$m{stock}][0]に新たな優勝者が誕生しました!<br>";
		$mes.="$m{name}選手です!$m{name}「$m{mes_win}」<br>";
		$mes.="賞金の $v Gが送られます!<br>";
		$mes.="それでは再び$m{name}選手に拍手を!<br>";
		$m{egg_c} += int(rand(20)+30) if $m{egg};
		$m{act} += 10;
		&write_colosseum_news(qq|<i>$menus[$m{stock}][0] 新ﾁｬﾝﾋﾟｵﾝ <font color="$cs{color}[$m{country}]">$m{name}</font> 誕生</i>|, 1);
		&refresh;
		&n_menu;
	}
	else {
		# 相手ﾃﾞｰﾀ取得
		($y{name},$y{country},$y{max_hp},$y{max_mp},$y{at},$y{df},$y{mat},$y{mdf},$y{ag},$y{cha},$y{wea},$y{skills},$y{mes_win},$y{mes_lose},$y{icon},$y{defence_c}) = split /<>/, $lines[$m{value}];
		$y{hp}  = $y{max_hp};
		$y{mp}  = $y{max_mp};
		$y{icon} = $default_icon unless -f "$icondir/$y{icon}";
		
		$mes .= $coms_1[int(rand(@coms_1))].$coms_2[int(rand(@coms_2))]."でしたね!それでは引き続き<br>" if $m{value} > 0;
		$mes .= "$menus[$m{stock}][0] $round_titles[$m{value}]<br>";
		$mes .= "$m{name} VS $y{name}<br>";
		$mes .= "試合始め!<br>";
		&n_menu;
		$m{tp} = 120;
	}
}

#================================================
# 戦闘処理
#================================================
sub tp_120 {
	require './lib/battle.cgi';

	if ($m{hp} <= 0) {
		&col_lose;
	}
	elsif ($y{hp} <= 0) {
		&col_win;
	}
}

#================================================
# 負け
#================================================
sub col_lose {
	$m{act} += $m{value} * 5 + 5;
	$mes .= '残念でした。また挑戦しに来てださい<br>';
	&_defence_c_up;
	&refresh;
	&n_menu;
}
#================================================
# 勝ち
#================================================
sub col_win {
	my $v = int( rand(10)+ 5 );
	$v = &use_pet('colosseum', $v);
	$m{exp} += $v;
	$m{egg_c} += int(rand(2)+1) if $m{egg};

	$mes .= "$vの$e2j{exp}を手に入れました<br>";
	&write_colosseum_news(qq|$menus[$m{stock}][0]$round_titles[$m{value}] ○ 挑戦者<font color="$cs{color}[$m{country}]">$m{name}</font> VS 防衛者<font color="$cs{color}[$y{country}]">$y{name}</font> ×|);
	
	$m{tp} = 110;
	++$m{value}; # ﾗｳﾝﾄﾞｶｳﾝﾄｱｯﾌﾟ
	&n_menu;
}

#================================================
# 防衛数ｶｳﾝﾄｱｯﾌﾟ
#================================================
sub _defence_c_up {
	my $count = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if ($count eq $m{value}) {
			my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c) = split /<>/, $line;
			++$defence_c;
			
			&write_colosseum_news(qq|$menus[$m{stock}][0]$round_titles[$m{value}] × 挑戦者<font color="$cs{color}[$m{country}]">$m{name}</font> VS 防衛者<font color="$cs{color}[$y{country}]">$y{name}</font> ○ 防衛$defence_c|);

			# 規定数以上だと自動引退＆石碑
			if ($defence_c >= $limit_defence_c) {
				&write_legend("champ_$m{stock}", "$cs{name}[$country]の$nameが$menus[$m{stock}][0]で$defence_c回の防衛を果たす", 1, $name);
				&write_colosseum_news(qq|<i><font color="$cs{color}[$country]">$name</font>が$menus[$m{stock}][0]で$defence_c回の防衛を果たし防衛者を引退しました</i>|);

				&_send_money_and_col_c_up($name, $defence_c);
			}
			else {
				push @lines, "$name<>$country<>$max_hp<>$max_mp<>$at<>$df<>$mat<>$mdf<>$ag<>$cha<>$wea<>$skills<>$mes_win<>$mes_lose<>$icon<>$defence_c<>\n";
			}
		}
		else {
			push @lines, $line;
		}
		++$count;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#================================================
# 新ﾁｬﾝﾋﾟｵﾝ誕生。
#================================================
sub _rewrite_champ {
	my $line = '';
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my @lines = <$fh>;
	push @lines, "$m{name}<>$m{country}<>$m{max_hp}<>$m{max_mp}<>$m{at}<>$m{df}<>$m{mat}<>$m{mdf}<>$m{ag}<>$m{cha}<>$m{wea}<>$m{skills}<>$m{mes_win}<>$m{mes_lose}<>$m{icon}<>0<>\n";
	$line = shift @lines if @lines > 3;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if ($line) {
		my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c) = split /<>/, $line;

		# 石碑に書き込み
		if ($defence_c >= $legend_defence_c) {
			&write_legend("champ_$m{stock}", "$cs{name}[$country]の$nameが$menus[$m{stock}][0]で$defence_c回の防衛を果たす", 1, $name);
			&write_colosseum_news(qq|<i><font color="$cs{color}[$country]">$name</font>が$menus[$m{stock}][0]で$defence_c回の防衛を果たし防衛者を引退しました</i>|);
		}
		else {
			&write_colosseum_news(qq|<b><font color="$cs{color}[$country]">$name</font>が$menus[$m{stock}][0]で$defence_c回の防衛を果たし防衛者を引退しました</b>|, 1, $name);
		}
		
		&_send_money_and_col_c_up($name, $defence_c);
	}
}

#================================================
# 引退者にお金送金と闘技場熟練度を上げる
#================================================
sub _send_money_and_col_c_up {
	my($name, $defence_c) = @_;

	my $y_id = unpack 'H*', $name;
	if (-f "$userdir/$y_id/user.cgi") {
		&send_money($name, $menus[$m{stock}][0], $defence_c * $menus[$m{stock}][2]);

		my %datas = &get_you_datas($y_id, 1);
		$datas{col_c} += $defence_c;
		&regist_you_data($name, 'col_c', $datas{col_c});
	}
}


#================================================
# 自分が防衛者かどうか
#================================================
sub is_champ {
	open my $fh, "< $logdir/colosseum/champ_$m{stock}.cgi" or &error("$logdir/colosseum/champ_$m{stock}.cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my $name = (split/<>/,$line)[0];
		return 1 if $name eq $m{name};
	}
	close $fh;
	return 0;
}

#================================================
# 防衛者のステータス表示
#================================================
sub champ_statuses {
	my $champ_stage = shift;
	
	open my $fh, "$logdir/colosseum/champ_$champ_stage.cgi" or &error("$logdir/colosseum/champ_$champ_stage.cgiﾌｧｲﾙが読み込めません");
	my @lines = <$fh>;
	close $fh;
	
	$mes .= "<hr>防衛者<br>";
	my $count = @lines;
	for my $line (@lines) {
		my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c) = split /<>/, $line;
		
		my $round_c = @round_titles - $count;
		$mes .= "$round_titles[$round_c]:$name(防衛$defence_c)/$weas[$wea][1]/$e2j{hp}$max_hp/$e2j{mp}$max_mp/$e2j{at}$at/$e2j{df}$df/$e2j{mat}$mat/$e2j{mdf}$mdf/$e2j{ag}$ag<br>";
		--$count;
	}
}


1; # 削除不可
