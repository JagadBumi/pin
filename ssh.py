import configparser
import subprocess
import sys
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

    def client(self, host, port, username, password):
        proxycmd = f'-o "ProxyCommand corkscrew 127.0.0.1 {lport} %h %p"'
        host = host
        port = port
        username = username
        password = password
        try:
            response= subprocess.Popen(
                (
                    f'sshpass -p {password} ssh -CND 1080 {username}@{host} -p {port} -v {proxycmd} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
                ),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            for line in response.stdout:
                line = line.decode('utf-8',errors='ignore')
                print(line)
                if 'debug1: pledge: proc' in line:
                    print(W + 'debug1: ' + G + 'Connected Successfully' + W)
        except KeyboardInterrupt:
            os.system('clear')
            sys.exit('debug1: Stopped !')

    def main(self):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        config = configparser.ConfigParser()
        try:
            config.read_file(open(os.path.join(file_dir, 'config.ini')))
            host = config['ssh']['host']
            port = config['ssh']['port']
            username = config['ssh']['username']
            password = config['ssh']['password']
        except Exception as e:
            os.system('clear')
            sys.exit(W + '+ ' + O + 'config.ini not found !' + W)
        self.client(host, port, username, password)
        
try:
    lport = sys.argv[1]
except Exception as e:
    os.system('clear')
    sys.exit(W + '+ ' + O + 'Usage: python3 ssh.py 8080' + W)
sshRun().main()
