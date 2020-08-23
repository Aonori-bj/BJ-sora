require './lib/move_player.cgi';
#=================================================
# 仕官 Created by Merino
#=================================================

# 拘束時間
$GWT *= 2;

# 仕官するのに必要なﾚﾍﾞﾙ
my $need_lv = 1;

# 仕官するのに必要な金額
my $need_money = $m{sedai} > 10 ? $rank_sols[$m{rank}]+30000 : $rank_sols[$m{rank}]+$m{sedai}*3000;

# 世界情勢が暗黒の場合、NPC国へ仕官するのに必要な金額
my $need_money_npc = 300000;


#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]は仕官することができません<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{lv} < $need_lv) {
		$mes .= "仕官するには $need_lv ﾚﾍﾞﾙ以上必要です<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{country}) {
		$mes .= "仕官する手続きとして$GWT分かかります<br>";
		$mes .= "他の国に仕官すると代表\者ﾎﾟｲﾝﾄと階級が下がります<br>";
		$mes .= "同盟国に仕官する場合は階級が下がりません<br>" if $union;
		$mes .= "移籍料として $need_money G支払う必要があります<br>";
		
		# 暗黒
		if ($w{world} eq $#world_states) {
			$mes .= qq|<font color="#FF0000">$cs{name}[$w{country}]に仕官する場合は、次の年になるまで他の国に仕官することはできません<br>|;
			$mes .= qq|$cs{name}[$w{country}]に仕官する場合は、代表\ﾎﾟｲﾝﾄが 0 になり、$need_money_npc G支払う必要があります<br></font>|;
		}
		
		$mes .= 'どの国に仕官しますか?<br>';
		
		&menu('やめる', @countries, '放浪する');
	}
	else {
		$mes .= 'どの国に仕官しますか?<br>';
		&menu('やめる', @countries);
	}
}
sub tp_1 {
	return if &is_ng_cmd(1 .. $w{country}+1);
	
	if ($cmd eq $m{country}) {
		$mes .= "自国に仕官はできません<br>";
		&begin;
	}
	# 国→放浪
	elsif ($cmd == $w{country} + 1) {
		 # 立候補者
		if ($m{name} eq $m{vote}) {
			$mes .= "$c_mの$e2j{ceo}の立候補を辞任する必要があります<br>";
			&begin;
			return;
		}

		&move_player($m{name}, $m{country}, 0);
		$m{country} = 0;
		$m{rank} = 0;
		$m{rank_exp} = 0;
		
		&mes_and_world_news("$c_mから立ち去り放浪の旅に出ました",1);
		
		# 代表ﾎﾟｲﾝﾄ0
		for my $k (qw/war dom mil pro/) {
			$m{$k.'_c'} = 0;
		}

		$mes .= "次に行動できるのは$GWT分後です<br>";
		&refresh;
		&wait;
	}
	elsif ($cs{member}[$cmd] >= $cs{capacity}[$cmd]) {
		$mes .= "$cs{name}[$cmd]は定員がいっぱいです<br>";
		&begin;
	}
	elsif (defined $cs{name}[$cmd]) { # 国が存在する
		# 国→他の国
		if ($m{country}) {
			# 君主
			if ($m{name} eq $cs{ceo}[$m{country}]) {
				$mes .= "$c_mの$e2j{ceo}を辞任する必要があります<br>";
				&begin;
				return;
			}
			elsif ($need_money > $m{money}) {
				$mes .= "移籍するには $need_money G必要です<br>";
				&begin;
				return;
			}
			# 暗黒
			elsif ($w{world} eq $#world_states) {
				if ($m{country} eq $w{country}) {
					$mes .= "$cs{name}[$m{country}]から抜け出すことは許されません<br>";
					&begin;
					return;
				}
				elsif ($cmd eq $w{country}) {
					require './lib/vs_npc.cgi';
					if ($need_money_npc > $m{money}) {
						$mes .= "悪魔と契約するには $need_money_npc G必要です<br>";
						&begin;
						return;
					}
					elsif (!&is_move_npc_country) {
						&begin;
						return;
					}
					$need_money = $need_money_npc;
				}
			}
			
			$m{money} -= $need_money;
			$cs{money}[$m{country}] += $need_money;
			$mes .= "移籍料として $need_money G支払いました<br>";
			
			unless ($union eq $cmd) {
				$m{rank} -= $m{rank} > 10 ? 2 : 1;
				$m{rank} = 1 if $m{rank} < 1;
				$mes .= "階級が$ranks[$m{rank}]になりました<br>";

				# 代表ﾎﾟｲﾝﾄ半分
				for my $k (qw/war dom mil pro/) {
					$m{$k.'_c'} = int($m{$k.'_c'} * 0.5);
				}
			}
			
			$mes .= "移籍の手続きに$GWT分かかります<br>" ;
			&wait;
		}
		# 無所属→国
		else {
			$m{rank} = 1 if $m{rank} < 1;
			&n_menu;
		}
		
		&move_player($m{name}, $m{country}, $cmd);
		$m{next_salary} = $time + 3600 * $salary_hour;
		$m{country} = $cmd;
		$m{vote} = '';
		
		&mes_and_world_news("$cs{name}[$cmd]に仕官しました",1);
		
		&refresh;
	}
	else {
		&begin;
	}
}




1; # 削除不可
