import subprocess
import time
import socket
import select
import sys
import threading
import os

def consume_stdout(p):
    for line in p.stdout:
        pass

def main():
    print("Starting Emulator...")
    # Start emulator
    p = subprocess.Popen(["./maquina rtm32/rtm32", "-d", "telnet", "--log=INFO"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    pty_path = None
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
        
    threading.Thread(target=consume_stdout, args=(p,), daemon=True).start()
    time.sleep(0.5)
    
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
    
    s.sendall(b'load test_fibonacci.mdbg\r\n')
    time.sleep(0.1)
    s.sendall(b's pc 0\r\n')
    time.sleep(0.1)
    s.sendall(b'c\r\n')
    
    # Read output
    fd = os.open(pty_path, os.O_RDWR | os.O_NONBLOCK)
    print("--- Output from UART ---")
    start = time.time()
    while time.time() - start < 1.0:
        r, _, _ = select.select([fd], [], [], 0.1)
        if fd in r:
            try:
                out = os.read(fd, 4096)
                if out:
                    sys.stdout.buffer.write(out)
                    sys.stdout.buffer.flush()
            except:
                break
    
    print("\n--- Done ---")
    p.kill()

if __name__ == '__main__':
    main()
