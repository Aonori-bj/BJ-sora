#!/usr/bin/perl
require 'config.cgi';
require "$datadir/contest.cgi";
#================================================
# ｺﾝﾃｽﾄ Created by Merino
#================================================
# past 過去, prepare ｴﾝﾄﾘｰ受付(次のｺﾝﾃｽﾄ), entry 現ｺﾝﾃｽﾄ

# 殿堂入り　追加削除並べ替え可能
my @legends = (
#	['ﾀｲﾄﾙ',		'ﾛｸﾞﾌｧｲﾙ名','種類'	],
	['究極の美',	'picture',	'img',	],
	['幻の名作',	'book',		'html'	],
	['永遠の名題',	'etc',		'html'	],
);
# １位に投票した人に送られるﾀﾏｺﾞ
my @egg_nos = (1..34,42..50);
my $free_theme = 'ﾌﾘｰﾃｰﾏ';#物語ｺﾝﾃｽﾄのお題がない時の表示

#================================================
&decode;
$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @contests;
my $this_dir = "$logdir/contest/$contests[$in{no}][1]";

&header;
&header_contest;

if    ($in{mode} eq 'past')   { &past; }
elsif ($in{mode} eq 'legend') { &legend; }
elsif ($in{mode} eq 'vote' && $in{vote} && $in{id} && $in{pass}) { &vote; &top; }
else { &top; }

&footer;
exit;

