#!/bin/bash
# file: syncTime.sh

if [ ! -z "$1" ]; then
  sleep $1
fi

my_dir="`dirname \"$0\"`"
my_dir="`( cd \"$my_dir\" && pwd )`"
if [ -z "$my_dir" ] ; then
  exit 1
fi
. $my_dir/utilities.sh

rtctime="$(get_rtc_time)"
  
if [[ $rtctime != *"1999"* ]] && [[ $rtctime != *"2000"* ]]; then
  rtc_to_system
fi

if $(has_internet) ; then
  net_to_system
  system_to_rtc
else
  sysyear="$(date +%Y)"
  if [[ $rtctime == *"1999"* ]] || [[ $rtctime == *"2000"* ]]; then
    if [[ $sysyear != *"1969"* ]] && [[ $sysyear != *"1970"* ]]; then
      system_to_rtc
    fi
  fi
fi