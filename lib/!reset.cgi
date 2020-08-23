#================================================
# 国ﾘｾｯﾄ Created by Merino
#================================================

# 統一難易度：[難しい 60 ～ 40 簡単]
my $game_lv = int( rand(11) + 45 );

# 統一期限(日)
my $limit_touitu_day = int( rand(6)+10 );


#================================================
# 期日が過ぎた場合
#================================================
sub time_limit  {
	&write_world_news("<b>$world_name大陸を統一する者は現れませんでした</b>");
	&write_legend('touitu', "$world_name大陸を統一する者は現れませんでした");
	$w{win_countries} = '';

	$w{world} = int(rand($#world_states)) unless $w{year} =~ /6$/; # 暗黒時代のﾘｾｯﾄは情勢を変更しない(暗黒解除するために情勢はそのまま)
	&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>") unless $w{year} =~ /5$/;
	&reset;
	
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

	&write_cs;
}

#================================================
# 国ﾃﾞｰﾀﾘｾｯﾄ処理
#================================================
sub reset {
	# 世界情勢 暗黒解除
	if ($w{year} =~ /6$/) {
		require './lib/vs_npc.cgi';
		&delete_npc_country;
		$w{world} = int(rand($#world_states));
	}

	# 仕官できる人数
	my $ave_c = int($w{player} / $w{country}) + 2;
	
	# set world
	$w{year}++;
	$w{game_lv} = $game_lv;
	$w{reset_time} = $time + 3600 * 24;
	$w{limit_time} = $time + 3600 * 24 * $limit_touitu_day;

	my($c1, $c2) = split /,/, $w{win_countries};

	# set countries
	for my $i (1 .. $w{country}) {
		# 統一国の場合はNPC弱体
		$cs{strong}[$i]   = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(6) + 10) * 1000;
		$cs{food}[$i]     = int(rand(30) + 5) * 1000;
		$cs{money}[$i]    = int(rand(30) + 5) * 1000;
		$cs{soldier}[$i]  = int(rand(30) + 5) * 1000;
		$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
		$cs{capacity}[$i] = $ave_c;
		$cs{is_die}[$i]   = 0;
		
		for my $j ($i+1 .. $w{country}) {
			$w{ "f_${i}_${j}" } = int(rand(40));
			$w{ "p_${i}_${j}" } = 0;
		}
		
		if ($w{year} % $reset_ceo_cycle_year == 0) {
			$cs{old_ceo}[$i] = $cs{ceo}[$i];
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}
	
	if ($w{year} % $reset_ceo_cycle_year == 0) {
		&write_world_news("<b>各国の$e2j{ceo}の任期が満了となりました</b>");
	}
	
	# 世界情勢 暗黒突入
	if ($w{year} =~ /6$/) {
		require './lib/vs_npc.cgi';
		&add_npc_country;
	}
}




1; # 削除不可