#================================================
# ｺﾝﾃｽﾄ用header
#================================================
sub header_contest {
	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	}

	for my $i (0 .. $#contests) {
		print $in{mode} ne 'legend' && $i eq $in{no} ? qq|$contests[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$contests[$i][0]</a> / |;
	}

	for my $i (0 .. $#legends) {
		print $in{mode} eq 'legend' && $i eq $in{no} ? qq|$legends[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i&mode=legend">$legends[$i][0]</a> / |;
	}
	print qq|<hr>|;
}


#================================================
# 殿堂入り
#================================================
sub legend {
	print qq|<h1>$legends[$in{no}][0]</h1><hr>|;
	open my $fh, "< $logdir/legend/$legends[$in{no}][1].cgi" or &error("$logdir/legend/$legends[$in{no}][1].cgiﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($round, $name, $file_title, $file_name, $ldate) = split /<>/, $line;
		print $legends[$in{no}][2] eq 'img'  ? qq|<img src="$logdir/legend/$legends[$in{no}][1]/$file_name" style="border: 5px ridge #FC3; vertical-align:middle;"> 第$round回$contests[$in{no}][0]優秀作品『$file_title』作:$name <font size="1">($ldate)</font><hr>|
			#: $legends[$in{no}][2] eq 'html' && $legends[$in{no}][1] eq 'book' ? qq|第$round回$contests[$in{no}][0]優秀作品 『<a href="$logdir/legend/$legends[$in{no}][1]/$file_name" target="_blank">$file_title</a>』作:$name <font size="1">($ldate)</font><hr>|
			: $legends[$in{no}][2] eq 'html' ? qq|第$round回$contests[$in{no}][0]優秀作品 『<a href="$logdir/legend/$legends[$in{no}][1]/$file_name" target="_blank">$file_title</a>』作:$name <font size="1">($ldate)</font><hr>|
			:                                  qq|第$round回$contests[$in{no}][0]優秀作品 『$file_title』作:$name <font size="1">($ldate)</font><hr>|
			;
	}
	close $fh;
}


#================================================
# 前回のｺﾝﾃｽﾄ結果
#================================================
sub past {
	print qq|<form method="$method" action="contest.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="submit" value="現在のｺﾝﾃｽﾄ" class="button1"></form>|;

	if (-s "$this_dir/past.cgi") {
		open my $fh, "< $this_dir/past.cgi" or &error("$this_dir/past.cgiﾌｧｲﾙが読み込めません");
		my $head_line = <$fh>;
		my($etime, $round) = split /<>/, $head_line;
		print qq|<h1>第$round回$contests[$in{no}][0] 結果</h1><hr>|;
		while (my $line = <$fh>) {
			my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;

			print $contests[$in{no}][2] eq 'img'  ? qq|<img src="$this_dir/$round/$file_name" style="vertical-align:middle;"> 『$file_title』 作:$name ◇ <b>$vote</b>票<br>$comment<hr>|
				#: $contests[$in{no}][2] eq 'html' && $contests[$in{no}][1] eq 'book' ? qq|『<a href="$this_dir/$round/$file_name" target="_blank">$file_title</a>』 作:$name ◇ <b>$vote</b>票<br>$comment<hr>|#96,126行目にお題コンテスト用の処理を追加　by あおのり
				: $contests[$in{no}][2] eq 'html' ? qq|『<a href="$this_dir/$round/$file_name" target="_blank">$file_title</a>』 作:$name ◇ <b>$vote</b>票<br>$comment<hr>|
				:                                   qq|『$file_title』 作:$name ◇ <b>$vote</b>票<br>$comment<hr>|;
				;
		}
		close $fh;
	}
	else {
		print qq|<p>前回のｺﾝﾃｽﾄは開催されていません</p>|;
	}
}


#================================================
# top
#================================================
sub top {
	print qq|<form method="$method" action="contest.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="mode" value="past"><input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="submit" value="前回の結果" class="button1"></form>|;

	my $sub_mes = '<hr>';
	open my $fh, "< $this_dir/entry.cgi" or &error("$this_dir/entry.cgiﾌｧｲﾙが読み込めません");
	my $head_line = <$fh>;
	my($etime, $round ,$theme_display) = split /<>/, $head_line;#お題の取り込み
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;

		$sub_mes .= qq|<input type="radio" name="vote" value="$no">| if $in{id} && $in{pass};
		$sub_mes .= $contests[$in{no}][2] eq 'img'  ? qq|<img src="$this_dir/$round/$file_name" style="vertical-align:middle;"> No.$no『$file_title』<hr>|
				  #: $contests[$in{no}][2] eq 'html' && $contests[$in{no}][1] eq 'book' ? qq|No.$no『<a href="$this_dir/$round/$file_name" target="_blank">$file_title</a>』<hr>|
					: $contests[$in{no}][2] eq 'html' ? qq|No.$no『<a href="$this_dir/$round/$file_name" target="_blank">$file_title</a>』<hr>|
				  :                                   qq|No.$no『$file_title』<hr>|;
				  ;
		++$count;
	}
	close $fh;

	my($min,$hour,$day,$month) = (localtime($etime))[1..4];
	++$month;

	# 過去ｺﾝﾃｽﾄ削除→現ｺﾝﾃｽﾄを過去ｺﾝﾃｽﾄ→次ｺﾝﾃｽﾄを現ｺﾝﾃｽﾄにする処理
	if ($time > $etime) {
		++$round;
		print qq|<h1>第$round回$contests[$in{no}][0]</h1>|;
		print qq|<p>…集計処理中…</p>|;

		if ($count > 0) {
			&_send_goods_to_creaters if -s "$this_dir/past.cgi";
			&_result_contest;
		}
		#絵画、物語ｺﾝﾃｽﾄのお題表示 本来は_start_contestに入れたかったけど変数の関係で面倒なので　by あおのり
		open my $fh, "< $logdir/legend/$legends[2][1].cgi" or &error("$logdir/legend/$legends[$in{no}][1].cgiﾌｧｲﾙが読み込めません");
		while (my $line = <$fh>) {#物語ｺﾝﾃｽﾄの回と同一の回のお題殿堂入りやつ探す
			my($round2, $name, $file_title, $file_name, $ldate) = split /<>/, $line;
			if($round2 eq $round - 1 && rand(3) < 2 ){#ｺﾝﾃｽﾄ期限と同じファイルに保存
				$free_theme = $file_title;#free_themeはこのファイル先頭で定義
			}
		}
		close $fh;
		&_start_contest;
	}
	elsif ($min_entry_contest > $count) {
		++$round;
		print qq|<h1>第$round回$contests[$in{no}][0]</h1>|;
		print qq|<p>【投票終了日・次回ｺﾝﾃｽﾄ $month月$day日$hour時$min分】</p>|;
		print qq|<p>登録者が集まっていないため開催延期中です</p>|;
		print qq|<p>今回のお題は「$theme_display」です</p>|;
	}
	elsif ($in{id} && $in{pass}) {
		print qq|<h1>第$round回$contests[$in{no}][0]</h1>|;
		print qq|<p>【投票終了日・次回ｺﾝﾃｽﾄ $month月$day日$hour時$min分】</p>|;
		print qq|<p>今回のお題は「$theme_display」です</p>|;
		print qq|<p><font color="#FF9999"><b>$mes</b></font></p>| if $mes;
		print qq|<p>投票は一人一票まで</p>|;
		print qq|<form method="$method" action="contest.cgi">|;
		print qq|<input type="radio" name="vote" value="0" checked>やめる$sub_mes|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="hidden" name="mode" value="vote"><input type="hidden" name="no" value="$in{no}">|;
		print qq|ｺﾒﾝﾄ[全角30(半角60)文字まで]:<br><input type="text" name="vote_comment" class="text_box_b"><br>|;
		print qq|<input type="submit" value="投票" class="button_s"></form>|;
	}
	else {
		print qq|<h1>第$round回$contests[$in{no}][0]</h1>|;
		print qq|<p>【投票終了日・次回ｺﾝﾃｽﾄ $month月$day日$hour時$min分】</p>|;
		print $sub_mes;
	}
}
# ------------------
# 過去のｺﾝﾃｽﾄ作品を作者に返品しﾌｧｲﾙ･ﾌｫﾙﾀﾞ削除
sub _send_goods_to_creaters {
	my $count = 0;
	open my $fh, "+< $this_dir/past.cgi" or &error("$this_dir/past.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		++$count;
		next unless -f "$this_dir/$round/$file_name";

		my $y_id = unpack 'H*', $name;
		if (-d "$userdir/$y_id/picture") {
			# 作品を作者へ返還
			rename "$this_dir/$round/$file_name", "$userdir/$y_id/$contests[$in{no}][1]/$file_name" or &error("Cannot rename $this_dir/$round/$file_name to $userdir/$y_id/$contests[$in{no}][1]/$file_name");

			# 作品があるよﾌﾗｸﾞをたてる
			open my $fh5, "> $userdir/$y_id/goods_flag.cgi";
			close $fh5;
		}
		else {
			unlink "$this_dir/$round/$file_name" or &error("$this_dir/$round/$file_nameﾌｧｲﾙを削除することができません");
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	close $fh;

	opendir my $dh, "$this_dir/$round" or &error("$this_dir/$roundﾃﾞｨﾚｸﾄﾘを開くことができません");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		unlink "$this_dir/$round/$file_name" or &error("$this_dir/$round/$file_nameﾌｧｲﾙを削除することができません");
	}
	closedir $dh;
	rmdir "$this_dir/$round" or &error("$this_dir/$roundﾃﾞｨﾚｸﾄﾘを削除することができません");
}
# ------------------
# 結果を集計して過去ｺﾝﾃｽﾄにﾘﾈｰﾑ
sub _result_contest {
	my @lines = ();
	open my $fh, "+< $this_dir/entry.cgi" or &error("$this_dir/entry.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		push @lines, $line;
	}

	# 多い順にsort
	@lines = map { $_->[0] } sort { $b->[5] <=> $a->[5] } map { [$_, split/<>/] } @lines;

	unshift @lines, $head_line;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	rename "$this_dir/entry.cgi", "$this_dir/past.cgi" or &error("Cannot rename $this_dir/entry.cgi to $this_dir/past.cgi");

	# 作品をｺﾋﾟｰして殿堂入り
	&__copy_goods_to_legend($head_line, $lines[1]) if @lines > $min_entry_contest;

	&__send_prize(@lines);
}


# 上位に賞品送る
sub __send_prize {
	my @lines = @_;

	require 'config_game.cgi'; # regist_you_data()のため

	my $head_line = shift @lines;
	my($etime, $round) = split /<>/, $head_line;

	my $count = 1;
	for my $line (@lines) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;

		# 1位なら称号
		if ($count eq '1') {
			&regist_you_data($name, 'shogo', $contests[$in{no}][3]);

			for my $v_name (split /,/, $vote_names) {
				next unless $v_name;
				my $egg_no = $egg_nos[int(rand(@egg_nos))];
				&send_item($v_name, 2, $egg_no);
			}
			&write_send_news("第$round回$contests[$in{no}][0]第$count位の$nameに投票した人にﾀﾏｺﾞが送られました");
		}

		&send_item($name, 2, $c_prizes[$count-1][0]);
		&send_money($name, $contests[$in{no}][0], $c_prizes[$count-1][1]);
		&write_send_news("<b>第$round回$contests[$in{no}][0]第$count位の$nameに$c_prizes[$count-1][1] Gと $eggs[ $c_prizes[$count-1][0] ][1]が送られました</b>", 1, $name);

		last if ++$count > @c_prizes;
	}
}


