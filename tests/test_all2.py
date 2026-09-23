import socket, time, subprocess, pty, os, select, sys

master, slave = pty.openpty()
emu = subprocess.Popen(['./maquina rtm32/rtm32', '--rom=snake.bin', '--exec=0xF0000000', '-d', 'telnet'], stdin=slave, stdout=slave, stderr=slave)
time.sleep(1)

s = socket.socket()
s.connect(('localhost', 4444))

def read_until(s, string):
    buf = b''
    for _ in range(100):
        try:
            d = s.recv(1)
            if not d: break
            buf += d
            if string.encode() in buf: return buf
        except: pass
        time.sleep(0.01)
    return buf

print('WAITING FOR PROMPT...')
print(read_until(s, 'RTM32> '))

print('SENDING c...')
s.send(b'c\n')
time.sleep(2)

print('SENDING break to check PC...')
s.send(b'\x03') # Maybe Ctrl+C ? Or just connect another telnet? No, let's just kill it.

res = b''
while select.select([master], [], [], 0)[0]:
    res += os.read(master, 10240)
print('UART OUTPUT LEN:', len(res))
if len(res) > 0:
    print('UART TAIL:', res[-1000:].decode('utf-8', 'ignore'))

emu.kill()
