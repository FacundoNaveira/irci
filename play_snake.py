import subprocess
import time
import socket
import select
import sys
import threading
import termios
import tty
import os

def forward_uart(pty_path):
    # Open PTY
    try:
        fd = os.open(pty_path, os.O_RDWR | os.O_NONBLOCK)
    except Exception as e:
        print(f"\r\nFailed to open UART PTY {pty_path}: {e}")
        return

    # Forward stdin to UART, and UART to stdout
    stdin_fd = sys.stdin.fileno()
    
    while True:
        r, w, x = select.select([stdin_fd, fd], [], [], 0.05)
        
        if stdin_fd in r:
            ch = os.read(stdin_fd, 1)
            if not ch:
                break
            # Press 'q' to quit
            if ch == b'q':
                break
            os.write(fd, ch)
            
        if fd in r:
            try:
                out = os.read(fd, 4096)
                if out:
                    sys.stdout.buffer.write(out)
                    sys.stdout.buffer.flush()
            except BlockingIOError:
                pass
            except OSError:
                break

def main():
    print("Starting Emulator...")
    # Start emulator
    p = subprocess.Popen(["./maquina rtm32/rtm32", "-d", "telnet"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    pty_path = None
    
    # Read until we find the PTY path
    while True:
        line = p.stdout.readline()
        if not line:
            break
        line_str = line.decode('utf-8', 'ignore')
        if "UART available on" in line_str:
            pty_path = line_str.split("UART available on")[1].strip()
            break
            
    if not pty_path:
        print("Failed to find UART PTY!")
        p.kill()
        return
        
    print(f"UART PTY found at {pty_path}")
    print("Connecting to debugger...")
    
    time.sleep(1.0)
    
    # Connect to debugger
    s = socket.socket()
    s.connect(('localhost', 4444))
    s.settimeout(1.0)
    
    # Handshake
    s.sendall(b'\xff\xfb\x01\xff\xfb\x03\xff\xfd\x03\n')
    try: s.recv(4096)
    except: pass
    s.sendall(b'\xff\xfe\x01\xff\xfe\x03\xff\xfc\x03')
    try: s.recv(4096)
    except: pass
    
    print("Loading game...")
    s.sendall(b'load snake.mdbg\r\n')
    try: s.recv(4096)
    except: pass
    
    s.sendall(b's pc 0\r\n')
    try: s.recv(4096)
    except: pass
    
    print("Starting execution...")
    s.sendall(b'c\r\n')
    try: s.recv(4096)
    except: pass
    
    print("Game started! Use W,A,S,D to move. Press 'q' to quit.")
    time.sleep(0.5)
    
    # Put terminal in raw mode
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        forward_uart(pty_path)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
    p.kill()
    print("\nGame exited.")

if __name__ == '__main__':
    main()
