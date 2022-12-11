#!/bin/bash
# file: clear_shutdown_startup

my_dir="`dirname \"$0\"`"
my_dir="`( cd \"$my_dir\" && pwd )`"
if [ -z "$my_dir" ] ; then
  exit 1
fi
. $my_dir/utilities.sh


clear_startup_time
clear_shutdown_time
