$mes .= qq|勲章 $m{medal}個<br>| if $is_mobile;
#=================================================
# 部隊変更 Created by Merino
#=================================================

# 勲章1個の金額
my $exchange_money = 3000;

# 引き換え品
my @prizes = (
# 種類 1=武器,2=卵,3=ﾍﾟｯﾄ 
#	[0]種類,[1]No,[2]勲章
	[0,	0,	0,	],
	[1,	12,	5,	],
	[1,	17,	5,	],
	[1,	27,	5,	],
	[2,	21,	15,	],
	[2,	33,	20,	],
	[2,	48,	25,	],
	[2,	3,	30,	],
	[2,	45,	80,	],
	[2,	37,	90,	],
	[2,	46,	99,	],
);


# 特別条件でｸﾗｽﾁｪﾝｼﾞできるもの
my %plus_needs = (
# 部隊No => 条件文,					if条件									# 条件ｸﾘｱ後の処理
	7  => ['ﾀﾞｰｸﾎｰｽを生贄',			sub{ $pets[$m{pet}][2] eq 'speed_up' },	sub{ $mes.="$pets[$m{pet}][1]を生贄にしました<br>"; $m{pet} = 0; } ],
	8  => ['ﾄﾞﾗｺﾞﾝ系のﾍﾟｯﾄを生贄',	sub{ $pets[$m{pet}][1] =~ /ﾄﾞﾗｺﾞﾝ/ },	sub{ $mes.="$pets[$m{pet}][1]を生贄にしました<br>"; $m{pet} = 0; } ],
	11 => ['職業が忍者',			sub{ $jobs[$m{job}][1] eq '忍者' },		sub{} ],
	12 => ["$eggs[23][1]を生贄",	sub{ $m{egg} eq '23'},					sub{ $mes.="$eggs[$m{egg}][1]を生贄にしました<br>"; $m{egg} = 0; $m{egg_c} = 0; } ],
	15 => ['職業が魔物使い',		sub{ $jobs[$m{job}][1] eq '魔物使い' },	sub{} ],
);


#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かありますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "ここでは$m{name}の持っている勲章に応じて部隊をｸﾗｽﾁｪﾝｼﾞしたりできます<br>";
		$mes .= 'どうしますか?<br>';
	}
	&menu('やめる','お金が欲しい','ｱｲﾃﾑが欲しい','部隊を変えたい');
}
sub tp_1 {
	return if &is_ng_cmd(1..3);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# 勲章→お金
#=================================================
sub tp_100 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}の所持している勲章は$m{medal}個ですね<br>";
	$mes .= "勲章1個につき $exchange_money Gに換えることができます<br>";
	$mes .= "何個の勲章を献上しますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="medal" value="0" class="text_box1" style="text-align:right">個|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="献上する" class="button1"></p></form>|;
}
sub tp_110 {
	if ($in{medal} && $in{medal} !~ /[^0-9]/) {
		if ($in{medal} > $m{medal}) {
			$mes .= "$in{medal}個も勲章を持っていません<br>";
		}
		else {
			my $v = $in{medal} * $exchange_money;
			$m{money} += $v;
			$m{medal} -= $in{medal};
			
			$mes .= "勲章$in{medal}個を献上して $v Gをもらいました<br>";
		}
	}
	&begin;
}

#=================================================
# 勲章→ｱｲﾃﾑ
#=================================================
sub tp_200 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}の所持している勲章は$m{medal}個ですね<br>";
	$mes .= "どれと交換しますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1" cellpadding="3"><tr><th>名前</th><th>勲章<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked>やめる<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i">|;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[卵]$eggs[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[ペ]$pets[ $prizes[$i][1] ][1]</td>|
			  ;
		$mes .= qq|<td align="right">$prizes[$i][2]個<br></td></tr>|;
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="交換する" class="button1"></p></form>|;
}
sub tp_210 {
	if ($cmd && defined $prizes[$cmd]) {
		if ($m{medal} >= $prizes[$cmd][2]) {
			$m{medal} -= $prizes[$cmd][2];
			
			$mes .= "勲章$prizes[$cmd][2]個を献上して";

			if ($prizes[$cmd][0] eq '1') {
				$mes .= "$weas[ $prizes[$cmd][1] ][1]に交換しました<br>";
				&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], $weas[ $prizes[$cmd][1] ][4]);
			}
			elsif ($prizes[$cmd][0] eq '2') {
				$mes .= "$eggs[ $prizes[$cmd][1] ][1]に交換しました<br>";
				&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1]);
			}
			elsif ($prizes[$cmd][0] eq '3') {
				$mes .= "$pets[ $prizes[$cmd][1] ][1]に交換しました<br>";
				&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1]);
			}
		}
		else {
			$mes .= '勲章が足りません<br>';
		}
	}
	&begin;
}

#=================================================
# 勲章→部隊＋お金
#=================================================
sub tp_300 {
	$m{tp} += 10;
	$mes .= "$m{name}の所持している勲章は$m{medal}個ですね<br>";
	$mes .= "ｸﾗｽﾁｪﾝｼﾞで余った勲章はお金に換金します<br>";
	$mes .= "どの部隊にｸﾗｽﾁｪﾝｼﾞしますか?<hr>";
	$mes .= "今の部隊からでｸﾗｽﾁｪﾝｼﾞできるのは以下です<br>";
	
	$mes .= "$units[0][1] 条件：なし<br>";
	my @menus = ('やめる', $units[0][1]);
	for my $i (1 .. $#units) {
		if ($i eq $units[$m{unit}][2]) {
			$mes .= "$units[$i][1] 条件：なし<br>";
			push @menus, $units[$i][1];
		}
		elsif ($m{unit} eq $units[$i][2]) {
			$mes .= "$units[$i][1] 条件：$units[ $units[$i][2] ][1]/勲章$units[$i][3]個/";
			$mes .= $plus_needs{$i}[0] if defined $plus_needs{$i};
			$mes .= "<br>";
			
			push @menus, $units[$i][1];
		}
		else {
			push @menus, '';
		}
	}
	
	&menu(@menus);
}
sub tp_310 {
	if ($cmd) {
		--$cmd;
		
		if ($cmd) {
			# ｸﾗｽﾀﾞｳﾝ
			unless ($cmd eq $units[$m{unit}][2]) {
				# 特殊条件
				if (defined $plus_needs{$cmd}) {
					if (&{ $plus_needs{$cmd}[1] } && $units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
						&{ $plus_needs{$cmd}[2] };
						$m{medal} -= $units[$cmd][3];
					}
					else {
						$mes .= "ｸﾗｽﾁｪﾝｼﾞできる条件を満たしていません<br>";
						&begin;
						return;
					}
				}
				elsif ($units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
					$m{medal} -= $units[$cmd][3];
				}
				else {
					$mes .= "ｸﾗｽﾁｪﾝｼﾞできる条件を満たしていません<br>";
					&begin;
					return;
				}
			}
		}
		
		$m{unit} = $cmd;
		$mes .= "$units[$m{unit}][1]にｸﾗｽﾁｪﾝｼﾞしました<br>";

		if ($m{medal} > 0) {
			my $v = $m{medal} * $exchange_money;
			$m{money} += $v;
			$mes .= "残りの勲章$m{medal}個を献上して $v Gをもらいました<br>";
			$m{medal} = 0;
		}
	}
	&begin;
}


1; # 削除不可
