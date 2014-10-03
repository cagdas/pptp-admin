#!/bin/bash
# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

if [ ! -r /etc/ppp/chap-secrets ]; then
	echo "Secret file not reachable !"
	exit 1
fi

PID_FILE="/var/run/pptp-admin.pid"

if [ ! -r $PID_FILE ]; then
	/usr/bin/python server.py start 1> logs/requests.log 2> logs/errors.log &
	pid=$!
	echo $pid > $PID_FILE
else
	pid=`cat $PID_FILE 2> /dev/null`

	if [ -e /proc/$pid -a /proc/$pid/exe ]; then
		echo "[ $pid ] Service has already started."
	else
	    rm /var/run/pptp-admin.pid
		echo "[ $pid ] Service stopped."
	fi
fi	