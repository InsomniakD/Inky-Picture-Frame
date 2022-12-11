#!/bin/bash
# file: add_shutdown_startup.sh

my_dir="`dirname \"$0\"`"
my_dir="`( cd \"$my_dir\" && pwd )`"
if [ -z "$my_dir" ] ; then
  exit 1
fi
. $my_dir/utilities.sh

TZDATE=$(date +%Z)

if [ "$TZDATE" == "CEST" ] ; then   #UCT +2h  (23h utc = 1h cest)
  date=$(date +%d --date='14 minute')
  hour=$(date +%H --date='14 minute')
  hour=${hour#0}
  minute=$(date +%M --date='14 minute')
  second='00'
  if [ "$hour" == 0 ] ; then
	  hour=22
	  date=$((date-1))
  elif [ "$hour" == 1 ] ; then
	  hour=23
	  date=$((date-1))
  else
	  hour=$((hour-2))
  fi
  set_startup_time $date $hour $minute $second

  date=$(date +%d --date='4 minute')
  hour=$(date +%H --date='4 minute')
  hour=${hour#0}
  minute=$(date +%M --date='4 minute')
  if [ "$hour" == 0 ] ; then
	  hour=22
	  date=$((date-1))
  elif [ "$hour" == 1 ] ; then
	  hour=23
	  date=$((date-1))
	else
	  hour=$((hour-2))
  fi
  set_shutdown_time $date $hour $minute

else
  date=$(date +%d --date='14 minute')
  hour=$(date +%H --date='14 minute')
  hour=${hour#0}
  minute=$(date +%M --date='14 minute')
  if [ "$hour" == 0 ] ; then
	  hour=23
	  date=$((date-1))
	else
	  hour=$((hour-1))
  fi

  second='00'
  set_startup_time $date $hour $minute $second

  date=$(date +%d --date='4 minute')
  hour=$(date +%H --date='4 minute')
  hour=${hour#0}
  minute=$(date +%M --date='4 minute')
  if [ "$hour" == 0 ] ; then
	  hour=23
	  date=$((date-1))
	else
	  hour=$((hour-1))
  fi
  set_shutdown_time $date $hour $minute
fi