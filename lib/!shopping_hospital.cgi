#=================================================
# 黒十字病院 Created by Merino
#=================================================

# ------------------
# 整形手術のｱｲｺﾝ表示
# [PC]一覧表示の折り返し数
my $tr = 10;

# [携帯]１ﾍﾟｰｼﾞの表示数
my $max_mobile_icon = 30;

# ------------------
# ﾍﾞｰｽとなる金額
my $base_price = $m{sedai} > 8 ? 400 + ($m{lv} * 10) : ($m{sedai} * 50) + ($m{lv} * 10);

# ﾒﾆｭｰ
my @menus = (
	# ﾒﾆｭｰ名,		値段
	['やめる',		0],
	['治癒',		$base_price * 20],
	['性転換手術',	$base_price * 50],
	['ﾛﾎﾞﾄﾐｰ手術',	500000],
	['整形手術',	1000], # ｱｲｺﾝを使わない場合はこの行と sub tp_400以降を削除してOK
);


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かありますかぁ?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '黒十字病院へようこそぉ<br>本日はどのようなご用件でしょぅかぁ?';
	}
	
	&menu(map { $_->[0] } @menus);
}
sub tp_1 {
	return if &is_ng_cmd(1..$#menus+1);
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#================================================
# 治癒
#================================================
sub tp_100 {
	$mes .= "$menus[1][0]わぁ、貴方の傷を癒すことができるわよぉ<br>";
	$mes .= "ただしぃ、$menus[1][1] Gのお金がかかるのぉ<br>";
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "$menus[1][0]する");
}
sub tp_110 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $menus[1][1]) {
		$mes .= "西洋の神秘の力を使って貴方の体を癒すわよぉ<br>";
		$mes .= "そぉれ、ﾊｯｽﾙｩ〜ﾊｯｽﾙｩ〜♪元気になったでしょ<br>";
		$mes .= "あたしが必要になったらまた来てね<br>";
		$m{hp} = $m{max_hp};
		$m{mp} = $m{max_mp};
		$m{money} -= $menus[1][1];
		&refresh;
		&n_menu;
	}
	else {
		$mes .= 'あらぁ、お金が足りませんわぁ<br>';
		&begin;
	}
}

#================================================
# 性転換
#================================================
sub tp_200 {
	$mes .= "$menus[2][0]をすると、$sexes[$m{sex}]じゃなくなっちゃうけどいいのかしらぁ?<br>";
	$mes .= "手術をするには、$menus[2][1] Gと手術時間$GWT分必要よぉ<br>";
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "$menus[2][0]する");
}
sub tp_210 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $menus[2][1]) {
		$mes .= '麻酔を打って手術を始めるわね<br>';
		$mes .= '次に目覚めたときにわぁ別人となっているわよぉ<br>';
		$m{sex} = $m{sex} eq '1' ? 2 : 1;
		$m{hp}  = $m{max_hp};
		$m{mp}  = $m{max_mp};
		$m{act} = 0;
		$m{money} -= $menus[2][1];
		&refresh;
		&wait;
		&write_memory("意を決して $sexes[$m{sex}] に性転換手術をしました");
	}
	else {
		$mes .= 'あらぁ、お金が足りませんわぁ<br>';
		&begin;
	}
}

