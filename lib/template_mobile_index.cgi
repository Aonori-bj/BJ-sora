#================================================
# index.cgi����ڰ�(�g��) Created by Merino
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
<div>��ڲ԰��:<input type="text" name="login_name" value="$cook_name"></div>
<div>�߽ܰ��:<input type="text" name="pass" value="$cook_pass"></div>
<div><input type="checkbox" name="is_cookie" value="1" $checked>���񂩂���͏ȗ�(Cookie�Ή��g�т̂�)</div>
<div><input type="submit" value="۸޲�"></div>
<input type="hidden" name="guid" value="ON">
</form>
<hr>
<ol>
<li><a href="http://www13.atwiki.jp/blindjustice/" accesskey="1">������</a>
<li><a href="new_entry.cgi" accesskey="2">�V�K�o�^</a>
<li><a href="players.cgi" accesskey="4">��ڲ԰�ꗗ</a>
<li><a href="legend.cgi" accesskey="5">�I�v�̐Δ�</a>
<li><a href="sales_ranking.cgi" accesskey="6">���l�ݷݸ�</a>
<li><a href="contest.cgi" accesskey="7">��ýĉ��</a>
<li><a href="news.cgi" accesskey="8">�ߋ��̉h��</a>
<li><a href="$home_m" accesskey="9">HOME</a>
<li><a href="reset_player.cgi" accesskey="0">ؾ�ď���</a>
</ol>
<hr>
۸޲ݒ�$cs_c{all}�l
<div>$login_list</div>
<hr>
��� $w{player}/$max_entry�l<br>
��ڲ԰�ۑ����� $auto_delete_day��<br>
(1�����1���ق�5��)<br>
��{�S������ $GWT��<br>
���^ $salary_hour���Ԗ�<br>
�N��̔C�� $reset_ceo_cycle_year�N����
<hr>
EOM
}


1; # �폜�s��
