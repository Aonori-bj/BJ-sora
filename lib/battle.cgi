require "$datadir/skill.cgi";
$is_battle = 1; # ﾊﾞﾄﾙﾌﾗｸﾞ1
#================================================
# 戦闘 Created by Merino
#================================================

# 武器による優劣
my %tokkous = (
# '強い属性' => qr/弱い属性/,
	'剣' => qr/斧/,
	'斧' => qr/槍/,
	'槍' => qr/剣/,
	'炎' => qr/風|無/,
	'風' => qr/雷|無/,
	'雷' => qr/炎|無/,
	'無' => qr/剣|斧|槍/,
);

#================================================
# 使う値を Set
#================================================
my @m_skills = split /,/, $m{skills};
my @y_skills = split /,/, $y{skills};

# 画面表示やｽｷﾙで使うのでｸﾞﾛｰﾊﾞﾙ変数
$m_at = $m{at};
$y_at = $y{at};
$m_df = $m{df};
$y_df = $y{df};
$m_ag = $m{ag};
$y_ag = $y{ag};

# 使用するのは AT or MAT, DF or MDF のどちらか
if    ($weas[$m{wea}][2] =~ /無|剣|斧|槍/) { $m_at = $m{at}  + $weas[$m{wea}][3]; }
elsif ($weas[$m{wea}][2] =~ /炎|風|雷/)    { $m_at = $m{mat} + $weas[$m{wea}][3]; $y_df = $y{mdf}; }
if    ($weas[$y{wea}][2] =~ /無|剣|斧|槍/) { $y_at = $y{at}  + $weas[$y{wea}][3]; }
elsif ($weas[$y{wea}][2] =~ /炎|風|雷/)    { $y_at = $y{mat} + $weas[$y{wea}][3]; $m_df = $m{mdf}; }

$m_ag -= $weas[$m{wea}][5];
$m_ag = int(rand(5)) if $m_ag < 1;
$y_ag -= $weas[$y{wea}][5];
$y_ag = int(rand(5)) if $y_ag < 1;

$m_at = int($m_at * 0.5) if $m{wea} && $m{wea_c} <= 0;

if ($m{wea} && $y{wea}) {
	if (&is_tokkou($m{wea},$y{wea})){
		$m_at = int(1.5 *$m_at);
		$y_at = int(0.75*$y_at);
		$is_m_tokkou = 1;
	}
	elsif (&is_tokkou($y{wea},$m{wea})) {
		$y_at = int(1.5 *$y_at);
		$m_at = int(0.75*$m_at);
		$is_y_tokkou = 1;
	}
}

#================================================
# ﾒｲﾝ動作
#================================================
&run_battle;
&battle_menu if $m{hp} > 0 && $y{hp} > 0;


