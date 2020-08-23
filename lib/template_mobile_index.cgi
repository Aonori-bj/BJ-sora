#================================================
# index.cgiÃİÌßÚ°Ä(Œg‘Ñ) Created by Merino
#================================================

#================================================
sub index {
	my($login_list, %cs_c) = @_;
	my($cook_name, $cook_pass, $cook_is_cookie) = &get_cookie;
	my $checked = $cook_is_cookie ? 'checked' : '';

	$cs_c{all} ||= 0;
	$cs_c{0}   ||= 0;
	print <<"EOM";
<h1>$title</h1>
<form method="$method" action="login.cgi">
<div>ÌßÚ²Ô°–¼:<input type="text" name="login_name" value="$cook_name"></div>
<div>Êß½Ü°ÄŞ:<input type="text" name="pass" value="$cook_pass"></div>
<div><input type="checkbox" name="is_cookie" value="1" $checked>Ÿ‰ñ‚©‚ç“ü—ÍÈ—ª(Cookie‘Î‰Œg‘Ñ‚Ì‚İ)</div>
<div><input type="submit" value="Û¸Ş²İ"></div>
<input type="hidden" name="guid" value="ON">
</form>
<hr>
<ol>
<li><a href="http://www13.atwiki.jp/blindjustice/" accesskey="1">à–¾‘</a>
<li><a href="new_entry.cgi" accesskey="2">V‹K“o˜^</a>
<li><a href="players.cgi" accesskey="4">ÌßÚ²Ô°ˆê——</a>
<li><a href="legend.cgi" accesskey="5">—I‹v‚ÌÎ”è</a>
<li><a href="sales_ranking.cgi" accesskey="6">¤l×İ·İ¸Ş</a>
<li><a href="contest.cgi" accesskey="7">ºİÃ½Ä‰ïê</a>
<li><a href="news.cgi" accesskey="8">‰ß‹‚Ì‰hŒõ</a>
<li><a href="$home_m" accesskey="9">HOME</a>
<li><a href="reset_player.cgi" accesskey="0">Ø¾¯Äˆ—</a>
</ol>
<hr>
Û¸Ş²İ’†$cs_c{all}l
<div>$login_list</div>
<hr>
’èˆõ $w{player}/$max_entryl<br>
ÌßÚ²Ô°•Û‘¶ŠúŠÔ $auto_delete_day“ú<br>
(1¢‘ã–Ú1ÚÍŞÙ‚Í5“ú)<br>
Šî–{S‘©ŠÔ $GWT•ª<br>
‹‹—^ $salary_hourŠÔ–ˆ<br>
ŒNå‚Ì”CŠú $reset_ceo_cycle_year”NüŠú
<hr>
EOM
}


1; # íœ•s‰Â
