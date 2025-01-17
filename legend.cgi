#!/usr/bin/perl
require 'config.cgi';
#================================================
# 石碑 Created by Merino
#================================================

# 表示するもの(./log/legend/にあるもの)　追加削除並べ替え可能
my @files = (
#	['ﾀｲﾄﾙ',				'ﾛｸﾞﾌｧｲﾙ名'],
	['歴代の大陸覇者',		'touitu'	],
	['†永遠の証†',		'comp_shogo'],
	['ｽｷﾙﾏｽﾀｰ',				'comp_skill'],
	['ｳｪﾎﾟﾝﾏｽﾀｰ',			'comp_wea'	],
	['ｴｯｸﾞﾏｽﾀｰ',			'comp_egg'	],
	['ﾍﾟｯﾄﾏｽﾀｰ',			'comp_pet'	],
	['ﾋﾟﾖﾋﾟﾖ歴代強王者',	'champ_0'	],
	['ﾋﾞｷﾞﾅｰ歴代強王者',	'champ_1'	],
	['ﾍﾞﾃﾗﾝ歴代強王者',		'champ_2'	],
	['ﾏｼﾞｼｬﾝ歴代強王者',	'champ_3'	],
	['ｿﾙｼﾞｬｰ歴代強王者',	'champ_4'	],
	['ﾁｬﾝﾋﾟｵﾝ歴代強王者',	'champ_5'	],
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
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="戻る" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index"><input type="submit" value="ＴＯＰ" class="button1"></form>|;
	}

	for my $i (0 .. $#files) {
		next unless -s "$logdir/legend/$files[$i][1].cgi";
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$files[$i][0]</a> / |;
	}

	print qq|<hr><h1>$files[$in{no}][0]</h1><hr>|;
	
	open my $fh, "< $logdir/legend/$files[$in{no}][1].cgi" or &error("$logdir/legend/$files[$in{no}][1].cgiﾌｧｲﾙが読み込めません");
	print qq|<li>$_</li><hr>\n| while <$fh>;
	close $fh;
}
