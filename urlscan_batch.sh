#!/bin/bash
# Batch to scan Jose Nunez domains
# https://github.com/heywoodlh/urlscan-py
# https://urlscan.io/user/
# How to use:
# 0 0 * * * $HOME/urlscan_batch.sh > $HOME/urlscan_batch.log
URLSCAN_API_KEY="XXXx"
export URLSCAN_API_KEY
domains=$(/bin/mktemp)|| exit 100
/bin/cat<<EOF>$domains
http://XXXXX.com
http://ZZZZZ.com
EOF
trap "/bin/rm -f $domains" INT QUIT EXIT
/usr/bin/logger --stderr "$: Started"
. ~/virtualenv/urlscan/bin/activate|| exit 100
# /bin/rm -f ~/.urlscan/urlscan.db
# urlscan init --api $URLSCAN_API_KEY
/usr/bin/logger --stderr "$0: Scanning domains from $domains"
urlscan scan --file $domains|| exit 100
/usr/bin/sleep 1h
while read url; do
    site=$(/usr/bin/basename $url| /bin/cut -d'.' -f1)
    /usr/bin/logger --stderr "$0: Search $url"
    search=$(urlscan search --url $url| /bin/tail -1;)
    /usr/bin/logger --stderr "$0: $search"
    uuid=$(echo $search| /usr/bin/cut -d' ' -f 5)
    logfile="$HOME/logs/urlscan-$site.log"
    /usr/bin/logger --stderr "$0: Retrieve $uuid: $logfile"
    urlscan retrieve --uuid $uuid --summary > $logfile
done < $domains
