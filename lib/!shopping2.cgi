#================================================
# �����ݸ�2 Created by Merino
#================================================

# �ƭ� ���ǉ�/�ύX/�폜/���בւ��\
my @menus = (
	['�߂�', 		'main'],
	['�O���߰��',	'shopping'],
	['�]�E���K',	'shopping_job_change'],
	['�b�艮',		'shopping_smith'],
	['��̐_�a',	'shopping_unit_exchange'],
	['��ýĉ��',	'shopping_contest'],
	['�󂭂���',	'shopping_lot'],
	['�������k��',	'shopping_marriage'],
	['�ŋ��Z',		'shopping_finance'],
);

#================================================
sub begin {
	$mes .= '�ǂ��ɍs���܂���?<br>';
	&menu(map { $_->[0] } @menus);
}
sub tp_1  { &b_menu(@menus); }



1; # �폜�s��
