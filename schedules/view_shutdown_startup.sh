#!/bin/bash
# file: clear_shutdown_startup

my_dir="`dirname \"$0\"`"
my_dir="`( cd \"$my_dir\" && pwd )`"
if [ -z "$my_dir" ] ; then
  exit 1
fi
. $my_dir/utilities.sh


shutdown_time=$(get_local_date_time "$(get_shutdown_time)")
if [ ${#shutdown_time} == '3' ]; then
    echo 'non def'
else
    echo " [$shutdown_time]";
fi

startup_time=$(get_local_date_time "$(get_startup_time)")
if [ ${#startup_time} == '3' ]; then
    echo 'non def'
else
    echo "  [$startup_time]";
fi	

#read