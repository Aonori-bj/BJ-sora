#================================================
# 商人のお店 Created by Merino
#================================================

#================================================
# お店の名前一覧表示
#================================================
sub begin {
	$layout = 2;
	
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "どのお店で買物しますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>店名</th><th>店長</th><th>紹介文<br></th></tr>| unless $is_mobile;

	open my $fh, "< $logdir/shop_list.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが読み込めません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		# 商品がない店は非表示
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";
		
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="お店に入る" class="button1"></p></form>|;
}

#================================================
# お店の商品一覧表示
#================================================
sub tp_1 {
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list.cgi" or &error('ｼｮｯﾌﾟﾘｽﾄﾌｧｲﾙが開けません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		if ($y{name} eq $name) {
			$is_find = 1;
			$m{stock} = $shop_name;
			$shop_message = $message;
			last;
		}
	}
	close $fh;
	
	# お店が存在しない
	if (!$is_find || !-f "$userdir/$shop_id/shop.cgi") {
		$mes .= "$m{stock}というお店は閉店してしまったようです<br>";
		&begin;
	}
	# 自分のお店で買い物できてしまうと、売上ﾗﾝｷﾝｸﾞが崩壊してしまうので。
	elsif ($m{name} eq $y{name}) {
		$mes .= "自分のお店で買い物することはできません<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop.cgi") {
		$mes .= qq|【$m{stock}】$y{name}「$shop_message」<br>|;
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;
		$mes .= qq|<table class="table1"><tr><th>商品名</th><th>値段<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop.cgi" or &error("$y{name}に入れません");
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			$mes .= qq|<tr><td><input type="radio" name="cmd" value="$no">|;
			$mes .= $kind eq '1' ? "$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])"
				  : $kind eq '2' ? "$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
				  : 			   "$pets[$item_no][1]"
				  ;
			$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
		}
		close $fh;
		
		$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="買う" class="button1"></p></form>|;
		$m{tp} = 100;
	}
	else {
#		$mes .= "【$cmd】準備中<br>";
		&begin;
	}
}

#================================================
# 買い物処理
#================================================
sub tp_100 {
	my $shop_id = unpack 'H*', $y{name};
	if ($cmd && -f "$userdir/$shop_id/shop.cgi") {
		my $is_find    = 0;
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $userdir/$shop_id/shop.cgi" or &error("商品ﾘｽﾄが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			
			if ($cmd eq $no) {
				$is_find = 1;

				if ($m{money} >= $price) {
					$m{money} -= $price;
					
					my $item_name = $kind eq '1' ? $weas[$item_no][1]
								  : $kind eq '2' ? $eggs[$item_no][1]
								  :				   $pets[$item_no][1]
								  ;
					$mes .= "$item_nameを買いました<br>$item_nameは預かり所に送られました<br>";
					
					&send_item($m{name}, $kind, $item_no, $item_c, $item_lv);
					&send_money($y{name}, "【$m{stock}($item_name)】$m{name}", $price, 1);
					$is_rewrite = 1;
					
					# 売上金加算
					open my $fh2, "+< $userdir/$shop_id/shop_sale.cgi" or &error("売上ﾌｧｲﾙが開けません");
					eval { flock $fh2, 2; };
					my $line2 = <$fh2>;
					my($sale_c, $sale_money) = split /<>/, $line2;
					$sale_c++;
					$sale_money += $price;
					seek  $fh2, 0, 0;
					truncate $fh2, 0;
					print $fh2 "$sale_c<>$sale_money<>";
					close $fh2;
				}
				else {
					$mes .= "$y{name}「お金が足りません」<br>";
					last;
				}
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
		
		unless ($is_find) {
			$mes .= "$y{name}「その商品は、たった今売り切れてしまいました」<br>" ;
		}
		$cmd = $y{name}; # 名前をcmdに入れて&tp_1
		&tp_1;
	}
	else {
		$mes .= 'やめました<br>';
		&begin
	}
}


1; # 削除不可
