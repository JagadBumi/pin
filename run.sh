#!/bin/bash
clear
function connect(){
    killall screen -q
    screen -wipe > /dev/null
    killall python2 -q
    killall python3 -q
    killall ssh -q
    lport="$1"
    screen -AmdS nohub python2 pin.py $lport
    sleep 1
    python3 ssh.py $lport
}

while true
do
connect 8080
done
