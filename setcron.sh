#!/bin/sh
# run this script to put pylocate to check every hour if your public_ip changed
cpath='python '`pwd`'/pylocate.py >> log/cron.log'
echo "adding the new cron rule"
crontab -l | { cat; echo "0 * * * * $cpath"; } | crontab -
echo "Successfully."
echo "Listing the cron tasks"
crontab -l
exit