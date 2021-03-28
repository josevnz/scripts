#!/bin/bash
# Wrapper for nikto
# Author: Jose Vicente Nunez
report=$HOME/logs/nikto-XXXX-com.json
/usr/bin/logger --stderr "Started $0. It will take a while"
for site in http://XXXX.com; do
	$HOME/nikto/program/nikto.pl \
		-host $site \
		-maxtime 1h \
		-no404 \
		-nointeractive \
		-Plugins 'apache_expect_xss;apacheusers;auth;cgi;content_search;cookies;dictionary;dir_traversal;favicon;fileops;headers;httpoptions;msgs;multiple_index;origin_reflection;paths;put_del_test;report_json;robots;shellshock;sitefiles;ssl;tests' \
		-Tuning 0x123456789ac \
		-Format json \
		-output $report
done
/usr/bin/logger --stderr "$0 is done"
