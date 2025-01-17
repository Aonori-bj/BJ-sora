my $this_file      = "$userdir/$id/shop.cgi";
my $shop_list_file = "$logdir/shop_list.cgi";
#================================================
# 商人のお店 Created by Merino
#================================================

# 建設費用
my $build_money = 100000;

# お店における最大数
my $max_shop_item = 20;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "他に何かしますか?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "自分の商人のお店の設定をします<br>";
		$mes .= "※$sales_ranking_cycle_day日間お店の売上がないとお店は自動的に閉店になります<br>";
	}
	&menu('やめる','商品閲覧', '店頭に置く', 'お店の紹介', 'お店を建てる');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);

	$m{tp} = $cmd * 100;
	if ($cmd eq '4') {
		if (-f $this_file) {
			$mes .= "すでに自分のお店を持っています<br>";
			&begin;
		}
		elsif ($jobs[$m{job}][1] ne '商人') {
			$mes .= "職業が商人でないとお店を建てることができません<br>";
			&begin;
		}
		else {
			$mes .= "お店を建てるには $build_money Gかかります<br>";
			$mes .= "※商人のお店ﾗﾝｷﾝｸﾞの更新が近い時に建てるとすぐに閉店してしまいます<br>";
			&menu('やめる','建てる');
		}
	}
	elsif (!-f $this_file) {
		$mes .= 'まずは、お店を建てる必要があります<br>';
		&begin;
	}
	else {
		&{ 'tp_'. $m{tp} };
	}
}

#=================================================
# 建設
#=================================================
sub tp_400 {
	if ($cmd eq '1') {
		if (-f $this_file) {
			$mes .= "すでに自分のお店を持っています<br>";
		}
		elsif ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error('お店を建てるのに失敗しました');
			close $fh;
			chmod $chmod, "$this_file";

			open my $fh2, "> $userdir/$id/shop_sale.cgi" or &error('ｾｰﾙｽﾌｧｲﾙが開けません');
			print $fh2 "0<>0<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale.cgi";

			open my $fh3, ">> $shop_list_file" or &error('お店ﾘｽﾄﾌｧｲﾙが開けません');
			print $fh3 "$m{name}店<>$m{name}<>$date開店<>0<>0<>\n";
			close $fh3;

			&mes_and_send_news("<b>商人のお店を建てました</b>", 1);
			$mes .= '<br>さっそくお店に商品を並べましょう<br>';
			$m{money} -= $build_money;
		}
		else {
			$mes .= 'お金が足りません<br>';
		}
	}
	&begin;
}

#=================================================
# 商品閲覧
#=================================================
sub tp_100 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $last_time = (stat "$userdir/$id/shop_sale.cgi")[9];
	my($min,$hour,$mday,$month) = (localtime($last_time))[1..4];
	++$month;
	open my $fh2, "< $userdir/$id/shop_sale.cgi" or &error("お店ﾌｧｲﾙが読み込めません");
	my $line = <$fh2>;
	close $fh2;
	my($sale_c, $sale_money) = split /<>/, $line;
	$mes .= "最終売上日時：$month/$mday $hour:$min<br>";
	$mes .= "現在の売上げ：$sale_c個 $sale_money G<br>";

	$mes .= '<hr>預かり所に戻しますか?<br>';
	$mes .= 'お店の商品一覧<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>やめる<br>|;
	$mes .= qq|<table class="table1"><tr><th>商品名</th><th>値段</th></tr>|;

	open my $fh, "< $this_file" or &error("$this_file が読み込めません");
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
	$mes .= qq|<p><input type="submit" value="預かり所に戻す" class="button1"></p></form>|;

	$m{tp} = 110;
}
sub tp_110 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	if ($cmd) {
		if ($m{is_full}) {
			$mes .= '預かり所がいっぱいです<br>';
			&begin;
		}
		else {
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_fileが開けません");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;

				if ($cmd eq $no) {

					&send_item($m{name}, $kind, $item_no, $item_c, $item_lv);

					$mes .= $kind eq '1' ? "$weas[$item_no][1]"
						  : $kind eq '2' ? "$eggs[$item_no][1]"
						  :				   "$pets[$item_no][1]"
						  ;
					$mes .= 'を預かり所に戻しました<br>';
				}
				else {
					push @lines, $line;
				}
			}
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;

			&tp_100;
		}
	}
	else {
		&begin;
	}
}


