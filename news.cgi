#!/usr/bin/perl
require 'config.cgi';
#================================================
# ﾆｭｰｽ表示 Created by Merino
#================================================

# 表示するもの(./log/にあるもの)　追加削除並べ替え可能
my @files = (
#	['ﾀｲﾄﾙ',		'ﾛｸﾞﾌｧｲﾙ名'],
	['過去の栄光',	'world_news',		],
	['世界情勢',	'world_big_news',	],
	['物流情報',	'send_news',		],
	['闘技場の軌跡','colosseum_news',	],
	['新着ﾌﾞﾛｸﾞ',	'blog_news',		],
	['新作絵画',	'picture_news',		],
	['新作本',		'book_news',		],
);

#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{no} ||= 0;
	$in{no} = 0 if $in{no} >= @files;

	if ($in{id} && $in{pass}) {
		print qq|<div style="margin-bottom: 14px;">|;
		print qq|<form method="$method" action="$script" style="display: inline;">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
		&show_wait;
		print qq|</div>|;
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="ＴＯＰ" class="button1"></form>|;
	}

	for my $i (0 .. $#files) {
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$files[$i][0]</a> / |;
	}

	print qq|<hr><h1>$files[$in{no}][0]</h1><hr>|;
	print qq|<font size="1">※画像が表\示されていないものは、その人のﾏｲﾋﾟｸﾁｬからなくなったものです</font><br>| if $files[$in{no}][1] eq 'picture_news';

	open my $fh, "< $logdir/$files[$in{no}][1].cgi" or &error("$logdir/$files[$in{no}][1].cgiﾌｧｲﾙが読み込めません");
	print qq|<li>$_</li><hr size="1">\n| while <$fh>;
	close $fh;
}

sub show_wait {
	&read_user;
#	my %p = get_you_datas($in{id}, 1);
	my $state = '';
	if ($m{lib} eq 'domestic') {
		if($m{tp} eq '110'){
			if($m{turn} eq '1'){
				$state = "小規模";
			}elsif($m{turn} eq '3'){
				$state = "大規模";
			}else{
				$state = "中規模";
			}
			$state .= "農業中です";
		}elsif($m{tp} eq '210'){
			if($m{turn} eq '1'){
				$state = "小規模";
			}elsif($m{turn} eq '3'){
				$state = "大規模";
			}else{
				$state = "中規模";
			}
			$state .= "商業中です";
		}elsif($m{tp} eq '310'){
			if($m{turn} eq '1'){
				$state = "小規模";
			}elsif($m{turn} eq '3'){
				$state = "大規模";
			}else{
				$state = "中規模";
			}
			$state .= "徴兵中です";
		}elsif($m{tp} eq '410'){
			if($m{turn} eq '1'){
				$state = "小規模";
			}elsif($m{turn} eq '3'){
				$state = "大規模";
			}elsif($m{turn} eq '4'){
				$state = "超規模";
			}else{
				$state = "中規模";
			}
			$state .= "長期内政中です";
		}
	}elsif($m{lib} eq 'military'){
		$state = "移動中です";
		if($m{tp} eq '110'){
			$state .= "(強奪)";
		}elsif($m{tp} eq '210'){
			$state .= "(諜報)";
		}elsif($m{tp} eq '310'){
			$state .= "(洗脳)";
		}elsif($m{tp} eq '410'){
			$state .= "(偵察)";
		}elsif($m{tp} eq '510'){
			$state .= "(偽計)";
		}elsif($m{tp} eq '610'){
			$state .= "(攻城)";
		}elsif($m{tp} eq '710'){
			if($m{value} eq 'military_ambush'){
				$state = "軍事";
			}else{
				$state = "進軍";
			}
			$state .= "待ち伏せ中です";
		}elsif($m{tp} eq '810'){
			$state .= "(長期強奪)";
		}elsif($m{tp} eq '910'){
			$state .= "(長期諜報)";
		}elsif($m{tp} eq '1010'){
			$state .= "(長期洗脳)";
		}
	}elsif($m{lib} eq 'prison'){
		$state = "$cs{prison_name}[$y{country}]で幽閉中です";
	}elsif($m{lib} eq 'promise'){
		$state = "移動中です";
		if($m{tp} eq '110'){
			$state .= "(友好)";
		}elsif($m{tp} eq '210'){
			$state .= "(停戦)";
		}elsif($m{tp} eq '310'){
			$state .= "(宣戦布告)";
		}elsif($m{tp} eq '410'){
			$state .= "(同盟交渉)";
		}elsif($m{tp} eq '510'){
			$state .= "(同盟破棄)";
		}elsif($m{tp} eq '610'){
			$state .= "(食料輸送)";
		}elsif($m{tp} eq '710'){
			$state .= "(資金輸送)";
		}elsif($m{tp} eq '810'){
			$state .= "(兵士輸送)";
		}
	}elsif($m{lib} eq 'war'){
		$state = "移動中です";
		if($m{value} eq '0.5'){
			$state .= "(少数進軍)";
		}elsif($m{value} eq '1'){
			$state .= "(進軍)";
		}elsif($m{value} eq '1.5'){
			$state .= "(長期遠征)";
		}
	}

	if ($state) {
		my $next_time_mes = sprintf("%d分%02d秒", int($m{wt} / 60), int($m{wt} % 60) );
		print qq| $state|;
		print qq| <span id="nokori_time">$next_time_mes</span>| if 0 < $m{wt};
	}
}
