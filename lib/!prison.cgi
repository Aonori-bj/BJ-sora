sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
#=================================================
# 牢獄 Created by Merino
#=================================================

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{act} >= 100) {
		$mes .= "$m{name}は少し休息をとることにした<br>次に行動できるのは $GWT分後です";
		$m{act} = 0;
		&wait;
		return 0;
	}
	return 1;
}

#=================================================
# 牢獄ﾒﾆｭｰ
#=================================================
sub tp_100 {
	if (-f "$userdir/$id/rescue_flag.cgi" # ﾚｽｷｭｰﾌﾗｸﾞがあるか
		|| $time < $w{reset_time} # 終戦中
		|| !defined $cs{name}[$y{country}]) { # 国削除

			unlink "$userdir/$id/rescue_flag.cgi" or &error("$userdir/$id/rescue_flag.cgi削除失敗") if -f "$userdir/$id/rescue_flag.cgi";
			$mes .= "仲間に救出されました<br>";
			
			&refresh;
			&n_menu;
			&escape;
	}
	else {
		$mes .= "$m{name}は$c_yの牢獄に閉じ込められました<br>";
		$mes .= 'どうしますか?<br>';
		&menu('助けを待つ','脱走を試みる','寝返る');
		$m{tp} += 10;
	}
}

sub tp_110 {
	# 脱出
	if ($cmd eq '1') {
		$mes .= "$m{name}は脱走ができそうか色々と試してみた<br>";
		if ( int(rand(4)) == 0 ) { # 成功
			$mes .= 'なんとか牢獄から脱出することに成功した!<br>';
			$m{tp} += 10;
		}
		elsif ( $m{cha} > rand(1000)+400 ) {
			$mes .= '看守を誘惑して牢獄から脱出することに成功した!<br>';
			$m{tp} += 10;
		}
		else {
			$mes .= 'どうやら無理なようだ…<br>';
			$m{act} += 10;
			$m{tp} = 100;
		}
		&n_menu;
	}
	# 寝返る
	elsif ($cmd eq '2') {
		$mes .= "寝返ると階級と代表\者ﾎﾟｲﾝﾄが下がり、手続きに$GWT分かかります<br>";
		$mes .= "$c_m を裏切り、$c_yに寝返りますか?<br>";
		&menu('やめる','寝返る');
		$m{tp} = 200;
	}
	else {
		$m{tp} = 100;
		&tp_100;
	}
}

#=================================================
# 牢獄脱出
#=================================================
sub tp_120 {
	$m{tp} += 10;
	$m{value} = int(rand(40))+40;
	$m{turn}  = int(rand(4)+4);
	$mes .= "牢獄から脱出しました! <br>";
	$mes .= "$c_y脱出まで残り【$m{turn}ﾀｰﾝ】敵兵の気配【$m{value}%】<br>";
	$mes .= 'どちらに進みますか?<br>';
	&menu('左','右');
	$m{value} += int( 10 - rand(21) ); # ±10
	$m{value} = int(rand(30)) if $m{value} < 10;
}

#=================================================
# ﾙｰﾌﾟﾒﾆｭｰ 捕まるか脱出するまで
#=================================================
sub loop_menu {
	$mes .= "$c_y脱出まで残り【$m{turn}ﾀｰﾝ】敵兵の気配【$m{value}%】<br>";
	$mes .= 'どちらに進みますか?<br>';
	int(rand(3)) == 0 ? &menu('左','右') : &menu('左','直進','右');
}
sub tp_130 {
	# 見つかる
	if ( $m{value} > rand(110)+30 ) {
		$mes .= '敵兵に見つかってしまった!!<br>';
		$m{tp} += 10;
		&n_menu;
	}
	# 脱出成功
	elsif (--$m{turn} <= 0) {
		&mes_and_world_news("無事に$c_yからの自力脱出に成功しました!");
		&refresh;
		&n_menu;
		&escape;
	}
	else {
		&loop_menu;
	}
	$m{value} += int( 10 - rand(21) ); # ±10
	$m{value} = int(rand(30)) if $m{value} < 10;
}
# 見つかった時:逃げ切れる or 捕まる
sub tp_140 {
	if ( rand(6) < 1 ) {
		$mes .= 'なんとか敵兵を振り切りました<br>';
		$m{tp} -= 10;
		&loop_menu;
	}
	else {
		$mes .= '敵兵に囲まれ牢獄へと連れ戻されました<br>';
		$m{tp} = 100;
		$m{act} += 20;
		&n_menu;
	}
}


#=================================================
# 寝返る
#=================================================
sub tp_200 {
	if ($cmd eq '1') {
		if ($cs{ceo}[$m{country}] eq $m{name}) {
			$mes .= "$e2j{ceo}は寝返ることができません<br>";
			$m{tp} = 100;
			&n_menu;
		}
#		if ($m{name} eq $m{vote} || &is_daihyo) {
#			$mes .= "国の代表\者や$e2j{ceo}に立候補している場合は寝返ることができません<br>";
#			$m{tp} = 100;
#			&n_menu;
#		}
		elsif ($m{shogo} eq $shogos[1][0]) {
			$mes .= "$shogos[1][0]は寝返ることができません<br>";
			$m{tp} = 100;
			&n_menu;
		}
		elsif ($cs{member}[$y{country}] >= $cs{capacity}[$y{country}]) {
			$mes .= "$c_yは定員がいっぱいです<br>";
			$m{tp} = 100;
			&n_menu;
		}
		else {
			require './lib/move_player.cgi';
			&move_player($m{name}, $m{country}, $y{country});
			&escape;
			
			$m{shogo} = $shogos[1][0];

			$m{rank} -= $m{rank} > 10 ? 2 : 1;
			$m{rank} = 1 if $m{rank} < 1;
			$mes .= "階級が$ranks[$m{rank}]になりました<br>";

			&mes_and_world_news("$cs{name}[$y{country}]に寝返りました", 1);
			$m{country} = $y{country};
			$m{vote} = '';
			
			# 代表ﾎﾟｲﾝﾄDown
			for my $key (qw/war dom mil pro/) {
				$m{$key.'_c'} = int($m{$key.'_c'} * 0.4);
			}

			&refresh;
			&wait;
			&n_menu;
		}
	}
	else {
		$mes .= 'やめました<br>';
		$m{tp} = 100;
		&n_menu;
	}
}

#=================================================
# 牢獄ﾌｧｲﾙから自分の名前を除く
#=================================================
sub escape {
	my @lines = ();
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi が開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country) = split /<>/, $line;
		push @lines, $line unless $name eq $m{name};
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # 削除不可
