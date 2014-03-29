#!/bin/sh

for i in `seq 1 5`;
do 
python clonevm.py -s vc.kazu.linux -u root -p <password> -n clone0${i}; 
done
