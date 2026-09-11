import socket, subprocess, time

p = subprocess.Popen(['./maquina rtm32/rtm32', '--rom=snake.bin', '--exec=0xF0000000', '-d', 'telnet'])
time.sleep(1)
s = socket.socket()
s.connect(('localhost', 4444))
# Wait for negotiation
time.sleep(0.5)
s.recv(1024)
s.send(b'c\n')

s.settimeout(2.0)
buf = b''
try:
    while True:
        data = s.recv(1024)
        if not data: break
        buf += data
except socket.timeout:
    pass

print('TELNET OUTPUT:')
print(buf.decode('utf-8', 'ignore'))
p.kill()
