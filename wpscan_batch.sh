#!/bin/bash
# Wrapper for wpscan
# Author: Jose Vicente Nunez
# gem install wpscan
# To send messages to the Telegram Bot
# python3 -m venv ~/virtualenv/wpscan
# . ~/virtualenv/wpscan/bin/activate
# pip install requests --upgrade
. ~/virtualenv/wpscan/bin/activate
#test -x $HOME/graalvm-ce-java11-21.0.0.2/bin/ruby && export RUBY=$HOME/graalvm-ce-java11-21.0.0.2/bin/ruby|| export RUBY=/usr/bin/ruby
export RUBY=/usr/bin/ruby
/usr/bin/logger --stderr "Started $0. It will take a while"
for site in $WPSCAN_SITES; do
	(
	logfile="$HOME/logs/wpscan-$(/usr/bin/basename $site).log"
	report="$HOME/logs/wpscan-$(/usr/bin/basename $site).json"
	/usr/bin/logger --stderr "$0: Analyzing $site:$logfile"
	$RUBY $HOME/bin/wpscan --url "$site" --api-token "$WPSCAN_API_KEY" --plugins-detection mixed --format json --output $logfile
	/usr/bin/jq '.["version"]|.vulnerabilities[].references' $logfile > $report
	if [ -x "$HOME/bin/send_telegram_mesg.sh" ]; then
		#declare CVE=$(/usr/bin/jq --raw-output '.|.cve|.[]' $report| /bin/sed 's#-#\\\\\\\\-#g'| /bin/xargs)
		#test -n "$CVE" && $HOME/bin/send_telegram_mesg.sh "*CVE*: $CVE"
		declare CVE=$(/usr/bin/jq --raw-output '.|.cve|.[]' $report| /bin/xargs)
		test -n "$CVE" && $HOME/bin/send_telegram_mesg.py "$site *CVE*: $CVE"
	fi
	) &
done
sleep 5
/usr/bin/logger --stderr "$0: Waiting for all sites to finish..."
wait
/usr/bin/logger --stderr "$0 is done"
