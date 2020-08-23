#================================================
# ﾇﾒﾛﾝ
#================================================
use bignum;
require './lib/_casino_funcs.cgi'; # ｺﾒﾝﾄ参照

$header_size = 4; # ﾊﾞｶﾗ用のﾍｯﾀﾞｰｻｲｽﾞ
# 親、ﾊﾞﾝｶｰ手札、ﾌﾟﾚｲﾔｰ手札、デッキ
($_leader, $_b_cards, $_p_cards, $_deck) = ($_header_size .. $_header_size + $header_size - 1); # ﾍｯﾀﾞｰ配列のｲﾝﾃﾞｯｸｽ
$coin_lack = 0; # 0 ｺｲﾝがﾚｰﾄに足りないと参加できない 1 ｺｲﾝがﾚｰﾄに足りなくても参加できる
$min_entry = 2; # 最低2人
$max_entry = 10; # 最高2人


my @nums = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K');
my @suits = $is_mobile ? ('S', 'H', 'C', 'D') : ('&#9824;', '&#9825;', '&#9827;', '&#9826;');
my @targets = ('ﾌﾟﾚｲﾔｰに', 'ﾊﾞﾝｶｰに', 'ﾀｲに');

my $max_bet = 200000; # 0.5倍されるので実際の倍の値
my @pers = (0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5);

sub run {
	&_default_run;
}

#================================================
# ｹﾞｰﾑ画面に表示される情報の定義
#================================================
sub show_game_info { # 親やﾍﾞｯﾄ額などの表示 参加者より前に表示される
	my ($m_turn, $m_value, $m_stock, @head) = @_;
#	print qq|ﾍﾞｯﾄｺｲﾝ:$head[$_rate]|;
#	my @deck = &shuffled_deck(6);
#	my $cards = 0;
#	$cards = ($cards << 6) + $deck[$_] for (0..$#deck);
#	print qq|$cards<br>|;
#	for my $i (0..$#deck) {
#		print qq|$deck[$i]<br>|;
#	}
}
#sub show_start_info { # 募集中のｹﾞｰﾑに参加しているﾌﾟﾚｲﾔｰに表示したい情報 _start_game_form の上に表示される 定義してなくても動作に問題ない
#	my ($m_turn, $m_value, $m_stock, @head) = @_;
#}
sub show_started_game { # 始まっているｹﾞｰﾑの表示 参加者かそうでないかは is_member で判別し切り替える
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants], $head[$_participants_datas], $head[$_rate] ne '', $head[$_leader]) if &is_member($head[$_participants], "$m{name}"); # ｹﾞｰﾑに参加している
}
sub show_tale_info { # 定義してなくても動作に問題ない
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&show_status($head[$_participants_datas]) if $head[$_participants];
}

#================================================
# 参加するﾌｫｰﾑ
#================================================
sub participate_form {
	my ($leader) = @_;
	my $button = $leader ? "参加する" : "親になる";
	# ｶｼﾞﾉ毎の処理
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_submit("participate", "$button");
	print qq|</form>|;
#	$m{coin} = 1500000;
#	&write_user;
}

#================================================
# 参加する処理 ﾚｰﾄのためのﾜﾝｸｯｼｮﾝ
#================================================
sub participate {
	&_participate('', '', $m{coin}); # my ($in_rate, $m_value, $m_stock, @tmp_head) = @_;
}

#================================================
# 開始する処理 実際のファイル操作は _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ﾍｯﾀﾞｰ
	my @participants = split /,/, $head[$_participants];
	my $is_start = 0;
	# ｶｼﾞﾉ毎の処理
	my @deck = &shuffled_deck(6);
	my $cards = 0;
	$cards = ($cards << 6) + $deck[$_] for (0..$#deck);

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # 参加者が必要十分、ｹﾞｰﾑ開始前なら
		($is_start, $head[$_state], $head[$_lastupdate]) = (1, 1, $time);
		# ｶｼﾞﾉ毎の処理
		$head[$_leader] = $participants[0];
		$head[$_deck] = $cards;
		$$head_line = &h_to_s(@head);
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			($mtime, $mturn) = ($time, 2);
			# ｶｼﾞﾉ毎の処理

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
}

