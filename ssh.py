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
GR = '\x1b[1;37m'

class sshRun:

    def client(self, host, port, username, password, phost, pport, ptype):
        proxycmd = f'-o "ProxyCommand corkscrew 127.0.0.1 {lport} %h %p"'
        sockport = f'-CND 1080'
        try:
            response = subprocess.Popen(
                (
                    f'sshpass -p {password} ssh {sockport} {username}@{host} -p {port} -v {proxycmd} -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
                ),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            
            for line in response.stdout:
                line = line.decode('utf-8', errors='ignore')
                
                if 'debug1: Executing proxy command:' in line:
                    os.system('clear')
                    print(G + 'CONNECT ' + socket.gethostbyname(host) + ':' + port + ' HTTP/1.0' + W)
                    if 'http' in ptype:
                        print(G + 'Using HTTP ' + O + socket.gethostbyname(phost) + ':' + pport + W)
                    if 'socks4' in ptype:
                        print(G + 'Using SOCKS4 ' + O + socket.gethostbyname(phost) + ':' + pport + W)
                    if 'socks5' in ptype:
                        print(G + 'Using SOCKS5 ' + O + socket.gethostbyname(phost) + ':' + pport + W)
                    
                if 'HTTP/' in line:
                    rsp = line.split('\n')[0]
                    rsp = rsp.split(': ')[3]
                    print(C + rsp + W)
                    
                if 'Connection timed out during banner exchange' in line:
                    print(R + 'Connection timed out during' + W)
                    
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
                    
        except Exception as e:
            os.system('clear')
            print(W + '<> ' + R + str(e).split('] ')[1] + W)
            os.system('killall screen -q')
            os.system('screen -wipe > /dev/null')
            os.system('killall python2 -q')
            
    def main(self):
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
            ptype = config['config']['proxytype']
            
            os.system('clear')
            if 'http' in ptype:
                os.system('screen -AmdS nohub python2 pin.py %s' % lport)
            elif 'socks4' in ptype:
                os.system('screen -AmdS nohub pproxy -l http://:8989 -r socks4://%s:%s -vv' % (phost, pport))
                os.system('screen -AmdS nohub python2 pin.py %s' % lport)
            elif 'socks5' in ptype:
                os.system('screen -AmdS nohub pproxy -l http://:8989 -r socks5://%s:%s -vv' % (phost, pport))
                os.system('screen -AmdS nohub python2 pin.py %s' % lport)
            else:
                os.system('clear')
                print(W + '<> ' + R + 'proxy type incorrect, http, socks4, socks5' + W)
                sys.exit()
                
        except Exception as e:
            os.system('clear')
            print(W + '<> ' + O + 'config.ini not found !' + W)
            os.system('killall screen -q')
            os.system('screen -wipe > /dev/null')
            os.system('killall python2 -q')
            sys.exit()
            
        while True:
            try:
                time.sleep(2)
                self.client(host, port, username, password, phost, pport, ptype)
            except KeyboardInterrupt:
                os.system('clear')
                print(W + '<> ' + O + 'ssh stopped' + W)
                os.system('killall screen -q')
                os.system('screen -wipe > /dev/null')
                os.system('killall python2 -q')
                break
                
if __name__ == '__main__':
    lport = 7071
    sshRun().main()
    