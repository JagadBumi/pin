import os, re, socket, sys, select, thread, time, configparser

ru = lambda text: text.decode('utf-8', 'ignore')
ur = lambda text: text.encode('utf-8', 'ignore')

W = '\x1b[0m'
R = '\x1b[31m'
G = '\x1b[1;32m'
O = '\x1b[33m'
B = '\x1b[34m'
P = '\x1b[35m'
C = '\x1b[36m'
GR = '\x1b[37m'

BLOCK = ('')
BUFFER = 1024

class realhost:

    def __init__(self, request, address):
        self.client = request
        self.Target_Host = None
        self.client_id = address
        self.AThread_NetData = self.client.recv(BUFFER)
        if self.AThread_NetData:
            if self.firewall(self.AThread_NetData):
                if 'HTTP' in self.AThread_NetData.splitlines()[0] and self.AThread_NetData.startswith('CONNECT'):
                    self.client.send('HTTP/1.1 200 Connection Established\r\n\r\n')
                    self.Run_Programs()
                #else:
                    #self.Run_Programs()
        return

    def __del__(self):
        self.client.close()

    def Run_Programs(self):
        netdata = self.AThread_NetData
        hp = netdata.split(' ')[1]
        h = hp.split(':')[0]
        p = hp.split(':')[1]
        req = netdata.replace(netdata, payload)
        req = req.replace('[host_port]',str(hp))
        req = req.replace('[host]',str(h))
        req = req.replace('[port]',str(p))
        req = req.replace('[crlf]','\r\n')
        self.Target_Host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.Target_Host.connect((phost, pport))
        except socket.error, (value,msg):
            self.client.close()
            self.Target_Host.close()
            os.system('clear')
            print(W + '+ ' + R + str(msg) + ' !')
        else:
            self.Target_Host.send(req)
            self.request_log(req)
            self.start = time.clock()
            self.handledata()

    def handledata(self, max_waiting = 30):
        socs = [self.Target_Host, self.client]
        count = 0
        while True:
            count += 1
            recv, _, error = select.select(socs, [], socs, 3)
            if error:
                break
            if recv:
                for bite in recv:
                    out = None
                    try:
                        data = bite.recv(BUFFER)
                    except socket.error, (value,msg):
                        break
                        os.system('clear')
                        print(W + '+ ' + B + str(msg) + ' !')

                    if data:
                        if bite is self.client:
                            if self.firewall(data):
                                out = self.Target_Host
                        elif bite is self.Target_Host:
                            out = self.client
                            self.response(data)
                        else:
                            break
                    else:
                        accept = False
                    if out:
                        out.send(data)
                        count = 0

            if count == max_waiting:
                break

        return

    def request_log(self, data):
        os.system('clear')
        print(W + '++++++++ Request ++++++++\n' + G + self.AThread_NetData.split('\r\n')[0] + '\n\n' + O + data.split('\r\n\r\n')[0] + '\n')

    def response(self, data):
        if data.startswith('HTTP'):
            print(W + '++++++++ Response ++++++++\n' + C + data.split('\n')[0])

    def firewall(self, data):
        url = data.splitlines()[0]
        for i in BLOCK:
            if i in url:
                return False

        return True

def main(handler = realhost):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('127.0.0.1', int(lport)))
    except socket.error, (value,msg):
        s.close()
        os.system('clear')
        sys.exit(W + '+ ' + O + str(msg) + ' !' + W)
    else:
        s.listen(0)
        while True:
            try:
                thread.start_new_thread(handler, s.accept())
            except KeyboardInterrupt:
                s.close()
                os.system('clear')
                sys.exit(W + '+ ' + O + 'pin.py stopped !' + W)

if __name__ == '__main__':
    os.system('clear')
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    config = configparser.ConfigParser()
    try:
        config.read_file(open(os.path.join(file_dir, 'config.ini')))
        payload = config['config']['payload']
        proxyhost = config['config']['proxyhost']
        pport = int(config['config']['proxyport'])
    except Exception as e:
        sys.exit(W + '+ config.ini not found !')
    regx = r'[a-zA-Z0-9_]'
    if re.match(regx,proxyhost):
        try:
            phost = socket.gethostbyname(proxyhost)
        except:
            phost = proxyhost
    try:
        lport = sys.argv[1]
    except Exception as e:
        os.system('clear')
        sys.exit(W + '+ ' + O + 'Usage: python2 pin.py 8080' + W)
    main()
    