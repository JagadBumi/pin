#!/bin/python3
import configparser
import subprocess
import socket
import time
import sys
import os

W = '\x1b[1;0m'
R = '\x1b[1;31m'
G = '\x1b[1;32m'
O = '\x1b[1;33m'
B = '\x1b[1;34m'
P = '\x1b[1;35m'
C = '\x1b[1;36m'
GR = '\x1b[37m'

class sshRun:

    def client(self, host, port, username, password, phost, pport):
        proxycmd = f'-o "ProxyCommand corkscrew 127.0.0.1 {lport} %h %p"'
        sockport = f'-CND 1080'
        while True:
            try:
                response = subprocess.Popen(
                    (
                        f'sshpass -p {password} ssh {sockport} {username}@{host} -p {port} -v {proxycmd} -o ConnectTimeout=30 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
                    ),
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
                for line in response.stdout:
                    line = line.decode('utf-8', errors='ignore')
                    if 'HTTP/' in line:
                        rsp = line.split('\n')[0]
                        rsp = rsp.split(': ')[3]
                        os.system('clear')
                        print(G + 'CONNECT ' + socket.gethostbyname(host) + ':' + port + ' HTTP/1.0' + W)
                        print(G + 'Connect using ' + O + socket.gethostbyname(phost) + ':' + pport + W)
                        print(C + rsp + W)
                    if 'Permission denied' in line:
                        os.system('clear')
                        print(W + '<> ' + R + 'username or password incorrect' + W)
                        print(W + '<> ' + R + host + W)
                        print(W + '<> ' + R + username + W)
                        print(W + '<> ' + R + password + W)
                        os.system('killall screen -q')
                        os.system('screen -wipe > /dev/null')
                        os.system('killall python2 -q')
                        sys.exit()
                    if 'debug1: pledge: proc' in line:
                        print(W + '<> ' + G + 'SOCKS5 Port Forwarded ' + sockport.split(' ')[1] + W)
                        print(W + '<> ' + G + 'SSH Connected' + W)
                time.sleep(1)
            except KeyboardInterrupt:
                os.system('clear')
                print(W + '<> ' + O + 'ssh stopped' + W)
                os.system('killall screen -q')
                os.system('screen -wipe > /dev/null')
                os.system('killall python2 -q')
                break
            
    def main(self):
        os.system('screen -AmdS nohub python2 pin.py %s' % lport)
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        config = configparser.ConfigParser()
        try:
            config.read_file(open(os.path.join(file_dir, 'config.ini')))
            host = config['ssh']['host']
            port = config['ssh']['port']
            username = config['ssh']['username']
            password = config['ssh']['password']
            phost = config['config']['proxyhost']
            pport = config['config']['proxyport']
        except Exception as e:
            os.system('clear')
            print(W + '<> ' + O + 'config.ini not found !' + W)
            os.system('killall screen -q')
            os.system('screen -wipe > /dev/null')
            os.system('killall python2 -q')
            sys.exit()
            
        self.client(host, port, username, password, phost, pport)
        
lport = 7071
sshRun().main()
