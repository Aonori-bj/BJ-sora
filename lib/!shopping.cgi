#================================================
# �����ݸ� Created by Merino
#================================================

# �ƭ� ���ǉ�/�ύX/�폜/���בւ��\
my @menus = (
	['�߂�', 		'main'],
	['�����߰��',	'shopping2'],
	['���l�̂��X',	'shopping_akindo'],
	['���̉攌��',	'shopping_akindo_picture'],
	['�ޯ�ϰ���',	'shopping_akindo_book'],
	['���l�̋�s',	'shopping_akindo_bank'],
	['�����݉��',	'shopping_auction'],
	['�ެݸ�����',	'shopping_junk_shop'],
	['�����޶޽',	'shopping_casino'],
	['���Ɍ�����',	'shopping_casino_exchange'],
	['���Z��',		'shopping_colosseum'],
	['���\���a�@',	'shopping_hospital'],
);

#================================================
sub begin {
	$mes .= '�ǂ��ɍs���܂���?<br>';
	&menu(map { $_->[0] } @menus);
}
sub tp_1  { &b_menu(@menus); }



1; # �폜�s��
