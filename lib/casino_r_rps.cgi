#================================================
# ﾇﾒﾛﾝ
#================================================
require './lib/_casino_funcs.cgi'; # ｺﾒﾝﾄ参照

$header_size = 2; # 制限ｼﾞｬﾝｹﾝ用のﾍｯﾀﾞｰｻｲｽﾞ
($_field_card, $_cards) = ($_header_size .. $_header_size + $header_size - 1); # ﾍｯﾀﾞｰ配列のｲﾝﾃﾞｯｸｽ
$coin_lack = 0; # 0 ｺｲﾝがﾚｰﾄに足りないと参加できない 1 ｺｲﾝがﾚｰﾄに足りなくても参加できる
$min_entry = 2; # 最低2人
$max_entry = 2; # 最高2人

sub run {
	&_default_run;
}

#================================================
# ｹﾞｰﾑ画面に表示される情報の定義
#================================================
sub show_game_info { # 親やﾍﾞｯﾄ額などの表示 参加者より前に表示される
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|ﾍﾞｯﾄｺｲﾝ:$head[$_rate]|;
}
#sub show_start_info { # 募集中のｹﾞｰﾑに参加しているﾌﾟﾚｲﾔｰに表示したい情報 _start_game_form の上に表示される 定義してなくても動作に問題ない
#	my ($m_turn, $m_value, $m_stock, @head) = @_;
#}
sub show_started_game { # 始まっているｹﾞｰﾑの表示 参加者かそうでないかは is_member で判別し切り替える
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants], $head[$_participants_datas], $head[$_rate] ne '') if &is_member($head[$_participants], "$m{name}"); # ｹﾞｰﾑに参加している
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
}