#================================================
# ﾌﾟﾚｲのﾌｫｰﾑ 基本ｶｼﾞﾉ毎に丸々書き換える必要がある
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants, $participants_datas, $is_bet, $leader) = @_;

	my $is_all_bet = 1; # 子全員のﾍﾞｯﾄ状態
	my $is_bet = 0; # 自分のﾍﾞｯﾄ状態
	my @participants = &get_members($participants);
	my @participants_datas = split /;/, $participants_datas;
	my $leader_coin = 0;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		if ($datas[0] eq $leader) { # 親のﾍﾞｯﾄは考慮せず、所持ｺｲﾝを取得する
			$leader_coin = $datas[2]; # 親の所持ｺｲﾝ
			next;
		}
		$is_all_bet = 0 if $datas[1] eq ''; # 誰かがﾍﾞｯﾄしてない
		$is_bet = 1 if $m{name} eq $datas[0] && $datas[1] ne ''; # 自分はすでにﾍﾞｯﾄしている
	}

	my $is_leader = $participants[0] eq $m{name}; # 親であるか
	if ( (!$is_all_bet && $is_leader) || $is_bet) { # 親が子のﾍﾞｯﾃｨﾝｸﾞを待ってるか、すでにﾍﾞｯﾃｨﾝｸﾞしている子
		print qq|<br>子のﾍﾞｯﾃｨﾝｸﾞを待っています<br>|;
		return;
	}

	if ($is_leader) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("deal", "配る");
		print qq|</form>|;
	}
	else {
		my @bet_coins = ();
		my $member_c = @participants - 1;
		my $size = length($leader_coin) - 1;
		my $leader_max_bet = (substr($leader_coin, 0, 1) . '0' x $size) / $member_c;
		@bet_coins = &get_bet_coins($leader_max_bet);

		print qq|<form method="$method" action="$this_script" name="form">|;
		print "ﾍﾞｯﾄ：".&create_select_menu("bet", 0, @bet_coins)."<br>";
		print "対象：".&create_select_menu("target", 0, @targets);
		print &create_submit("play", "賭ける");
		print qq|</form>|;
	}
}

#================================================
# ﾌﾟﾚｲの処理
#================================================
sub play {
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my @participants = split /,/, $head[$_participants];
	my $is_member = &is_member($head[$_participants], $m{name});

	unless ($is_member) {
		close $fh;
		return;
	}

	my @participants_datas = split /;/, $head[$_participants_datas];
	my $leader_coin = 0;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		if ($datas[0] eq $head[$_leader]) { # 親のﾍﾞｯﾄは考慮せず、所持ｺｲﾝを取得する
			$leader_coin = $datas[2]; # 親の所持ｺｲﾝ
			last;
		}
	}
	my @bet_coins = &get_bet_coins($leader_coin);

	my %sames = ();
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		# 親じゃなく、ﾍﾞｯﾄもしてないなら処理
		if ($head[$_leader] ne $mname && $is_member && $mname eq $m{name} && 2 <= $mturn && $mvalue eq '') {
			$mtime = $time;
			$mvalue = $in{target};
			$mstock = $bet_coins[$in{bet}];
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return "$targets[$in{target}] $bet_coins[$in{bet}] ｺｲﾝ 賭けました";
}

