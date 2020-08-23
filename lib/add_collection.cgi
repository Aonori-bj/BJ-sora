#=================================================
# ｺﾚｸｼｮﾝ追加 Created by Merino
#=================================================
# 使い方: require './lib/add_collection.cgi'; して &add_collection;
# collction.cgi,depot.cgiで使用

#================================================
# ｺﾚｸｼｮﾝﾃﾞｰﾀ取得 + 今装備中のﾓﾉがｺﾚｸｼｮﾝにないなら追加
#=================================================
sub add_collection {
	my @kinds = ('', 'wea', 'egg', 'pet');
	my $kind = 1;
	my $is_rewrite = 0;
	my @lines = ();
	
	open my $fh, "+< $userdir/$id/collection.cgi" or &error("ｺﾚｸｼｮﾝﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d; # \n改行削除
		
		# 追加
		if ($m{ $kinds[$kind] } && $line !~ /,$m{ $kinds[$kind] },/) {
			$is_rewrite = 1;
			$line .= "$m{ $kinds[$kind] },";
			$mes .= $kind eq '1' ? $weas[$m{wea}][1]
				  : $kind eq '2' ? $eggs[$m{egg}][1]
				  :                $pets[$m{pet}][1]
				  ;
			$mes .= 'が新しく図鑑に追加されました<br>';
			
			# sort
			$line  = join ",", sort { $a <=> $b } split /,/, $line;
			$line .= ",";
		}
		
		push @lines, "$line\n";
		++$kind;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
	
	return @lines;
}


1; # 削除不可
