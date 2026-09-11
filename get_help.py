import socket
import time

s = socket.socket()
s.connect(('localhost', 4444))

time.sleep(1)
s.sendall(b'\xff\xfb\x01\xff\xfb\x03\xff\xfd\x03\n')
time.sleep(1)
s.recv(1024)

s.sendall(b'help\n')
time.sleep(1)
print(s.recv(4096).decode(errors='ignore'))
