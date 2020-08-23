require "$datadir/skill.cgi";
my $this_file = "$userdir/$id/skill.cgi";
#================================================
# ½·ÙŒp³ Created by Merino
#================================================

#=================================================
sub begin {
	my @m_skills = split /,/, $m{skills};
	$layout = 2;
	if ($m{tp} > 1) {
		$mes .= '‘¼‚É‰½‚©‚µ‚Ü‚·‚©?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'K“¾Ï‚İ‚Ì‹Z‚ğŠw‚ñ‚¾‚èA¡Šo‚¦‚Ä‚¢‚é‹Z‚ğ–Y‚ê‚é‚±‚Æ‚ª‚Å‚«‚Ü‚·<br>';
	}

	$mes .= '<hr>Šo‚¦‚Ä‚¢‚é‹Z<br>';
	for my $no (@m_skills) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>';
	
	open my $fh, "< $this_file" or &error("$this_file‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $line = <$fh>;
	close $fh;
	$line =~ tr/\x0D\x0A//d;
	
	my $count = 0;
	my $sub_mes = '';
	for my $no (split /,/, $line) {
		next if $no eq ''; # æ“ª‚Ì‹ó
		
		$sub_mes .= "[$skills[$no][2]]$skills[$no][1] Á”ï$e2j{mp}$skills[$no][3]<br>" if $no;
		++$count;
	}
	my $comp_par = $count <= 0 ? 0 : int($count / $#skills * 100);
	$comp_par = 100 if $comp_par > 100;
	&write_comp_legend if $count eq $#skills;
	
	$mes .= "K“¾Ï‚İ‚Ì‹ZsºİÌß—¦ <b>$comp_par</b>%t<hr>";
	$mes .= $sub_mes;
	
	&menu('‚â‚ß‚é','Šo‚¦‚é','–Y‚ê‚é');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_' .$m{tp} };
}


#=================================================
# Šo‚¦‚é
#=================================================
sub tp_100 {
	$layout = 2;
	$m{tp} += 10;
	$mes .= "‚Ç‚Ì‹Z‚ğŠo‚¦‚Ü‚·‚©?<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked> ‚â‚ß‚é<br>|;
	
	open my $fh, "< $this_file" or &error("$this_file‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
	my $line = <$fh>;
	close $fh;
	$line =~ tr/\x0D\x0A//d;
	for my $no (split /,/, $line) {
		next unless $no;
		$mes .= qq|<input type="radio" name="cmd" value="$no">[$skills[$no][2]]$skills[$no][1]<br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="Šo‚¦‚é" class="button1"></form>|;
	&n_menu;
}
sub tp_110 {
	my @m_skills = split /,/, $m{skills};
	if ($cmd) {
		if (@m_skills >= 5) {
			$mes .= '5ŒÂ‚Ü‚Å‚µ‚©Šo‚¦‚é‚±‚Æ‚ª‚Å‚«‚Ü‚¹‚ñ<br>';
		}
		else {
			open my $fh, "< $this_file" or &error("$this_file‚ª“Ç‚İ‚ß‚Ü‚¹‚ñ");
			my $line = <$fh>;
			close $fh;
			$line =~ tr/\x0D\x0A//d;

			for my $no (split /,/, $line) {
				next unless $no;
				if ($no eq $cmd) {
					$mes .= "[$skills[$no][2]]$skills[$no][1]‚ğŠo‚¦‚Ü‚µ‚½!<br>";
					$m{skills} .= "$no,";
					last;
				}
			}
		}
	}
	&begin;
}

#=================================================
# –Y‚ê‚é
#=================================================
sub tp_200 {
	$m{tp} += 10;
	$mes .= "‚Ç‚Ì‹Z‚ğ–Y‚ê‚Ü‚·‚©?<br>";
	&menu('‚â‚ß‚é', map{ "[$skills[$_][2]]$skills[$_][1]" } split /,/, $m{skills});
}
sub tp_210 {
	my @m_skills = split /,/, $m{skills};
	if ($cmd) {
		my $line = '';
		for my $i (1 .. $#m_skills+1) {
			if ($i eq $cmd) {
				$mes .= "[$skills[ $m_skills[$i-1] ][2]]$skills[ $m_skills[$i-1] ][1]‚ğ–Y‚ê‚Ü‚µ‚½";
			}
			else {
				$line .= "$m_skills[$i-1],";
			}
		}
		$m{skills} = $line;
	}
	&begin;
}

#=================================================
# ºİÌßØ°Äˆ—
#=================================================
sub write_comp_legend {
	&write_legend('comp_skill', "$c_m‚Ì$m{name}‚ª‘S‚Ä‚Ì‹Z‚ğ‹É‚ß‚é", 1);
	&mes_and_world_news("<i>‘S‚Ä‚Ì‹Z‚ğºİÌßØ°Ä‚µ‚Ü‚µ‚½B$m{name}‚Éš‰œ‹`t”Í‚ÌÌ†‚ª‚ ‚½‚¦‚ç‚ê‚Ü‚µ‚½</i>");

	# ˆê“I‚ÈÌ†
	$m{shogo} = 'š‰œ‹`t”Í';

	# 0 ‚ğ’Ç‰Á‚·‚é‚±‚Æ‚Å ºİÌßflag‚Æ‚µ‚Ä0‚ğ’Ç‰Á100%‚ğ’´‚¦‚½”š‚É‚È‚é
	open my $fh, "+< $this_file" or &error("$this_fileÌ§²Ù‚ªŠJ‚¯‚Ü‚¹‚ñ");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	$line =~ tr/\x0D\x0A//d; # \n‰üsíœ
	$line .= '0,';
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	close $fh;
}


1; # íœ•s‰Â
