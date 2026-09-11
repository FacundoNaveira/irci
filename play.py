import socket
import sys
import threading
import time
import termios
import tty

def forward_output(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        except:
            break

def main():
    s = socket.socket()
    s.connect(('localhost', 4444))
    
    # Handshake
    time.sleep(0.1)
    s.sendall(b'\xff\xfb\x01\xff\xfb\x03\xff\xfd\x03\n')
    time.sleep(0.1)
    s.recv(4096)
    s.sendall(b'\xff\xfe\x01\xff\xfe\x03\xff\xfc\x03')
    time.sleep(0.1)
    s.recv(4096)
    
    # Load program
    s.sendall(b'load snake_flat.bin\r\n')
    time.sleep(0.1)
    s.recv(4096)
    
    # Set PC
    s.sendall(b's pc 0\r\n')
    time.sleep(0.1)
    s.recv(4096)
    
    # Continue
    s.sendall(b'c\r\n')
    time.sleep(0.1)
    
    # Print what we've missed (usually just the 'RTM32> Continuing execution...' text)
    # We will ignore it to keep the screen clean.
    s.recv(4096)
    
    # Set raw terminal mode for capturing keys instantly
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        
        t = threading.Thread(target=forward_output, args=(s,))
        t.daemon = True
        t.start()
        
        while True:
            ch = sys.stdin.read(1)
            if not ch:
                break
            s.sendall(ch.encode('ascii'))
            if ch == 'q':  # emergency exit
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    main()
