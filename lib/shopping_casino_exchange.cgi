$mes .= qq|ｺｲﾝ $m{coin} 枚<br>| if $is_mobile;
#================================================
# ｶｼﾞﾉ交換所 Created by Merino
#================================================

# 交換賞品
my @prizes = (
# 種類 1=武器,2=卵,3=ﾍﾟｯﾄ
#	[0]種類,[1]No,[2]ﾒﾀﾞﾙ
	[0,	0,	0,		],
	[2,	22,	1000,	],
	[2,	24,	3000,	],
	[2,	23,	5000,	],
	[1,	2,	10000,	],
	[1,	7,	10000,	],
	[1,	22,	10000,	],
	[2,	25,	20000,	],
	[2,	16,	30000,	],
	[3,	126,40000,	],
	[2,	3,	100000,	],
	[2,	2,	200000,	],
);


#================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]はお断りだ<br>";
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かありますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= 'ここは、手持ちのお金をｺｲﾝに交換したり<br>';
		$mes .= 'ｺｲﾝと賞品の交換をすることができます<br>';
		$mes .= 'どうしますか？<br>';
	}
	&menu('やめる','ｺｲﾝに交換','賞品と交換');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#=================================================
# お金→ｺｲﾝに交換
#=================================================
sub tp_100 {
	$layout = 1;

	$mes .= "$m{name}様はｺｲﾝを$m{coin}枚お持ちです<br>";
	$mes .= 'ｺｲﾝ1枚20Gです<br>いくらお求めですか?<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="coin" value="0" class="text_box1" style="text-align:right">枚|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="交換する" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	if ($in{coin} && $in{coin} !~ /[^0-9]/) {
		my $v = int($in{coin} * 20);
		if ($m{money} >= $v) {
			$m{money} -= $v;
			$m{coin}  += $in{coin};
			$mes .= "$v Gをｺｲﾝ $in{coin} 枚に交換しました<br>";
		}
		else {
			$mes .= 'お金が足りません<br>';
		}
	}
	&begin;
}


#=================================================
# ｺｲﾝ→賞品に交換
#=================================================
sub tp_200 {
	$layout = 1;

	$mes .= "$m{name}様はｺｲﾝを$m{coin}枚お持ちです<br>";
	$mes .= "どの賞品と交換しますか?<br>";

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>賞品</th><th>必要ｺｲﾝ<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked> やめる<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i"> |;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[卵]$eggs[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[ペ]$pets[ $prizes[$i][1] ][1]</td>|
			  ;
		$mes .= qq|<td align="right">$prizes[$i][2]ｺｲﾝ<br></td></tr>|;
	}
	$mes .= qq|</table><p><input type="submit" value="交換する" class="button1"></p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"></form>|;
	$m{tp} += 10;
}
sub tp_210 {
	if ($cmd) {
		for my $i (1 .. $#prizes) {
			next unless $cmd eq $i;

			if ($m{coin} >= $prizes[$i][2]) {
				$m{coin} -= $prizes[$i][2];

				if ($prizes[$i][0] eq '1') {
					$mes .= "$weas[ $prizes[$i][1] ][1]に交換しました<br>";
					&send_item($m{name}, $prizes[$i][0], $prizes[$i][1], $weas[ $prizes[$i][1] ][4]);
				}
				elsif ($prizes[$i][0] eq '2') {
					$mes .= "$eggs[ $prizes[$i][1] ][1]に交換しました<br>";
					&send_item($m{name}, $prizes[$i][0], $prizes[$i][1]);
				}
				elsif ($prizes[$i][0] eq '3') {
					$mes .= "$pets[ $prizes[$i][1] ][1]に交換しました<br>";
					&send_item($m{name}, $prizes[$i][0], $prizes[$i][1]);
				}
			}
			else {
				$mes .= 'ｺｲﾝが足りません<br>';
			}
			last;
		}
	}
	&begin;
}




1; # 削除不可
