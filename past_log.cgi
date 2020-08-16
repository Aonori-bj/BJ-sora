#!/usr/bin/perl
require 'config.cgi';
#================================================
# 過去ﾛｸﾞ閲覧 Created by Merino
#================================================
&get_data;
&error("過去ﾛｸﾞﾌｧｲﾙ($in{this_file}_log.cgi)が存在しません") unless -f "$in{this_file}_log.cgi";
&error("他の国の過去ﾛｸﾞは見れません")   if $in{this_file} =~ m|/(\d+)/| && $1 ne $m{country};
&error("他の国の過去ﾛｸﾞは見れません")   if $in{this_file} =~ m|/(\d+?)_(\d+?)| && !($1 eq $m{country} || $2 eq $m{country});
&error("国の代表\者でないと見れません") if $in{this_file} =~ /daihyo/ && !&is_daihyo;
&run;
&footer;
exit;

#================================================
sub run {
	print qq|<form method="$method" action="$in{this_script}">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>過去ﾛｸﾞ/$in{this_title}</h2><hr>|;

	open my $fh, "< $in{this_file}_log.cgi" or &error("$in{this_file}_log.cgi ﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname <font size="1">($cs{name}[$bcountry] : $bdate)</font><br>$bcomment</font><hr size="1">\n|;
	}
	close $fh;
}


1; # 削除不可
