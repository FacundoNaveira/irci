import subprocess, time, socket, sys, os, termios, tty

p = subprocess.Popen(['./maquina rtm32/rtm32', '-d', 'telnet', '--log=INFO'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pty_path = None
while True:
    line = p.stdout.readline().decode('utf-8', 'ignore')
    if 'UART available on' in line:
        pty_path = line.split('UART available on')[1].strip()
        break

time.sleep(1)
fd = os.open(pty_path, os.O_RDWR | os.O_NONBLOCK)
attr = termios.tcgetattr(fd)
print('IFLAG:', hex(attr[0]))
p.kill()
