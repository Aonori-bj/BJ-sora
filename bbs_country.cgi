#!/usr/bin/perl
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# ���f���� Created by Merino
#=================================================
&get_data;
#&error("$cs{name}[0]�̕��͂����p�ł��܂���") if $m{country} eq '0';
&error("�S�����͍���c���ɂ͓���܂���") if $m{lib} eq 'prison';

$this_title  = "$cs{name}[$m{country}]����c��";
$this_file   = "$logdir/$m{country}/bbs";
$this_script = 'bbs_country.cgi';

# ���̍��̐l�����������܂Ȃ��̂ŕ����F����̫�ĐF(�F�t�������ꍇ�́���s�폜)
$cs{color}[$m{country}] = $cs{color}[0];

#=================================================
&run;
&footer;
exit;