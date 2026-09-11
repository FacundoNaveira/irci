import socket, subprocess, time

p = subprocess.Popen(['./maquina rtm32/rtm32', '--rom=snake.bin', '--exec=0xF0000000', '-d', 'telnet'])
time.sleep(1)
s = socket.socket()
s.connect(('localhost', 4444))

def wait_prompt(s):
    buf = b''
    for _ in range(50):
        try:
            buf += s.recv(1024)
            if b'RTM32>' in buf: return True
        except: pass
        time.sleep(0.05)
    return False

s.settimeout(0.1)
wait_prompt(s)
s.send(b'c\n')

buf = b''
s.settimeout(2.0)
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
