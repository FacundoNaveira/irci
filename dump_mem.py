import socket
import time

s = socket.socket()
s.connect(('localhost', 4444))

time.sleep(1)
print("Handshake")
s.sendall(b'\xff\xfb\x01\xff\xfb\x03\xff\xfd\x03\n')
time.sleep(1)
print(s.recv(1024).decode(errors='ignore'))

s.sendall(b'd m0xF0000000 4\n')
time.sleep(1)
print(s.recv(1024).decode(errors='ignore'))

s.sendall(b'd m0x00000000 4\n')
time.sleep(1)
print(s.recv(1024).decode(errors='ignore'))
