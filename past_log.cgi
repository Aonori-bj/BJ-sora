#!/usr/bin/perl
require 'config.cgi';
#================================================
# �ߋ�۸މ{�� Created by Merino
#================================================
&get_data;
&error("�ߋ�۸�̧��($in{this_file}_log.cgi)�����݂��܂���") unless -f "$in{this_file}_log.cgi";
&error("���̍��̉ߋ�۸ނ͌���܂���")   if $in{this_file} =~ m|/(\d+)/| && $1 ne $m{country};
&error("���̍��̉ߋ�۸ނ͌���܂���")   if $in{this_file} =~ m|/(\d+?)_(\d+?)| && !($1 eq $m{country} || $2 eq $m{country});
&error("���̑�\\�҂łȂ��ƌ���܂���") if $in{this_file} =~ /daihyo/ && !&is_daihyo;
&run;
&footer;
exit;

#================================================
sub run {
	print qq|<form method="$method" action="$in{this_script}">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>�ߋ�۸�/$in{this_title}</h2><hr>|;

	open my $fh, "< $in{this_file}_log.cgi" or &error("$in{this_file}_log.cgi ̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname <font size="1">($cs{name}[$bcountry] : $bdate)</font><br>$bcomment</font><hr size="1">\n|;
	}
	close $fh;
}


1; # �폜�s��