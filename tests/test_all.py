import socket, time, subprocess, pty, os, select

master, slave = pty.openpty()
emu = subprocess.Popen(['./maquina rtm32/rtm32', '--rom=snake.bin', '--exec=0xF0000000', '-d', 'telnet'], stdin=slave, stdout=slave, stderr=slave)
time.sleep(1)

s = socket.socket()
s.connect(('localhost', 4444))
time.sleep(0.5)
# read telnet handshake
print("TELNET:", s.recv(1024))
s.send(b'c\n')
time.sleep(1)
s.send(b'step\n')
time.sleep(0.5)

res = b''
while select.select([master], [], [], 0)[0]:
    res += os.read(master, 10240)
print('UART OUTPUT LEN:', len(res))
if len(res) > 0:
    print('UART HEAD:', res[:500].decode('utf-8', 'ignore'))
    print('UART TAIL:', res[-500:].decode('utf-8', 'ignore'))

print("TELNET:", s.recv(1024))
emu.kill()