#================================================
# ﾛﾎﾞﾄﾐｰ手術
#================================================
sub tp_300 {
	$mes .= "$menus[3][0]をするとぉ、貴方のお名前やﾊﾟｽﾜｰﾄﾞを変えることができるわぁ<br>";
	$mes .= "ただしﾄ･ｸ･ﾍﾞ･ﾂな大手術だからぁ、$cs{name}[0]の方しかすることができないのぉ<br>" if $m{country};
	$mes .= "手術をするには、$menus[3][1] Gと手術時間$GWT分必要よぉ<br>";
	$mes .= "手術をするとぉ、現在利用している銀行のお金はなくなってしまうわよぉ<br>" if $m{bank};
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "$menus[3][0]する");
}
sub tp_310 {
	return if &is_ng_cmd(1);
	if ($m{country}) {
		$mes .= "$cs{name}[0]になってからぁ、また来てね<br>";
		&begin;
		return;
	}

	$mes .= qq|それでわぁ、新しいお名前とﾊﾟｽﾜｰﾄﾞを教えてね<br>|;
	$mes .= qq|<form method="GET" action="$script"><table class="table1">|;
	$mes .= qq|<tr><td><tt>ﾌﾟﾚｲﾔ-名：</tt></td><td><input type="text" name="new_name" value="$m{name}" class="text_box1"><br></td></tr>|;
	$mes .= qq|<tr><td><tt>ﾊﾟｽﾜｰﾄﾞ ：</tt></td><td><input type="text" name="new_pass" value="$m{pass}" class="text_box1"><br></td></tr>|;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="確定" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_320 {
	if ($m{country}) {
		$mes .= "$cs{name}[0]になってからぁ、また来てね<br>";
		&begin;
		return;
	}
	elsif ($m{money} < $menus[3][1]) {
		$mes .= 'あらぁ、お金が足りませんわぁ<br>';
		&begin;
		return;
	}
	elsif (!$in{new_name} && $in{new_pass} eq '') {
		&begin;
		return;
	}
	elsif ($in{new_name} eq $m{name} && $in{new_pass} eq $m{pass}) {
		&begin;
		return;
	}

	&error('ﾌﾟﾚｲﾔ-名が入力されていません')	unless $in{new_name};
	&error('ﾊﾟｽﾜｰﾄﾞが入力されていません')	if $in{new_pass} eq '';

	&error('ﾌﾟﾚｲﾔ-名に不正な文字( ,;\"\'&<>\\\/ )が含まれています')	if $in{new_name} =~ /[,;\"\'&<>\\\/]/;
	&error('ﾌﾟﾚｲﾔ-名に不正な空白が含まれています')				if $in{new_name} =~ /　/ || $in{new_name} =~ /\s/;
	&error('ﾌﾟﾚｲﾔ-名は全角6(半角12)文字以内です')				if length($in{new_name}) > 12;
	&error('ﾊﾟｽﾜｰﾄﾞは半角英数字で入力して下さい')				if $in{new_pass} =~ m/[^0-9a-zA-Z]/;
	&error('ﾊﾟｽﾜｰﾄﾞは半角英数字4〜12文字です')					if length $in{new_pass} < 4 || length $in{new_pass} > 12;
	&error('ﾌﾟﾚｲﾔ-名とﾊﾟｽﾜｰﾄﾞが同一文字列です')					if $in{new_name} eq $in{new_pass};

	unless ($m{name} eq $in{new_name}) {
		my $new_id = unpack 'H*', $in{new_name};
		&error('その名前はすでに使われています') if -d "$userdir/$new_id";
		&write_world_news("$m{name} が $in{new_name} と改名をしました", 1);

		rename "$userdir/$id", "$userdir/$new_id" or &error('名前の変換に失敗しました');

		my @lines = ();
		open my $fh, "+< $logdir/0/member.cgi" or &error("$cs{name}[0]のﾒﾝﾊﾞｰﾌｧｲﾙが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			next if $line eq $m{name};
			push @lines, "$line\n";
		}
		push @lines, "$in{new_name}\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		$id = $new_id;
		$m{name} = $in{new_name};
		$mes .= qq|<font color="#FF0000">新ﾌﾟﾚｲﾔｰ名:$in{new_name}</font><br>|;
	}

	unless ($m{pass} eq $in{new_pass}) {
		$m{pass} = $in{new_pass};
		$pass    = $in{new_pass};
		$mes .= qq|<font color="#FF0000">新ﾊﾟｽﾜｰﾄﾞ:$in{new_pass}</font><br>|;
	}
	
	$m{hp}  = $m{max_hp};
	$m{mp}  = $m{max_mp};
	$m{act} = 0;
	$m{bank} = '';
	$m{money} -= $menus[3][1];
	&refresh;
	&wait;
	
	$mes .= qq|昔の貴方はもう存在しないわぁ<br><font color="#FF0000"><b>新しい名前とﾊﾟｽﾜｰﾄﾞを忘れないようにね</b></font><br>|;
	$mes .= qq|[次回から入力省略]にﾁｪｯｸを入れいている人わぁ、一度ﾛｸﾞｲﾝし直した方がいいわよぉ<br>| unless $is_mobile;
}

#================================================
# 整形
#================================================
sub tp_400 {
	if ($default_icon eq '') {
		$mes .= 'ごめんなさぁい。この病院には整形のﾄﾞｸﾀｰがいないのぉ<br>';
		&begin;
		return;
	}
	$mes .= "$menus[4][0]は、貴方の顔をまったくの別人にしちゃうわよぉ<br>";
#	$mes .= "今使用している顔ｶﾀﾛｸﾞは、ﾏｲﾋﾟｸﾁｬに戻るわよぉ<br>" if -f "$icondir/$m{icon}";
	$mes .= "手術をするには、$menus[4][1] Gと手術時間$GWT分かかりますけどぉ<br>";
	$mes .= "どぉするぅ？<br>";
	$m{tp} += 10;
	&menu("やめる", "$menus[4][0]する");
}
sub tp_410 {
	return if &is_ng_cmd(1);
	if ($default_icon eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	$mes .= 'どのようなお顔にしますぅ?<br>ｶﾀﾛｸﾞからお選びくださぁい<br>';
	unless ($m{icon} eq $default_icon) {
		my $file_title = &get_goods_title($m{icon});
		$mes .= "現在の顔ｱｲｺﾝﾀｲﾄﾙ『$file_title』<br>";
	}

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="icon" value="0" checked> やめる<hr>|;
	
	opendir my $dh, "$userdir/$id/picture" or &error('ﾏｲﾋﾟｸﾁｬが開けません');
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^_/;
		next if $file_name =~ /\.html$/;

		my $file_title = &get_goods_title($file_name);
		$mes .= qq|<input type="radio" name="icon" value="$file_name"><img src="$userdir/$id/picture/$file_name" $mobile_icon_size> $file_title<hr>|;
	}
	closedir $dh;

	$mes .= qq|<input type="radio" name="icon" value="$default_icon"><img src="$icondir/$default_icon" $mobile_icon_size> ﾃﾞﾌｫﾙﾄ<hr>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="決定" class="button1"></form>|;

	$m{tp} += 10;
	&n_menu;
}
sub tp_420 {
	if ($default_icon eq '') {
		&begin;
		return;
	}

	if ( $in{icon} && ($in{icon} eq $default_icon || -f "$userdir/$id/picture/$in{icon}") ) {
		if ($m{money} >= $menus[4][1]) {
			# 自作ｱｲｺﾝ
			unless ($in{icon} eq $default_icon) {
				&error("$non_titleのものは整形することができません") if $in{icon} =~ /^_/;
				&error("同じﾀｲﾄﾙのものがすでに使われています") if -f "$icondir/$in{icon}";
				
				# 変更前のｱｲｺﾝが自作ｱｲｺﾝならﾏｲﾋﾟｸﾁｬに戻す
				if ($m{icon} ne $default_icon && -f "$icondir/$m{icon}") {
					if (-f "$userdir/$id/picture/$m{icon}") {
						$mes .= "同じﾀｲﾄﾙの絵がﾏｲﾋﾟｸﾁｬにあったため、変更前の顔ｶﾀﾛｸﾞは消滅しました<br>";
					}
					else {
						rename "$icondir/$m{icon}", "$userdir/$id/picture/$m{icon}" or &error("あらやだ、整形に失敗しちゃったわぁ");
						my $file_title = &get_goods_title($m{icon});
						$mes .= "変更前に使用していた『$file_title』がﾏｲﾋﾟｸﾁｬに戻りました<br>";
					}
				}
				rename "$userdir/$id/picture/$in{icon}", "$icondir/$in{icon}"  or &error("あらやだ、整形に失敗しちゃったわぁ");
			}

			$m{icon} = $in{icon};

			$mes .= '麻酔を打って手術を始めるわね<br>';
			$mes .= '次に目覚めたときにわぁ別人となっているわよぉ<br>';
			
			$m{hp}  = $m{max_hp};
			$m{mp}  = $m{max_mp};
			$m{act} = 0;
			$m{money} -= $menus[4][1];
			&refresh;
			&wait;
		}
		else {
			$mes .= 'あらぁ、お金が足りませんわぁ<br>';
			&begin;
		}
	}
	else {
		$mes .= 'やめました<br>';
		&begin;
	}
}



1; # 削除不可
