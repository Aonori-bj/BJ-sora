$mes .= qq|ｺｲﾝ $m{coin} 枚<br>| if $is_mobile;
#================================================
# ｶｼﾞﾉ Created by Merino
#================================================
# @m…mark @o…ozz の意味

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]の方は出入り禁止です<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # 疲労している場合は行えない
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かやっちゃう?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "いらっしゃ〜い♪ｼﾞｬﾝｼﾞｬﾝ遊んでいってね<br>";
	}
	
	&menu('やめる','$1ｽﾛｯﾄ','$10ｽﾛｯﾄ','$100ｽﾛｯﾄ','ﾊｲﾛｳ','ﾄﾞｯﾍﾟﾙ');
}

sub tp_1 {
	return if &is_ng_cmd(1..5);
	
	$m{tp} = $cmd * 100;
	&menu('Play!', 'やめる');
	$m{stock} = 0;
	$m{value} = '';

	if    ($cmd eq '1') { $mes .= 'ここは$1ｽﾛｯﾄです<br>'; }
	elsif ($cmd eq '2') { $mes .= 'ここは$10ｽﾛｯﾄです<br>'; }
	elsif ($cmd eq '3') { $mes .= 'ここは$100ｽﾛｯﾄです<br>'; }
	elsif ($cmd eq '4') {
		$mes .= 'ﾊｲﾛｳへようこそ!<br>';
		$mes .= '前のｶｰﾄﾞより大きいか小さいかを当てるｹﾞｰﾑです<br>';
		$mes .= '同じｶｰﾄﾞの場合は負けですので注意してくださいね<br>';
		$mes .= '一回10ｺｲﾝです<br>';
	}
	elsif ($cmd eq '5') { # ﾄﾞｯﾍﾟﾙ
		$mes .= 'ﾄﾞｯﾍﾟﾙへようこそ!<br>';
		$mes .= '3枚のｶｰﾄﾞの中から、ﾃﾞｨｰﾗｰが引いたｶｰﾄﾞと同じｶｰﾄﾞを引けば勝ちです<br>';
		$mes .= '一回10ｺｲﾝです<br>';
	}
	else {
		&refresh;
		&n_menu;
	}
}