#================================================
# ﾌﾟﾚｲの処理2
#================================================
sub deal {
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my @participants = split /,/, $head[$_participants];

	my $is_all_bet = 1; # 子全員のﾍﾞｯﾄ状態
	my @participants_datas = split /;/, $head[$_participants_datas];
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		next if $datas[0] eq $participants[0]; # 親のﾍﾞｯﾄは考慮しない
		$is_all_bet = 0 if $datas[2] eq ''; # 誰かがﾍﾞｯﾄしてない
		last unless $is_all_bet;
	}
	unless ($is_all_bet) {
		close $fh;
		return;
	}

	my @p_cards = ();
	my @b_cards = ();
	for my $i (0 .. 1) {
		push @p_cards, $head[$_deck] & 63;
		$head[$_deck] >>= 6;

		push @b_cards, $head[$_deck] & 63;
		$head[$_deck] >>= 6;
	}

	my @points = (&calc(@p_cards), &calc(@b_cards));
	my @is_hit = (0, 0);
	if ($points[0] < 8 && $points[1] < 8) { # Player と Banker どちらも 8 9 じゃないならﾁｬｰﾄ（どちらかが 8 9 ならﾁｬｰﾄ飛ばして勝負）
		if ($points[0] < 6) { # 0～5 Hit
			push @p_cards, $head[$_deck] & 63;
			$head[$_deck] >>= 6;
			$is_hit[0] = 1;
		}

		if ($points[1] < 3 || (!$is_hit[0] && $points[1] < 7) ) { # 0～2 か 3～6 で Player が3枚目を引いてないなら Hit
			push @b_cards, $head[$_deck] & 63;
			$head[$_deck] >>= 6;
			$is_hit[1] = 1;
		}
		elsif (2 < $points[1] && $points[1] < 7 && $is_hit[0]) { # 4～6 で Player が3枚目を引いている
			my $p_3_pt = &calc($p_cards[2]); # Player の3枚目のﾎﾟｲﾝﾄ
			if (	($points[1] == 3 && $p_3_pt != 8) # 3 Player の3枚目が 8 じゃないなら Hit
				||	($points[1] == 4 && $p_3_pt != 0 && $p_3_pt != 1 && $p_3_pt != 8 && $p_3_pt != 9) # 4 Player の3枚目が 0 1 8 9 じゃないなら Hit
				||	($points[1] == 5 && ($p_3_pt == 4 || $p_3_pt == 5 || $p_3_pt == 6 || $p_3_pt == 7)) # 5 Player の3枚目が 4 5 6 7 なら Hit
				||	($points[1] == 6 && ($p_3_pt == 6 || $p_3_pt == 7))) { # 6 Player の3枚目が 6 7 なら Hit
				push @b_cards, $head[$_deck] & 63;
				$head[$_deck] >>= 6;
				$is_hit[1] = 1;
			}
		}

		@points = (&calc(@p_cards), &calc(@b_cards));
	}

	my $result = $points[1] < $points[0] ?		0	# Tie
				  : $points[0] < $points[1] ?		1	# Player勝利
				  :										2;	# Banker勝利

	my %sames = ();
	my @members = ();
	my @winners = ();
	my @win_bets = ();
	my @losers = ();
	my @lose_bets = ();
	my @leader = ();
	my @game_members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次
		if ($participants[0] eq $mname) {
			$mtime = $time;
			@leader = ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock);
			next;
		}

		my $is_find = 0;
		for my $participant (@participants) {
			if ($participant eq $mname && 2 <= $mturn) {
				push @game_members, $mname;
				$is_find = 1;
				last;
			}
		}
		# 参加者なら処理
		if ($is_find) {
			if ($mvalue == $result) {
				push @winners, $mname;
				push @win_bets, $mstock;
			}
			else {
				push @losers, $mname;
				push @lose_bets, $mstock;
			}
			$mtime = $time;
			$mvalue = $mstock = '';
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	for $i (0 .. $#winners) {
		my $v = 0;
		$v = $result == 0 ? $win_bets[$i] * 1 # Player勝利 配当1倍
			: $result == 1 ? int($win_bets[$i] * 0.95) # Banker勝利  配当0.95倍
			:					  $win_bets[$i] * 8; # Tie 配当8倍
		$leader[5] = ($leader[5] - $v) < 0 ? 0 : $leader[5] - $v;
	}
	if ($result != 2) {
		for $i (0 .. $#losers) {
			my $v = $lose_bets[$i];
			$leader[5] = 2500000 < ($leader[5] + $v) ? 2500000 : $leader[5] + $v;
		}
	}
	unshift @members, "$time<>$leader[1]<>$leader[2]<>$leader[3]<>$leader[4]<>$leader[5]<>\n"; # leader

	my $leader = $head[$_leader];
	if (4 <= $m{c_turn}) {
		&init_header(\@head);
		&reset_members(\@members);
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $result_mes = 'Player：';
	for my $i (0 .. $#p_cards) {
		my ($num, $suit) = &get_card($p_cards[$i]);
		$result_mes .= "$suits[$suit]$nums[$num]";
		$result_mes .= ' ' if $i < $#p_cards;
	}
	$result_mes .= "($points[0]) Banker：";

	for my $i (0 .. $#b_cards) {
		my ($num, $suit) = &get_card($b_cards[$i]);
		$result_mes .= "$suits[$suit]$nums[$num]";
		$result_mes .= ' ' if $i < $#b_cards;
	}
	$result_mes .= "($points[1])";

	my $total_v = 0;
	for $i (0 .. $#winners) {
		my $v = 0;
		$v = $result == 0 ? $win_bets[$i] * 1 # Player勝利 配当1倍
			: $result == 1 ? int($win_bets[$i] * 0.95) # Banker勝利  配当0.95倍
			:					  $win_bets[$i] * 8; # Tie 配当8倍
		my $vv = &coin_move($v, $winners[$i], 1);
		&coin_move(-1 * $vv, $leader, 1);
		$total_v -= $v;
		$result_mes .= "<br>$winners[$i] は $v ｺｲﾝ 勝ちました";
#		$result_mes .= '<br>' if $i < $#winners;
	}

	if ($result != 2) {
		for $i (0 .. $#losers) {
			my $v = $lose_bets[$i];
			my $vv = &coin_move(-1 * $v, $losers[$i], 1);
			&coin_move(-1 * $vv, $leader, 1);
			$total_v += $v;
			$result_mes .= "<br>$losers[$i] は $v ｺｲﾝ 負けました";
		}
	}
	else { # Tie を外しても総取りにならずﾍﾞｯﾄ戻ってくる
		for $i (0 .. $#losers) {
			my $v = $lose_bets[$i];
			$result_mes .= "<br>$losers[$i] は $v ｺｲﾝ の払い戻しです";
		}
	}

	$result_mes .= "<br>$leader は $total_v ｺｲﾝ 得ました";

	$m{c_turn}++;
	if (5 <= $m{c_turn}) {
		$m{c_turn} = 0;

		for my $game_member (@game_members) {
			&regist_you_data($game_member, 'c_turn', '0');
		}
	}
	&write_user;

	return $result_mes;
}

sub show_status {
	my @participants_datas = split /;/, shift;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
			print "$datas[0]($datas[2]ｺｲﾝ)";
			print "<br>" if $i != $#participants_datas;
	}
}

