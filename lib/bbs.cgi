require './lib/_bbs_chat.cgi';
#================================================
# BBS Created by Merino
#================================================

# �A���������݋֎~����(�b)
$bad_time    = 10;

# �ő�۸ޕۑ�����
$max_log     = 50;

# �ő���Đ�(���p)
$max_comment = 2000;

# ���ް�ɕ\������鎞��(�b)
$limit_member_time = 60 * 4;

# �ő�ߋ�۸ޕۑ�����
$max_bbs_past_log = 50;


#================================================
sub run {
	if ($in{mode} eq "write" && $in{comment}) {
		&write_comment;
		
		# �ۑ�۸ޗp
		if ($in{is_save_log}) {
			if (&is_daihyo) {
				my $sub_this_file = $this_file;
				$this_file .= "_log";
				$max_log = $max_bbs_past_log;
				&write_comment;
				$this_file = $sub_this_file;
				$mes .= "�������݂�۸ޕۑ����܂���<br>";
			}
			else {
				$mes .= "���̑�\\�҈ȊO��۸ޕۑ��͂ł��܂���<br>";
			}
		}
	}
	
	my($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title <font size="2" style="font-weight:normal;">$this_sub_title</font></h2>|;
	print qq|<p>$mes</p>| if $mes;

	print qq|<form method="$method" action="past_log.cgi"><input type="hidden" name="this_title" value="$this_title">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="this_file" value="$this_file"><input type="hidden" name="this_script" value="$this_script">|;
	print qq|<input type="submit" value="�ߋ�۸�" class="button_s"></form>|;
	
	my $rows = $is_mobile ? 2 : 5;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="��������" class="button_s">|;
	print qq|�@ <input type="checkbox" name="is_save_log" value="1">۸ޕۑ�</form><br>|;
	print qq|<font size="2">$member_c�l:$member</font><hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$bicon = $bicon ? qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>| : '';
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			print qq|<div>$bicon<font color="$cs{color}[$bcountry]">$bname<br>$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font></div><hr size="1">\n|;
		}
		else {
			print qq|<table border="0"><tr><td valign="top" style="padding-right: 0.5em;">$bicon<br><font color="$cs{color}[$bcountry]">$bname</font></td><td valign="top"><font color="$cs{color}[$bcountry]">$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font><br></td></tr></table><hr size="1">\n|;
		}
	}
	close $fh;
}


1; # �폜�s��