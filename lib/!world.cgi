sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
#================================================
# 世界情勢 Created by Merino
#================================================

#================================================
# 選択画面
#================================================
sub tp_100 {
	$mes .= "あなたはこの世界に何を求めますか?<br>";
	&menu('皆が望むもの','希望','絶望','平和');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};

	if ($cmd eq '1') { # 希望
		&mes_and_world_news("<b>世界に希望を望みました</b>", 1);
		$w{world} = int(rand(8)+1);
	}
	elsif ($cmd eq '2') { # 絶望
		&mes_and_world_news("<b>世界に絶望を望みました</b>", 1);
		$w{world} = int(rand(9)+9);
	}
	elsif ($cmd eq '3') { # 平和
		&mes_and_world_news("<b>世界に平和を望みました</b>", 1);
		$w{world} = 0;
	}
	else {
		&mes_and_world_news('<b>世界にみなが望むものを望みました</b>', 1);
		$w{world} = int(rand(@world_states-1));
	}

	# 強制暗黒期
	if ($old_world eq $#world_states) {
		$w{world} = $#world_states;
		&write_world_news("<i>$m{name}の願いはかき消されました</i>");
	}
	# 同じのじゃつまらないので
	elsif ($w{world} eq $old_world) {
		$w{world} = int(rand(@world_states-1));
		++$w{world} if $w{world} eq $old_world;
		$w{world} = int(rand(10)) if $w{world} > $#world_states-1;
		&write_world_news("<i>世界は $world_states[$old_world] となりま…せん $world_states[$w{world}]となりました</i>");
	}
	else {
		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
	}
	
	if ($w{world} eq '0') { # 平和
		$w{reset_time} += 3600 * 24 * 2;
	}
	elsif ($w{world} eq '7') { # 結束
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			push @win_cs, [$i, $cs{win_c}[$i]];
		}
		@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;
		
		# 奇数の場合は一番国は除く
		shift @win_cs if @win_cs % 2 == 1;
		
		my $half_c = int(@win_cs*0.5-1);
		for my $i (0 .. $half_c) {
			my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
			$w{'p_'.$c_c} = 1;
		}
	}
	
	&refresh;
	&n_menu;
	&write_cs;
}



1; # 削除不可
