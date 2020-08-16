#!/usr/bin/perl
require 'config.cgi';
#================================================
# Üİ¸¯¼®İØİ¸ Created by Merino
#================================================
# ’¼Øİ‚·‚é‚ÆID‚ÆÊß½‚ªØÌ§×°‚È‚Ç‚É‰k‚ê‚Ä‚µ‚Ü‚¤‚½‚ßB

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

