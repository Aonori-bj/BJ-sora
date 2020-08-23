my $this_file = "$logdir/junk_shop.cgi";
#================================================
# ｼﾞｬﾝｸｼｮｯﾌﾟ Created by Merino
#=================================================

# 何もないときの売物(武器)
my @wea_nos = (1,6,11,16,21,26);

# ｶﾞﾁｬｶﾞﾁｬﾀﾞﾏｺﾞ
my @gacha_eggs = (
	# 値段,		ﾀﾏｺﾞNo
	[5000,	[42,42,43,43,43,43,51,51,51,1,4],		],
	[20000,	[42,42,42,42,42,43,43,1,4..15,33,50],	],
	[50000,	[42,43,1,3..24,33,33,33,50],			],
);

# ｶﾞﾁｬｶﾞﾁｬﾀﾏｺﾞができる間隔(秒)
my $gacha_time = 24 * 60 * 60;

# 買う値段
my $buy_price  = 500;

# 売る値段
my $sall_price = 100;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何する?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ｼﾞｬﾝｸｼｮｯﾌﾟでなんでも買えなんでも売る<br>';
		$mes .= 'お前何する?<br>';
	}
	
	&menu('やめる','買う','売る', 'ｶﾞﾁｬﾀﾏ');
}

sub tp_1 {
	return if &is_ng_cmd(1..3);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '1') {
		$mes .= "欲しいのあたか?<br>そこら辺のもの $buy_price Gでいける<br>";
		&menu('やめる','買う');
	}
	elsif ($cmd eq '2') {
		$mes .= "何を売てくれる $sall_price Gで買い取る<br>";
		my @menus = ('やめる');
		push @menus, $m{wea} ? $weas[$m{wea}][1] : '';
		push @menus, $m{egg} ? $eggs[$m{egg}][1] : '';
		push @menus, $m{pet} ? $pets[$m{pet}][1] : '';
		&menu(@menus);
	}
	elsif ($cmd eq '3') {
		$mes .= '運だましのｶﾞﾁｬｶﾞﾁｬﾀﾏｺﾞ。値段色々。何が出るかはお楽しめ<br>';
		my @menus = ('やめる');
		for my $i (0..$#gacha_eggs) {
			push @menus, "$gacha_eggs[$i][0] G";
		}
		&menu(@menus);
	}
	else {
		&begin;
	}
}

#=================================================
# 買う
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	
	if ($m{money} < $buy_price) {
		$mes .= 'お前貧乏。売れない。貧乏暇なし働け<br>';
	}
	elsif ($m{is_full}) {
		$mes .= 'お前の預かり所いぱい。売れない<br>';
	}
	else {
		$m{money} -= $buy_price;

		if (-s $this_file) {
			my $count = 0;
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_file ﾌｧｲﾙが開けません");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				push @lines, $line;
				last if ++$count > 50;
			}
			my $get_line = int(rand(2)) == 0 ? shift @lines : pop @lines;
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
			
			my($kind, $item_no, $item_c) = split /<>/, $get_line;
			
			&send_item($m{name}, $kind, $item_no, $item_c);
			$mes .= $kind eq '1' ? $weas[$item_no][1]
				  : $kind eq '2' ? $eggs[$item_no][1]
				  :				   $pets[$item_no][1]
				  ;
			$mes .= 'を買いました<br>';
			
		}
		# 何もない場合はデフォルトアイテム
		else {
			my $wea_no = $wea_nos[int(rand(@wea_nos))];
			&send_item($m{name}, 1, $wea_no, $weas[$wea_no][4]);
			$mes .= "$weas[$wea_no][1]を買いました<br>";
		}
		$mes .= "お前いい奴、友達。買た物は預かり所に送たよ<br>";
	}
	&begin;
}

#=================================================
# 売る
#=================================================
sub tp_200 {
	if (    ($cmd eq '1' && $m{wea})
		 || ($cmd eq '2' && $m{egg})
		 || ($cmd eq '3' && $m{pet}) ) {
		 
			if ($cmd eq '1') {
				$mes .= "$weas[$m{wea}][1]を売りました<br>";
				$line = "$cmd<>$m{wea}<>$m{wea_c}<>\n";
				$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
			}
			elsif ($cmd eq '2') {
				$mes .= "$eggs[$m{egg}][1]を売りました<br>";
				$line = "$cmd<>$m{egg}<>$m{egg_c}<>\n";
				$m{egg} = $m{egg_c} = 0;
			}
			elsif ($cmd eq '3') {
				$mes .= "$pets[$m{pet}][1]を売りました<br>";
				$line = "$cmd<>$m{pet}<>0<>\n";
				$m{pet} = 0;
			}
			else {
				&error('ｱｲﾃﾑの種類が異常です');
			}
			
			$mes .= "お前いい人、仲良し。良いもの持てる $sall_money Gやる<br>";
			$m{money} += $sall_price;
			
			open my $fh, ">> $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
			print $fh $line;
			close $fh;
	}
	&begin;
}

#=================================================
# ｶﾞﾁｬﾀﾏ
#=================================================
sub tp_300 {
	return if &is_ng_cmd(1..$#gacha_eggs+1);
	--$cmd;
	
	if ($m{gacha_time} + $gacha_time > $time) {
		my $g_time = $m{gacha_time} + $gacha_time - $time;
		my $next_gacha_time = sprintf("%02d時%02d分", int($g_time / 3600), int($g_time % 3600 / 60) );
		$mes .= "ｶﾞﾁｬｶﾞﾁｬやり過ぎるとお前壊れる。あと $next_gacha_time くらい待て<br>";
	}
	elsif ($m{money} >= $gacha_eggs[$cmd][0]) {
		my @egg_nos = @{ $gacha_eggs[$cmd][1] };
		my $egg_no  = $egg_nos[int(rand(@egg_nos))];
		$m{money}  -= $gacha_eggs[$cmd][0];
		
		&send_item($m{name}, 2, $egg_no,);
		$mes .= "ｶﾞﾁｬｶﾞﾁｬ♪ﾋﾟｰ♪<br>$eggs[$egg_no][1]が出ました<br>";
		
		$m{gacha_time} = $time;
	}
	else {
		$mes .= 'お前貧乏。ｶﾞﾁｬｶﾞﾁｬﾀﾞﾒ。貧乏暇なし働け<br>';
	}

	&begin;
}


1; # 削除不可
