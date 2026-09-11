import socket, time
s = socket.socket()
s.connect(('localhost', 4444))
time.sleep(0.5)
s.recv(1024)
s.send(b'step\n')
time.sleep(0.5)
print(s.recv(1024).decode('utf-8', 'ignore'))
