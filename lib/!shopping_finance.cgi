#================================================
# 闇金融 Created by Merino
#================================================

# 借りれる金額
my $fall_money = $m{sedai} > 20 ? 200000 : $m{sedai} * 10000;

# 利子
my $interest = 1.3;


#================================================
sub begin {
	if ($m{shogo} eq $shogos[1][0]) {
		my $v = int($fall_money * $interest);
		$mes .= "$v Gきっちり利子もそろえて、はよ返さんかい!";
		&menu('逃げる','返済する');
	}
	else {
		$mes .= 'いらっしゃいませ、お金にお困りですか?<br>';
		$mes .= 'お貸しできる金額は世代を重ねるほど多くお貸しできます<br>';
		$mes .= "$m{name}様は $m{sedai} 世代目ですので $fall_money Gお貸しすることができます<br>";
		&menu('やめる', '借りる');
	}
}

sub tp_1 {
	return if &is_ng_cmd(1);
	
	if ($m{shogo} eq $shogos[1][0]) {
		my $v = int($fall_money * $interest);
		if ($m{money} >= $v) {
			$m{money} -= $v;
			$m{shogo} = '';
			$mes .= 'ご利用は計画的にね!<br>';
		}
		else {
			$mes .= 'おいっ!金が足りないぞ!<br>';
			$mes .= "$m{name} は逃げるように立ち去った…<br>";
		}
	}
	else {
		$m{shogo} = $shogos[1][0];
		$m{money} += $fall_money;
		$mes .= "$fall_money G確かにお貸ししました<br>";
		$mes .= "お貸しした分はきちんと返済してくださいね<br>";
	}
	
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}



1; # 削除不可
