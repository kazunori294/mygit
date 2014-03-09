#!/usr/bin/perl

use Net::OpenSSH;
my $ssh = Net::OpenSSH->new('192.168.12.1', user => 'kharada');
$ssh->system('show configuration');
