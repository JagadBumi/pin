import configparser
import subprocess
import socket
import sys
import re
import os

W = '\x1b[0m'
R = '\x1b[31m'
G = '\x1b[1;32m'
O = '\x1b[33m'
B = '\x1b[34m'
P = '\x1b[35m'
C = '\x1b[36m'
GR = '\x1b[37m'

class sshRun:

    def client(self, logs, host, port, username, password, phost, pport):
        proxycmd = f'-o "ProxyCommand corkscrew 127.0.0.1 {lport} %h %p"'
        sockport = f'-CND 1080'
        host = host
        port = port
        username = username
        password = password
        try:
            response= subprocess.Popen(
                (
                    f'sshpass -p {password} ssh {sockport} {username}@{host} -p {port} -v {proxycmd} -o ConnectTimeout=50 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
                ),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            for line in response.stdout:
                line = line.decode('utf-8',errors='ignore')
                if 'y' in sys.argv[2]:
                    print(line)
                    if 'Permission denied' in line:
                        print(R + 'username or password incorrect' + W)
                        os.system('killall screen -q')
                        os.system('screen -wipe > /dev/null')
                        os.system('killall bash -q')
                    if 'debug1: pledge: proc' in line:
                        print(W + '<> ' + G + 'SSH Connected' + W)
                elif 'n' in sys.argv[2]:
                    if 'HTTP/' in line:
                        rsp = line.split('\n')[0]
                        rsp = rsp.split(': ')[3]
                        os.system('clear')
                        print(G + 'CONNECT ' + host + ':' + port + ' HTTP/1.0' + W)
                        print(G + 'Connect using ' + O + phost + ':' + pport + W)
                        print(C + rsp + W)
                    if 'Permission denied' in line:
                        print(R + 'username or password incorrect' + W)
                        os.system('killall screen -q')
                        os.system('screen -wipe > /dev/null')
                        os.system('killall bash -q')
                    if 'debug1: pledge: proc' in line:
                        print(W + '<> ' + G + 'SOCKS5 Port Forwarded ' + sockport.split(' ')[1] + W)
                        print(W + '<> ' + G + 'SSH Connected' + W)
                else:
                    print(line)
                    if 'Permission denied' in line:
                        print(R + 'username or password incorrect' + W)
                        os.system('killall screen -q')
                        os.system('screen -wipe > /dev/null')
                        os.system('killall bash -q')
                    
        except KeyboardInterrupt:
            os.system('clear')
            sys.exit(W + '<> ' + O + 'ssh stopped !' + W)

    def main(self):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        config = configparser.ConfigParser()
        try:
            config.read_file(open(os.path.join(file_dir, 'config.ini')))
            host = config['ssh']['host']
            port = config['ssh']['port']
            username = config['ssh']['username']
            password = config['ssh']['password']
            proxyhost = config['config']['proxyhost']
            proxyport = config['config']['proxyport']
            regx = r'[a-zA-Z0-9_]'
            if re.match(regx,proxyhost):
                try:
                    phost = socket.gethostbyname(proxyhost)
                    pport = proxyport
                except:
                    phost = proxyhost
                    pport = proxyport
        except Exception as e:
            os.system('clear')
            sys.exit(W + '<> ' + O + 'config.ini not found !' + W)
            
        self.client(logs, host, port, username, password, phost, pport)
        
try:
    lport = sys.argv[1]
    logs = sys.argv[2]
except Exception as e:
    os.system('clear')
    sys.exit(W + '<> ' + O + 'Usage: python3 ssh.py 8080' + W)
sshRun().main()
