#================================================
# ｼｮｯﾋﾟﾝｸﾞ2 Created by Merino
#================================================

# ﾒﾆｭｰ ◎追加/変更/削除/並べ替え可能
my @menus = (
	['戻る', 		'main'],
	['前のﾍﾟｰｼﾞ',	'shopping'],
	['ﾊﾛｰﾜｰｸ',	'shopping_job_change'],
	['鍛冶屋',		'shopping_smith'],
	['謎の神殿',	'shopping_unit_exchange'],
	['ｺﾝﾃｽﾄ会場',	'shopping_contest'],
	['宝くじ屋',	'shopping_lot'],
#	['賽銭箱',	'shopping_offertory_box'],
	['結婚相談所',	'shopping_marriage'],
	['闇金融',		'shopping_finance'],
#	['星降りのほこら',	'shopping_mix'],
#	['道場',	'shopping_master'],
);

#================================================
sub begin {
	$mes .= 'どこに行きますか?<br>';
	&menu(map { $_->[0] } @menus);
}
sub tp_1  {
	return if &is_ng_cmd(1..$#menus);
	&b_menu(@menus);
}

1; # 削除不可
