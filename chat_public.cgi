#!/usr/bin/perl
require 'config.cgi';
require './lib/chat.cgi';
#=================================================
# ‹¤’ÊÁ¬¯Ä Created by Merino
#=================================================
&get_data;

$this_title  = "Œğ—¬Lê";
$this_file   = "$logdir/chat_public";
$this_script = 'chat_public.cgi';

@denies = ('pw126254065205.8.panda-world.ne.jp');

&header2;

#=================================================
&run;
&footer;
exit;