#================================================
# 実行処理
#================================================
sub run_battle {
	if ($cmd eq '') {
		$mes .= '戦闘ｺﾏﾝﾄﾞを選択してください<br>';
	}
	elsif ($m{turn} >= 20) { # なかなか決着つかない場合
		$mes .= '戦闘限界ﾀｰﾝを超えてしまった…これ以上は戦えません<br>';
		&lose;
	}
	elsif ( rand($m_ag * 3) >= rand($y_ag * 3) ) {
		my $v = &m_attack;
		if ($y{hp} <= 0 && $m{hp} > 0) {
			&win;
		}
		else {
			&y_attack;
			if    ($m{hp} <= 0) { &lose; }
			elsif ($y{hp} <= 0) { &win;  }
			elsif ($m{pet}) {
				&use_pet('battle', $v);
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	else {
		&y_attack;
		if ($m{hp} <= 0) {
			&lose;
		}
		else {
			my $v = &m_attack;
			if    ($m{hp} <= 0) { &lose;  }
			elsif ($y{hp} <= 0) { &win; }
			elsif ($m{pet}) {
				&use_pet('battle', $v);
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	
	$m{mp} = 0 if $m{mp} <= 0;
	$y{mp} = 0 if $y{mp} <= 0;
}


#=================================================
# 自分の攻撃
#=================================================
sub m_attack {
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	# 必殺技 正常なｺﾏﾝﾄﾞか # 属性が装備しているものと同じか # MPがあるか
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && $m{mp} >= $m_s->[3] ) {
		$m{mp} -= $m_s->[3];
		$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
		$mes .= "$m{name}の$m_s->[1]!!<br>";
		local $who = 'm';
		&{ $m_s->[4] }($m_at);
	}
	# ﾋﾟｺﾘﾝ! 習得技5未満 かつ 武器ﾚﾍﾞﾙ かつ 相手の強さ普通以上↑ 
	elsif (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0) {
		local $who = 'm';
		&_pikorin;
	}
	else { # 攻撃
		$mes .= "$m{name}の攻撃!!";
		my $v = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0
			? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
		
		if ($is_counter) {
			$mes .= "<br>攻撃を返され $v のﾀﾞﾒｰｼﾞをうけました<br>";
			$m{hp} -= $v;
		}
		elsif ($is_stanch) {
			$mes .= "<br>ｽﾀﾝで動けない!<br>";
		}
		else {
			$mes .= "<br>$v のﾀﾞﾒｰｼﾞをあたえました<br>";
			if ($m{wea_c} > 0) {
				--$m{wea_c};
				$mes .= "$weas[$m{wea}][1]は壊れてしまった<br>" if $m{wea_c} == 0;
			}
			$y{hp} -= $v;
		}
	}
}
#=================================================
# 相手の攻撃
#=================================================
sub y_attack {
	my $y_s = $skills[ $y_skills[ int(rand(6))-1 ] ];
	
	# 必殺技 正常なｺﾏﾝﾄﾞか # 属性が装備しているものと同じか # MPがあるか
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && $y{mp} >= $y_s->[3] ) {
		$y{mp} -= $y_s->[3];
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}の$y_s->[1]!!<br>";

		local $who = 'y';
		&{ $y_s->[4] }($y_at);
	}
	else {
		$mes .= "$y{name}の攻撃!!";
		my $v = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0
			? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);

		if ($is_counter) {
			$mes .= "<br>攻撃を返し $v のﾀﾞﾒｰｼﾞをあたえました<br>";
			$y{hp} -= $v;
		}
		elsif ($is_stanch) {
			$mes .= "<br>ｽﾀﾝで動けない!<br>";
		}
		else {
			$mes .= "<br>$v のﾀﾞﾒｰｼﾞをうけました<br>";
			$m{hp} -= $v;
		}
	}
}

#=================================================
# 会心、通常攻撃
#=================================================
sub _attack_kaishin {
	my $at = shift;
	$mes .= '<b>会心の一撃!!</b>';
	return int($at * (rand(0.4)+0.8) );
}
sub _attack_normal {
	my($at, $df) = @_;
	my $v = int( ($at * 0.5 - $df * 0.3) * (rand(0.3)+ 0.9) );
	   $v = int(rand(5)+1) if $v < 5;
	return $v;
}
#=================================================
# 新技習得(すでに覚えている技でも発動)
#=================================================
sub _pikorin {
	# 覚えられる属性のものを全て@linesに入れる
	my @lines = ();
	for my $i (1 .. $#skills) {
		push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
	}
	
	if (@lines) {
		my $no = $lines[int(rand(@lines))];
		$m_mes = "閃いた!! $skills[$no][1]!";
		# 覚えていない技なら追加
		my $is_learning = 1;
		for my $m_skill (@m_skills) {
			if ($m_skill eq $no) {
				$is_learning = 0;
				last;
			}
		}
		$m{skills} .= "$no," if $is_learning;
		$mes .= qq|<font color="#CCFF00">☆閃き!!$m{name}の$skills[ $no ][1]!!</font><br>|;
		$skills[ $no ][4]->($m_at);
	}
	else { # 例外処理：覚えられるものがない
		$m_mes = '閃めきそうで閃けない…';
	}
}


#=================================================
# 戦闘用メニュー
#=================================================
sub battle_menu {
	$menu_cmd  = qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
	$menu_cmd .= qq|<option value="0">攻撃</option>|;
	for my $i (1 .. $#m_skills+1) {
		next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
		next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
		$menu_cmd .= qq|<option value="$i"> $skills[ $m_skills[$i-1] ][1]</option>|;
	}
	$menu_cmd .= qq|</select><br><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= qq|<input type="submit" value="決 定" class="button1"></form>|;
}


#=================================================
# 勝利
#=================================================
sub win {
	$m{hp} = 0 if $m{hp} < 0;
	$y{hp} = 0;
	$m{turn} = 0;
	$mes .= "$y{name}を倒しました<br>";

	$m_mes = $m{mes_win}  unless $m_mes;
	$y_mes = $y{mes_lose} unless $y_mes;
}

#=================================================
# 敗北
#=================================================
sub lose {
	$m{hp} = 0;
	$y{hp} = 0 if $y{hp} < 0;
	$m{turn} = 0;
	$mes .= "$m{name}はやられてしまった…<br>";

	$m_mes = $m{mes_lose} unless $m_mes;
	$y_mes = $y{mes_win}  unless $y_mes;
}


#=================================================
# 武器により特攻がつくかどうか
#=================================================
sub is_tokkou {
	my($wea1, $wea2) = @_;
	return defined $tokkous{ $weas[$wea1][2] } && $weas[$wea2][2] =~ /$tokkous{ $weas[$wea1][2] }/ ? 1 : 0;
}



1; # 削除不可
