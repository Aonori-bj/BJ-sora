#!/usr/bin/perl
require 'config.cgi';
#================================================
# ﾜﾝｸｯｼｮﾝﾘﾝｸ Created by Merino
#================================================
# 直ﾘﾝするとIDとﾊﾟｽがﾘﾌｧﾗｰなどに洩れてしまうため。

&decode;
&header;
&run;
&footer;
exit;

#================================================

sub run {
	my $url = $ENV{'QUERY_STRING'};

	$url =~ s/&#44;/,/g;
	$url =~ s/&lt;/</g;
	$url =~ s/&gt;/>/g;
	$url =~ s/&quot;/"/g;
	$url =~ s/&amp;/&amp/g;
	$url =~ s/&#59;/;/g;
	$url =~ s/&amp/&/g;
	print qq|<div class="mes"><a href="$url">$url</a><br><br></div>|;
}

