# How to use pin
<b>install python corkscrew screen</b>
<pre><code>
pkg install python python2 python3 corkscrew screen -y
pip install configparser
pip2 install configparser
git clone https://github.com/JagadBumi/pin
cd pin
chmod +x *
</code></pre>

Set up config.ini the payload proxy host port and ssh host port username password
<br>

run the script run.sh
<br>
bash run.sh or ./run.sh
<br>

If connected open tun2tap for socks port forwarded
<br>

Server ip 127.0.0.1
<br>
Server port 1080
<br>

Set custom routes exclude
<br>
8.8.8.8/32;proxyhosthere/32
