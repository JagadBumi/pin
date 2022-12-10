#!/bin/bash
clear
function logs(){
	clear
	read -p "<> Enable Logs [y/n]: " log
	case $log in y)
	lg="y";;
	n)
	lg="n";;
	*)
	lg="$log";;
	esac
	clear
}
logs
function connect(){
    killall screen -q
    screen -wipe > /dev/null
    killall python2 -q
    killall python3 -q
    killall ssh -q
    lport="$1"
    screen -AmdS nohub python2 pin.py $lport
    sleep 1
    python3 ssh.py $lport $lg
}

while true
do
connect 8080
done