#=================================================
# 店頭に置く
#=================================================
sub tp_200 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $i = 1;

	$mes .= 'どれをお店に出しますか?<br>';
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>やめる<br>|;

	open my $fh, "< $userdir/$id/depot.cgi" or &error("$userdir/$id/depot.cgi が読み込めません");
	while (my $line = <$fh>) {
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

		$mes .= $kind eq '1' ? qq|<input type="radio" name="cmd" value="$i">[$weas[$item_no][2]]$weas[$item_no][1]★$item_lv($item_c/$weas[$item_no][4])<br>|
			  : $kind eq '2' ? qq|<input type="radio" name="cmd" value="$i">[卵]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])<br>|
			  :				   qq|<input type="radio" name="cmd" value="$i">[ぺ]$pets[$item_no][1]<br>|
			  ;
		++$i;
	}
	close $fh;
	$mes .= qq|<p>値段：<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="お店に置く" class="button1"></p></form>|;

	$m{tp} = 210;
}
sub tp_210 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	if ($cmd) {
		my @shop_items = ();
		open my $in, "< $this_file" or &error("$this_fileが読み込めません");
		push @shop_items, $_ while <$in>;
		close $in;

		if (@shop_items >= $max_shop_item) {
			$mes .= 'これ以上お店に商品を置くことはできません<br>';
			&begin;
			return;
		}
	elsif ($in{price} =~ /[^0-9]/ || $in{price} <= 0 || $in{price} >= 5000001) {
			$mes .= '値段は 1 G 以上 499万9999 G以内にする必要があります<br>';
			&begin;
			return;
		}

		my @lines = ();
		my $i = 1;
		open my $fh, "+< $userdir/$id/depot.cgi" or &error("$userdir/$id/depot.cgi が開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			if ($cmd eq $i) {
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

				my($last_no) = (split /<>/, $shop_items[-1])[0];
				++$last_no;

				open my $fh2, ">> $this_file" or &error("$this_fileが開けません");
				print $fh2 "$last_no<>$kind<>$item_no<>$item_c<>$item_lv<>$in{price}<>\n";
				close $fh2;

				$mes .= $kind eq '1' ? "$weas[$item_no][1]"
					  : $kind eq '2' ? "$eggs[$item_no][1]"
					  :				   "$pets[$item_no][1]"
					  ;
				$mes .= "を $in{price} Gで店頭に並べました<br>";
			}
			else {
				push @lines, $line;
			}

			++$i;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		&tp_200;
	}
	else {
		&begin;
	}
}

#=================================================
# お店の設定
#=================================================
sub tp_300 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error('お店ﾘｽﾄが読み込めません');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		if ($name eq $m{name}) {
			$is_find = 1;

			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|前回の売上：$sale_c個 $sale_money G<br>|;
			$mes .= qq|<hr>お店の名前[全角8(半角16)文字まで]：<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|紹介文[全角20(半角40)文字まで]：<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="変更する" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;

	# お店があるのにﾘｽﾄにないのはおかしいのでもう一度追加
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error('お店ﾘｽﾄﾌｧｲﾙが開けません');
		print $fh3 "$m{name}店<>$m{name}<>$date開店<>0<>0<>\n";
		close $fh3;
	}

	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= 'やめました';
		&begin;
		return;
	}

	&error('お店の名前が長すぎます。全角8(半角16)文字まで') if length $in{name} > 16;
	&error('紹介文が長すぎます。全角20(半角40)文字まで') if length $in{mes} > 40;

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $shop_list_file" or &error('お店ﾘｽﾄが開けません');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		if ($name eq $m{name}) {
			unless ($shop_name eq $in{name}) {
				$mes .= "お店の名前を $in{name} に変えました<br>";
				$shop_name = $in{name};
				$is_rewrite = 1;
			}
			unless ($message eq $in{message}) {
				$mes .= "紹介文を $in{message} に変えました<br>";
				$message = $in{message};
				$is_rewrite = 1;
			}

			if ($is_rewrite) {
				$line = "$shop_name<>$name<>$message<>$sale_c<>$sale_money<>\n";
			}
			else {
				last;
			}
		}
		elsif ($shop_name eq $in{name}) {
			&error("すでに同じ名前のお店が存在します");
		}
		push @lines, $line;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}


1; # 削除不可