#=================================================
# ｽﾛｯﾄ
#=================================================
sub tp_100 { &_slot(1) }
sub tp_200 { &_slot(10) }
sub tp_300 { &_slot(100) }
sub _slot {
	my $bet = shift;
	
	if ($cmd eq '0') {
		if ($m{coin} >= $bet) {
			my @m = ('∞','♪','†','★','７');
			my @o = (5,10, 15,  20,  30,  50); # ｵｯｽﾞ 一番左はﾁｪﾘｰが2つそろいのとき
			my @s = ();
			$s[$_] = int(rand(@m)) for (0 .. 2);
			$mes .= "[\$$betｽﾛｯﾄ]<br>";
			$mes .= "<p>【$m[$s[0]]】【$m[$s[1]]】【$m[$s[2]]】</p>";
			$m{coin} -= $bet;
			
			if ($s[0] == $s[1]) { # 1つ目と2つ目
				if ($s[1] == $s[2]) { # 2つ目と3つ目
					my $v = $bet * $o[$s[0]+1]; # +1 = ﾁｪﾘｰ2そろい
					$m{coin} += $v;
					$mes .= "なんと!! $m[$s[0]] が3つそろいました!!<br>";
					$mes .= 'おめでとうございます!!<br>';
					$mes .= "***** ｺｲﾝ $v 枚 GET !! *****<br>";
					&c_up('cas_c');
					&use_pet('casino');
				}
				elsif ($s[0] == 0) { # ﾁｪﾘｰのみ1つ目と2つ目がそろえばよい
					my $v = $bet * $o[0];
					$m{coin} += $v;
					$mes .= 'ﾁｪﾘｰが2つそろいました♪<br>';
					$mes .= "ｺｲﾝ $v 枚Up♪<br>";
					&c_up('cas_c');
					&use_pet('casino');
				}
				else {
					$mes .= '<p>ﾊｽﾞﾚ</p>';
					$m{act} += 1;
				}
			}
			else {
				$mes .= '<p>ﾊｽﾞﾚ</p>';
				$m{act} += 1;
			}
			$mes .= 'もう一度やりますか?';
			&menu('Play!', 'やめる');
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	else {
		&begin;
	}
}

#=================================================
# ﾊｲﾛｳ
#=================================================
sub tp_400 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # 低い順
			$m{value} = int(rand(@m)) if $m{value} eq '';
			$mes .= "【$m[$m{value}]】<br>次のｶｰﾄﾞは High(高い)? or Low(低い)?";
			&menu('High!(高い)','Low!(低い)');
			
			$m{tp} = 410;
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} がある場合は勝ち->やめるの選択
		$mes .= "ｺｲﾝ $m{stock} 枚を手に入れました!<br>";
		$m{coin} += $m{stock};
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_410 {
	my $stock_old = $m{value};
	my @m = ('2','3','4','5','6','7','8','9','10','J','Q','K','A','Jo'); # 低い順
	
	$m{value} = int(rand(@m));
	$mes .= "【$m[$stock_old]】-> 【$m[$m{value}]】<br>";

	if (   ($cmd eq '0' && $m{value} > $stock_old)     # 高い選択で高い時
		|| ($cmd eq '1' && $m{value} < $stock_old) ) { # 低い選択で低い時
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 2;
			$mes .= 'おめでとうございます!<br>';
			$mes .= "$m{stock}ｺｲﾝ Get!<br>";
			$mes .= '手に入れたｺｲﾝをそのまま次へと賭けることができます<br>';
			&menu('挑戦する','やめる');

			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # 負け
		$m{coin} -= 10;
		$m{stock} = 0;
		$m{value} = '';
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 6;
	}
	$m{tp} = 400;
}


#=================================================
# ﾄﾞｯﾍﾟﾙ
#=================================================
sub tp_500 {
	if ($cmd eq '0') {
		if ($m{coin} >= 10) {
			my @m = ('★','◆','▲');
			$m{value} = int(rand(@m));
			$mes .= "ﾃﾞｨｰﾗｰのｶｰﾄﾞ【$m[$m{value}]】<br>";
			$mes .= '<p>【□】【□】【□】</p><p>どのｶｰﾄﾞを選びますか?</p>';
	
			&menu('左','真ん中','右');
			$m{tp} = 510;
		}
		else {
			$mes .= 'ｺｲﾝが足りません<br>';
			&begin;
		}
	}
	elsif ($m{stock}) { # $m{stock} がある場合は勝ち->やめるの選択
		$mes .= "ｺｲﾝ $m{stock} 枚を手に入れました<br>";
		$m{coin} += $m{stock};
		&begin;
	}
	else {
		&begin;
	}
}
sub tp_510 {
	my @m = ('★','◆','▲');
	my @s = (0,1,2);
	my $a = int(rand(@m));
	
	$mes .= "ﾃﾞｨｰﾗｰのｶｰﾄﾞ【$m[$m{value}]】<br>";
	$mes .= "<p>【$m[$s[$a]]】【$m[$s[$a-1]]】【$m[$s[$a-2]]】</p>";
	
	if (   ($cmd eq '0' && $m[$m{value}] eq $m[$s[$a]])       # 左選択
		|| ($cmd eq '1' && $m[$m{value}] eq $m[$s[$a-1]])     # 真ん中選択
		|| ($cmd eq '2' && $m[$m{value}] eq $m[$s[$a-2]]) ) { # 右選択
		
			$m{stock} = 10 if $m{stock} == 0;
			$m{stock} *= 6;
			$mes .= 'おめでとうございます!<br>';
			$mes .= "ｺｲﾝ $m{stock} 枚 Get!<br>";
			$mes .= '手に入れたｺｲﾝをそのまま次へと賭けることができます<br>';
			&menu('挑戦する','やめる');
			&c_up('cas_c');
			&use_pet('casino');
	}
	else { # 負け
		$m{coin} -= 10;
		$m{stock} = $m{value} = 0;
		$mes .= '<p>残念でしたね。もう一度やりますか?</p>';
		&menu('Play!','やめる');
		$m{act} += 5;
	}
	$m{tp} = 500;
}



1; # 削除不可
