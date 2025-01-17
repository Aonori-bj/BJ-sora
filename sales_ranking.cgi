#!/usr/bin/perl
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# 売上ﾗﾝｷﾝｸﾞ Created by Merino
#=================================================

# 表示するもの(./log/にあるもの)　◎追加/変更/削除/並べ替え可能
my @files = (
#	['ﾀｲﾄﾙ',		'ﾛｸﾞﾌｧｲﾙ名(shop_list_xxxx←の部分)'],
	['商人のお店',	'',			'個'],
	['美の画伯館',	'picture',	'枚'],
	['ﾌﾞｯｸﾏｰｹｯﾄ',	'book',		'冊'],
	['商人の銀行',	'bank',		'回'],
);

# 最低限必要な売上数(商人のお店のみ)
my $min_sale_c = 5;


#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @files;
my $type = $files[$in{no}][1] ? "_$files[$in{no}][1]" : '';
my $flag_file = "$logdir/sales_ranking${type}_cycle_flag.cgi";
my $this_file = "$logdir/shop_list${type}.cgi";

&update_sales_ranking if -M $flag_file > $sales_ranking_cycle_day;
&run;
&footer;
exit;

#=================================================
# ﾗﾝｷﾝｸﾞ画面
#=================================================
sub run {
	my $flag_time = (stat $flag_file)[9];
	my($min, $hour, $mday, $month) = ( localtime( $flag_time + $sales_ranking_cycle_day * 24 * 3600) )[1..4];
	++$month;

	print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	for my $i (0 .. $#files) {
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?no=$i">$files[$i][0]</a> / |;
	}
	print qq|<h1>$files[$in{no}][0]売上ﾗﾝｷﾝｸﾞ</h1>|;
	print qq|<div class="mes"><ul><li>ﾗﾝｷﾝｸﾞと各お店の売上金と売上数は、$sales_ranking_cycle_day日ごとにﾘｾｯﾄされ更新されます|;

	if ($files[$in{no}][1] eq 'bank') {
		print "<li>更新のﾀｲﾐﾝｸﾞで手続回数が 0 回の銀行は倒産となります";
		print "<li>更新のﾀｲﾐﾝｸﾞで総預金額が 100万 G未満の銀行は倒産となります";
		print qq|<li>次の更新時間：$month月$mday日$hour時$min分</ul></div><br>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>利益</th><th>手続き</th><th>銀行名</th><th>経営者</th><th>ﾒｯｾｰｼﾞ</th></tr>| unless $is_mobile;
	}
	else {
		if ($files[$in{no}][1] eq '') {
			print qq|<li>更新のﾀｲﾐﾝｸﾞで売上数が $min_sale_c個未満のお店は閉店となります|;
		}
		else {
			print qq|<li>更新のﾀｲﾐﾝｸﾞで売上金が 0 Gのお店は閉店となります|;
		}
		print qq|<li>次の更新時間：$month月$mday日$hour時$min分</ul></div><br>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>順位</th><th>売上金</th><th>売上数</th><th>店名</th><th>店長</th><th>ﾒｯｾｰｼﾞ</th></tr>| unless $is_mobile;
	}
	
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_fileﾌｧｲﾙが読み込めません");
	while ($line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		print $is_mobile     ? qq|<hr><b>$rank</b>位/$sale_money G/$sale_c$files[$in{no}][2]/$shop_name/$name/$message/\n|
			: $rank % 2 == 0 ? qq|<tr><th>$rank位</th><td align="right">$sale_money G</td><td align="right">$sale_c$files[$in{no}][2]</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$rank位</th><td align="right">$sale_money G</td><td align="right">$sale_c$files[$in{no}][2]</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
}

#=================================================
# 売上ﾗﾝｷﾝｸﾞを更新
#=================================================
sub update_sales_ranking  {
	my %sames = ();
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_fileﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		# ﾊﾞｸﾞでお店が二つになっているものを除く
		next if ++$sames{$name} > 1;

		my $id = unpack 'H*', $name;
		next unless -f "$userdir/$id/shop${type}.cgi";
		
		open my $fh2, "+< $userdir/$id/shop_sale${type}.cgi";
		eval { flock $fh2, 2; };
		my $line2 = <$fh2>;
		my($m_sale_c, $m_sale_money) = split /<>/, $line2;
		
		# 商人の銀行、総預金ﾁｪｯｸ
		if ($files[$in{no}][1] eq 'bank' && &is_the_end("$userdir/$id/shop${type}.cgi") ) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			&write_send_news("<b>$nameの経営する$shop_nameは総預金額が100万未満のため倒産しました</b>", 1, $name);
		}
		# 売上金が 0G なら削除
		elsif ($m_sale_money <= 0) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			
			if ($files[$in{no}][1] eq 'bank') {
				&write_send_news("<b>$nameの経営する$shop_nameは経営破綻のため倒産しました</b>", 1, $name);
			}
			else {
				&write_send_news("<b>$nameの経営する$shop_nameは経営破綻のため閉店しました</b>", 1, $name);
			}
		}
		# 商人のお店は最低限必要な売上数もチェック
		elsif ($files[$in{no}][1] eq '' && $m_sale_c < $min_sale_c) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			&write_send_news("<b>$nameの経営する$shop_nameは経営破綻のため閉店しました</b>", 1, $name);
		}
		else {
			seek  $fh2, 0, 0,;
			truncate $fh2, 0;
			print $fh2 "0<>0<>";
			close $fh2;
			
			push @lines, "$shop_name<>$name<>$message<>$m_sale_c<>$m_sale_money<>\n";
		}
	}
	@lines = map{ $_->[0] } sort { $b->[4] <=> $a->[4] } map { [$_, split /<>/] } @lines;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	# 更新周期ﾌﾗｸﾞﾌｧｲﾙを更新
	open my $fh9, "> $flag_file";
	close $fh9;
}

sub is_the_end {
	my $bank_file = shift;
	
	my $sum_money = 0;
	open my $fh, "< $bank_file" or &error("$bank_fileﾌｧｲﾙが読み込めません");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		$sum_money += $money;
	}
	close $fh;
	
	return $sum_money < 1000000 ? 1 : 0;
}