sub shuffled_deck {
	my $deck_n = shift; # ﾃﾞｯｸ数
	my $size = 52; # ｶｰﾄﾞ枚数
	my @deck = ();
	for my $i (0..$deck_n) {
		push @deck, $_ for (1 ..$size);
	}
	for my $i (0 .. $#deck) {
		my $j = int(rand($i + 1)); # 周回する度に乱数範囲を広げる
		my $temp = $deck[$i];
		$deck[$i] = $deck[$j];
		$deck[$j] = $temp;
	}
	return @deck;
}

sub get_card {
	my $card = shift;
	my $num = ($card-1) % 13; # 1～52 の値から -1 したものを 13 で割った余りが 0～12 になる
	my $suit = int(($card-1)/13); # 0ｽﾍﾟｰﾄﾞ 1ﾊｰﾄ 2ｸﾗﾌﾞ 3ﾀﾞｲﾔ
	return ($num, $suit);
}

sub calc {
	my @cards = @_;
	my $tmp_pt = 0;
	my $pt = 0;
	for my $i (0 .. $#cards) {
		$tmp_pt = (($cards[$i]-1) % 13) + 1; # 1～13
		if ($tmp_pt < 10) {
			$pt += $tmp_pt;
		}
	}
	return substr($pt, -1);
}

sub get_bet_coins {
	my $bet = $max_bet < $_[0] ? $max_bet : $_[0];
	my @bet_coins = ();
	for my $i (0..$#pers) {
		my $v = int($bet * $pers[$i]);
		push @bet_coins, $v if $v <= $m{coin};
	}
	return @bet_coins;
}

1;#削除不可