sub __copy_goods_to_legend {
	my($head_line, $line) = @_;
	my($etime, $round) = split /<>/, $head_line;
	my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;

	# すでに同じﾌｧｲﾙ名が存在していたら殿堂入りはしない
	return if -f "$logdir/legend/$contests[$in{no}][1]/$file_name";

	# 作品を殿堂入りﾌｫﾙﾀﾞにｺﾋﾟｰ
	open my $in, "< $this_dir/$round/$file_name";
	binmode $in;
	my @datas = <$in>;
	close $in;

	open my $out, "> $logdir/legend/$contests[$in{no}][1]/$file_name";
	binmode $out;
	print $out @datas;
	close $out;

	# 殿堂入りﾌｧｲﾙに作者やﾌｧｲﾙ名など記入
	my @lines = ();
	open my $fh, "+< $logdir/legend/$contests[$in{no}][1].cgi";
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if (@lines > $max_log - 1) {
			my($dround, $dname, $dfile_title, $dfile_name) = split /<>/, $line;
			unlink "$logdir/legend/$contests[$in{no}][1]/$dfile_name" if -f "$logdir/legend/$contests[$in{no}][1]/$dfile_name";
		}
		else {
			push @lines, $line;
		}
	}
	unshift @lines, "$round<>$name<>$file_title<>$file_name<>$date<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

