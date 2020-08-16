#!/usr/bin/perl
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# ‘ã•\ê—pŒf¦”Â Created by Merino
#=================================================
&get_data;
&error("$cs{name}[0]‚Ì•û‚Í“ü‚ê‚Ü‚¹‚ñ") if $m{country} eq '0';
&error("˜S–’†‚Í•]‹c‰ï‚É‚Í“ü‚ê‚Ü‚¹‚ñ") if $m{lib} eq 'prison';
&error("‘‚Ì‘ã•\\Ò‚Å‚È‚¢‚Æ“ü‚ê‚Ü‚¹‚ñ") unless &is_daihyo;

$this_title  = "Še‘‘ã•\\•]‹c‰ï";
$this_file   = "$logdir/bbs_daihyo";
$this_script = 'bbs_daihyo.cgi';

#=================================================
&run;
&footer;
exit;
