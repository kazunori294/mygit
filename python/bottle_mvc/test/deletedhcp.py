#!/usr/bin/python
# coding: UTF-8
 
f = open('/dhcp/dhcpd-reservations.conf')
lines = f.readlines()
fp = open('/dhcp/test.txt', 'w')

for line in lines:
  if not "ubu" in line:
    fp.write(line)
	
f.close()
fp.close()
