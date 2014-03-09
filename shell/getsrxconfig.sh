#!/bin/sh

ssh -l kharada 192.168.12.1 "show configuration" > /var/log/srx_config/srx_`date +"%Y%m%d_%I%M"`.txt
