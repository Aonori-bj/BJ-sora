my $this_file = "$logdir/auction.cgi";
#=================================================
# ｵｰｸｼｮﾝ Created by Merino
#=================================================

# 落札時間(日)
my $limit_day = 3;

# 最大出品数
my $max_auction = 30;

# 出品禁止ｱｲﾃﾑ
my %taboo_items = (
	wea => [1,6,11,16,21,26], # 武器
	egg => [], # ﾀﾏｺﾞ
	pet => [], # ﾍﾟｯﾄ
);


#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]の方はお断りしています<br>";
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かしますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ｵｰｸｼｮﾝ会場に来ました<br>何をしますか?<br>';
	}
	&menu('やめる','入札する','出品する');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#=================================================
# 入札
#=================================================
sub tp_100 {
	$layout = 1;
	
	$mes .= qq|ｵｰｸｼｮﾝの落札日数は、出品日から $limit_day日前後です<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
 	$mes .= $is_mobile ? qq|<hr>落札品/落札額/落札者/出品者<br>|
 		: qq|<table class="table1" cellpadding="3"><tr><th>落札品</th><th>落札額</th><th>落札者</th><th>出品者<br></th>|;

	open my $fh, "< $this_file" or &error("$this_fileが読み込めません");
	while (my $line = <$fh>) {
		my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price) = split /<>/, $line;
		my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])"
					   : $kind eq '2' ? "[卵]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
					   : "[ペ]$pets[$item_no][1]"
					   ;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$item_title/$item_price G/$to_name/$from_name<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$item_title</td><td align="right">$item_price G</td><td>$to_name</td><td>$from_name<br></td></tr>|;
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<p>入札金額：<input type="text" name="money" value="0" class="text_box1" style="text-align:right" class="text1">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="入札する" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_110 {
	$in{money} = int($in{money});
	if ($m{money} < $in{money}) {
		$mes .= 'そんなにお金を持っていません<br>';
	}
	elsif ($cmd && $in{money} && $in{money} !~ /[^0-9]/) {
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price) = split /<>/, $line;
			if ($no eq $cmd) {
				my $need_money = int($item_price * 1.2);
				if ( $in{money} >= $need_money ) {
					my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])"
								   : $kind eq '2' ? "[卵]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
								   :			    "[ペ]$pets[$item_no][1]"
								   ;
					
					$mes .= "$item_titleに $in{money} Gで入札しました<br>";
					$line = "$bit_time<>$no<>$kind<>$item_no<>$item_c<>$item_lv<>$from_name<>$m{name}<>$in{money}<>\n";
					$is_rewrite = 1;
				}
				else {
					$mes .= "入札は現在の落札額の1.2倍以上の金額( $need_money G)が必要です<br>";
				}
				push @lines, $line;
			}
			# 落札処理
			elsif ($time > $bit_time) {
				my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])"
							   : $kind eq '2' ? "[卵]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
							   :			    "[ペ]$pets[$item_no][1]"
							   ;

				&send_item($to_name, $kind, $item_no, $item_c, $item_lv);
				&send_money($to_name, 'ｵｰｸｼｮﾝ会場', "-$item_price");
				&send_money($from_name, 'ｵｰｸｼｮﾝ会場', $item_price);
				&write_send_news("$from_nameの出品した$item_titleを$to_nameが $item_price Gで落札しました");
				$is_rewrite = 1;
			}
			else {
				push @lines, $line;
			}
		}
		if ($is_rewrite) {
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
		}
		close $fh;
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}

#=================================================
# 出品
#=================================================
sub tp_200 {
	$layout = 1;
	$mes .= 'どれを出品しますか?<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">$weas[$m{wea}][1]★$m{wea_lv}($m{wea_c})<br>| if $m{wea};
	$mes .= qq|<input type="radio" name="cmd" value="2">$eggs[$m{egg}][1]($m{egg_c})<br>| if $m{egg};
	$mes .= qq|<input type="radio" name="cmd" value="3">$pets[$m{pet}][1]<br>| if $m{pet};
	$mes .= qq|<p>初期金額<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="出品する" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..3);
	
	my $is_find = 0;
	my @lines = ();
	open my $fh, "< $this_file" or &error("$this_file が開けませんでした");
	while (my $line = <$fh>) {
		my($name) = (split /<>/, $line)[6];
		if (!$is_find && $m{name} eq $name) {
			$is_find = 1;
		}
		push @lines, $line;
	}
	close $fh;
	
	if ($is_find) {
		$mes .= '出品しているものが落札されるまで、出品することはできません<br>';
	}
	elsif (@lines >= $max_auction) {
		$mes .= '現在、出品の受付はしておりません<br>出品数が減ってから再度申\し込みください<br>';
	}
	elsif ($in{price} =~ /[^0-9]/ || $in{price} >= 999999) {
		$mes .= '値段は 99万9999 G以内にする必要があります<br>';
	}
	elsif ( ($cmd eq '1' && $m{wea})
		 || ($cmd eq '2' && $m{egg})
		 || ($cmd eq '3' && $m{pet}) ) {
			
			my @kinds = ('', 'wea', 'egg', 'pet');
			for my $taboo_item (@{ $taboo_items{ $kinds[$cmd] } }) {
				if ($taboo_item eq $m{ $kinds[$cmd] }) {
					my $t_item_name = $cmd eq '1' ? $weas[$m{wea}][1]
									: $cmd eq '2' ? $eggs[$m{egg}][1]
									:               $pets[$m{pet}][1]
									;
					$mes .= "$t_item_nameは出品禁止ｱｲﾃﾑとなっております<br>";
					&begin;
					return;
				}
			}
			
			my $item_price = $in{price} || 0;
			my $item_no = $m{ $kinds[$cmd]       };
			my $item_c  = $m{ $kinds[$cmd].'_c'  } || 0;
			my $item_lv = $m{ $kinds[$cmd].'_lv' } || 0;
			
			if ($cmd eq '1' && $m{wea}) {
				&mes_and_send_news("$weas[$m{wea}][1]を出品しました");
				$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
			}
			elsif ($cmd eq '2' && $m{egg}) {
				&mes_and_send_news("$eggs[$m{egg}][1]を出品しました");
				$m{egg} = $m{egg_c} = 0;
			}
			elsif ($cmd eq '3' && $m{pet}) {
				&mes_and_send_news("$pets[$m{pet}][1]を出品しました");
				$m{pet} = 0;
			}
			
			my $bit_time = $time + int( $limit_day * 3600 * 24 + rand(3600) ); # 入札時間を１時間程度ばらけさす
			
			my($last_no) = (split /<>/, $lines[-1])[1];
			++$last_no;
			open my $fh2, ">> $this_file" or &error("$this_file が開けませんでした");
			print $fh2 "$bit_time<>$last_no<>$cmd<>$item_no<>$item_c<>$item_lv<>$m{name}<>$m{name}<>$item_price<>\n";
			close $fh2;
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}


1; # 削除不可