#================================================
# 参加する処理 ﾚｰﾄのためのﾜﾝｸｯｼｮﾝ
#================================================
sub participate {
	&_participate('', $m{coin}, 0); # my ($in_rate, $m_value, $m_stock, @tmp_head) = @_;
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
	my @cards = (0..17);

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # 参加者が必要十分、ｹﾞｰﾑ開始前なら
		($is_start, $head[$_state], $head[$_lastupdate]) = (1, 1, $time);
		# ｶｼﾞﾉ毎の処理
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			($mtime, $mturn) = ($time, 2);
			# ｶｼﾞﾉ毎の処理
			my @m_cards = ();
			push @m_cards, splice(@cards, int(rand($#cards)), 1) for (0..2);
			$mstock = join(',', @m_cards);

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
	# ｶｼﾞﾉ毎の処理
	if ($is_start) {
		$head[$_cards] = join(',', @cards);
		$$head_line = &h_to_s(@head);
	}
}

#================================================
# ﾌﾟﾚｲのﾌｫｰﾑ 基本ｶｼﾞﾉ毎に丸々書き換える必要がある
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants, $participants_datas, $is_bet) = @_;
	unless (&is_my_turn($participants, $m{name})) {
		print qq|<br>相手が思考中です<br>|;
		return;
	}

	my @hand_cards = split /,/, $m_stock;
	my @hand_card_names = (); # 手札の名称を持つ配列
	push (@hand_card_names, &get_card_name($hand_cards[$_])) for (0 .. $#hand_cards);

	my @participants = &get_members($participants);
	my @participants_datas = split /;/, $participants_datas;
	my @coins = (); # 自分と相手の所持ｺｲﾝ
	unless ($is_bet) {
		for my $i (0 .. $#participants_datas) {
			my @datas = split /:/, $participants_datas[$i];
			$coins[ ($m{name} ne $datas[0]) ] = $datas[1];
		}
	}

	my $max_bet = $coins[0] < $coins[1] ? $coins[0] : $coins[1];
	my @bet_coins = (int($max_bet/20), int($max_bet/10), int($max_bet/8), int($max_bet/6), int($max_bet/4), int($max_bet/2));

	print qq|<form method="$method" action="$this_script" name="form">|;
	print "ﾍﾞｯﾄ：".&create_select_menu("bet", 0, @bet_coins)."<br>" unless $is_bet;
	print "手札：".&create_select_menu("card", 0, @hand_card_names);
	print &create_submit("play", "ｶｰﾄﾞを出す");
	print qq|</form>|;
}

#================================================
# ﾌﾟﾚｲの処理
#================================================
sub play {
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my $field_card = $head[$_field_card];
	my @cards = split /,/, $head[$_cards];
	my $is_crash = $head[$_field_card] ne '';
	my $is_bet = $head[$_rate] ne '';
	my @game_members = &get_members($head[$_participants]);
	my $is_my_turn = $head[$_state] && $game_members[0] eq $m{name} && 2 <= $m{c_turn};
	my @participants_datas = split /;/, $head[$_participants_datas];

	my $turn = 0;
	my @names = (); # 自分と相手の名前
	my @hand_cards = ();
	my @coins = (); # 自分と相手の所持ｺｲﾝ
	my @play_cards = ();
	my @m_new_cards = ();
	my @y_new_cards = ();

	my $result_str = '';
	my $result_coin = 0;
	if ($is_my_turn) { # 自分のﾀｰﾝの行動
		for my $i (0 .. $#participants_datas) {
			my @datas = split /:/, $participants_datas[$i];
			$names[ ($m{name} eq $datas[0]) ] = $datas[0]; # 後攻の行動で勝負するから eq で 1 にｱｸｾｽ
			$coins[ ($m{name} ne $datas[0]) ] = $datas[1]; # どっちでも良いけど 0 が自分、 1 が相手
			@hand_cards = split /,/, $datas[2] if $m{name} eq $datas[0];
		}

		$head[$_field_card] = splice(@hand_cards, $in{card}, 1);
		if ($is_bet) { # ﾍﾞｯﾄされている
			if ($is_crash) { # すでに相手がｶｰﾄﾞを出している
				@play_cards = ($field_card % 3, $head[$_field_card] % 3); # 相手と自分のｶｰﾄﾞを取得

				if ($play_cards[1] eq '0') {
					$result_str = $play_cards[0] eq '1' ? '勝ち'
									: $play_cards[0] eq '2' ? '負け'
									:								  'あいこ'
									;
				}
				elsif ($play_cards[1] eq '1') {
					$result_str = $play_cards[0] eq '2' ? '勝ち'
									: $play_cards[0] eq '0' ? '負け'
									:								  'あいこ'
									;
				}
				elsif ($play_cards[1] eq '2') {
					$result_str = $play_cards[0] eq '0' ? '勝ち'
									: $play_cards[0] eq '1' ? '負け'
									:								  'あいこ'
									;
				}

				if ($result_str ne 'あいこ' || @hand_cards == 0) { # あいこじゃないか、手札がなくなったら流し
					$result_coin = $head[$_rate];
					$head[$_rate] = '';
					push @m_new_cards, splice(@cards, int(rand($#cards)), 1) for (0..2);
					push @y_new_cards, splice(@cards, int(rand($#cards)), 1) for (0..2);
					$head[$_cards] = join(',', @cards);
				}
				$head[$_field_card] = '';
			}
			if ($result_str ne '負け') { # 負けじゃないならﾀｰﾝ交代イコール負けた方にﾍﾞｯﾄ権
				$head[$_participants] = &change_turn($head[$_participants]); # ﾀｰﾝ終了 1ﾀｰﾝで複数回行動するようなｹﾞｰﾑならｺﾒﾝﾄｱｳﾄし、最終的な行動で実行
			}
		}
		else { # ﾍﾞｯﾄされていない
			my $max_bet = $coins[0] < $coins[1] ? $coins[0] : $coins[1];
			my @bet_coins = (int($max_bet/20), int($max_bet/10), int($max_bet/8), int($max_bet/6), int($max_bet/4), int($max_bet/2));
			$head[$_rate] = $bet_coins[$in{bet}];
			$head[$_participants] = &change_turn($head[$_participants]); # ﾀｰﾝ終了 1ﾀｰﾝで複数回行動するようなｹﾞｰﾑならｺﾒﾝﾄｱｳﾄし、最終的な行動で実行
		}
	}

	my ($winner_coin, $loser_coin) = (0, 0);
	if ($is_my_turn && $is_bet && $is_crash && $result_str && $result_str ne 'あいこ') {
		# 所持ｺｲﾝの取得
		($winner_coin, $loser_coin) = $result_str eq '勝ち' ? ($coins[0], $coins[1]) : ($coins[1], $coins[0]);

		if (2500000 < ($winner_coin + $result_coin)) { # 所持ｺｲﾝ + 得るｺｲﾝ が 2500000 を超えるなら
			$result_coin = (2500000 - $winner_coin); # 得るｺｲﾝは 2500000 が限度
			$winner_coin = 2500000; # 所持ｺｲﾝは 2500000
			$loser_coin -= $result_coin;
		}
		else { # ｺｲﾝの移動で所持できるｺｲﾝの上限や下限に引っかからない
			$winner_coin += $result_coin;
			$loser_coin -= $result_coin;
		}
	}

	my %sames = ();
	my $is_find = 0;
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # 同じ人なら次

		if ($mname eq $game_members[0] && $is_my_turn) {
			$mtime = $time;
			if ($is_bet && $is_crash && (($result_str && $result_str ne 'あいこ') || @hand_cards == 0)) {
				if ($result_str && $result_str eq '勝ち') {
					$mvalue = $winner_coin;
				}
				elsif ($result_str && $result_str eq '負け') {
					$mvalue = $loser_coin;
				}
				$mstock = join(',', @m_new_cards);
			}
			else {
				$mstock = join(',', @hand_cards);
			}
			$is_find++;
		}
		elsif ($mname eq $game_members[1] && $is_my_turn) {
			if ($is_bet && $is_crash && (($result_str && $result_str ne 'あいこ') || @hand_cards == 0)) {
				if ($result_str && $result_str eq '勝ち') {
					$mvalue = $loser_coin;
				}
				elsif ($result_str && $result_str eq '負け') {
					$mvalue = $winner_coin;
				}
				$mstock = join(',', @y_new_cards);
				$mes .= "game_members 1 $mturn<br>";
			}
			$is_find++;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

#	if ($is_my_turn && $is_bet && $is_crash && $result_str && @cards == 0 && @hand_cards == 0 && @m_new_cards == 0) {
	if ($is_my_turn && $is_bet && $is_crash && @cards == 0 && $result_str && @m_new_cards == 0 && ( ($result_str ne 'あいこ' && @hand_cards < 3) || @hand_cards == 0)) {
#	if ($m{c_turn} == 5 && @m_new_cards == 0) {
		&init_header(\@head);
		&reset_members(\@members);
	}

	unshift @members, &h_to_s(@head); # ﾍｯﾀﾞｰ
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $result_mes = '';
	if ($is_my_turn && $is_bet && $is_crash && $result_str && $result_str ne 'あいこ') {
		if ($result_str eq '勝ち') {
			$m{coin} = $winner_coin;
			&write_user;
			&regist_you_data($game_members[1], 'coin', $loser_coin);
			$result_mes .= "<br>$game_members[0] は $result_coin ｺｲﾝ 勝ちました<br>";
			$result_mes .= "$game_members[1] は $result_coin ｺｲﾝ 負けました";
		}
		else {
			$m{coin} = $loser_coin;
			&write_user;
			&regist_you_data($game_members[1], 'coin', $winner_coin);
			$result_mes .= "<br>$game_members[1] は $result_coin ｺｲﾝ 勝ちました<br>";
			$result_mes .= "$game_members[0] は $result_coin ｺｲﾝ 負けました";
		}

	}

	# 終了処理
	# 自分のﾀｰﾝ、ﾍﾞｯﾄされてる、じゃんけんしてる、結果出てる、もうﾃﾞｯｸない、手札もない
	if ($is_my_turn && $is_bet && $is_crash && @cards == 0 && $result_str && @m_new_cards == 0 && ( ($result_str ne 'あいこ' && @hand_cards < 3) || @hand_cards == 0)) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 0;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '0');
			}
		}
	}

	if ($is_my_turn) {
		unless ($is_bet && $is_crash) {
			return 'じゃーんけーん！';
		}
		else {
			return "ポンっ！ $names[0](".&get_card_name($play_cards[0]).") vs $names[1](".&get_card_name($play_cards[1]).")$result_mes";
		}
	}
}

sub show_status {
	my @participants_datas = split /;/, shift;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
			print "$datas[0]($datas[1]ｺｲﾝ)";
			print "<br>" if $i != $#participants_datas;
	}
}

sub get_card_name {
	my $card = $_[0] % 3;
	return $card == 1 ? 'チョキ'
		  : $card == 2 ? 'パー'
							: 'グー';
}

1;#削除不可