# ------------------
# 次ｺﾝﾃｽﾄを現ｺﾝﾃｽﾄにﾘﾈｰﾑ
sub _start_contest {
	my $end_time = $time + 24 * 60 * 60 * $contest_cycle_day;

	my @lines = ();
	open my $fh, "+< $this_dir/prepare.cgi" or &error("$this_dir/prepare.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	push @lines, "$end_time<>$round<>$free_theme<>\n";

	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	# ｴﾝﾄﾘｰ数が最低ｴﾝﾄﾘｰ数を超えた場合は開催
	if ( @lines > $min_entry_contest ) {
		rename "$this_dir/prepare.cgi", "$this_dir/entry.cgi" or &error("Cannot rename $this_dir/prepare.cgi to $this_dir/entry.cgi");

		# 投票/未投票識別ﾌｧｲﾙを初期化
		open my $fh3, "> $this_dir/vote_name.cgi" or &error("$this_dir/vote_name.cgiﾌｧｲﾙが作れません");
		print $fh3 ",";
		close $fh3;

		# 開催宣言
		require 'config_game.cgi'; # write_send_news()のため
		my($min,$hour,$day,$month) = (localtime($end_time))[1..4];
		++$month;
		&write_world_news("<i>第$round回$contests[$in{no}][0]が開催されました！投票締め切りは$month月$day日$hour時までです</i>");

		# 次ｺﾝﾃｽﾄを初期化
		++$round;
	 	open my $fh2, "> $this_dir/prepare.cgi" or &error("$this_dir/prepare.cgiﾌｧｲﾙが開けません");
		print $fh2 "$end_time<>$round<>\n";
		close $fh2;
		mkdir "$this_dir/$round" or &error("$this_dir/$roundﾃﾞｨﾚｸﾄﾘが作れません");
	}
	else {
		# 時間を延長
		--$round;
	 	open my $fh2, "> $this_dir/entry.cgi" or &error("$this_dir/entry.cgiﾌｧｲﾙが開けません");
		print $fh2 "$end_time<>$round<>$free_theme<>\n";
		close $fh2;
	}
}

#=================================================
# 投票処理
#=================================================
sub vote {
	&read_user;
	&error("ｺﾒﾝﾄの文字数ｵｰﾊﾞｰ。全角30[半角60]文字まで") if length $in{vote_comment} > 60;

	# 投票済みならﾘﾀｰﾝ。未投票なら名前を追加
	if (&add_vote_name) {
		$mes .= "現在行われている $contests[$in{no}][0] にはすでに投票済みです<br>";
		return;
	}

	my @lines = ();
	open my $fh, "+< $this_dir/entry.cgi" or &error("$this_dir/entry.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;

		if ($in{vote} eq $no) {
			++$vote;
			if ($in{vote_comment}) {
				$comment .= qq|<b>$m{name}</b>｢$in{vote_comment}｣,|;
				$mes .= "$in{vote_comment}というｺﾒﾝﾄで";
			}
			$mes .= "No.$no $file_titleに投票しました<br>";

			$line = "$no<>$name<>$file_title<>$file_name<>$vote<>$comment<>$m{name},$vote_names<>\n";
		}

		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}
# ------------------
sub add_vote_name {
	open my $fh, "+< $this_dir/vote_name.cgi" or &error("$this_dir/vote_name.cgiﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	$line =~ tr/\x0D\x0A//d;
	if ($line =~ /,\Q$m{name}\E,/) {
		close $fh;
		return 1;
	}
	$line .= "$m{name},";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	close $fh;
	return 0;
}
