import pty, os, time, select, subprocess
master, slave = pty.openpty()
p = subprocess.Popen(['./rtm32.asm', 'test_rx.rtm', '-o', 'test_rx.bin'])
p.wait()
p = subprocess.Popen(['./maquina rtm32/rtm32', '--rom=test_rx.bin', '--numsteps=100'], stdin=slave, stdout=slave, stderr=slave)
time.sleep(0.5)
os.write(master, b'A')
time.sleep(0.5)
res = b''
while select.select([master], [], [], 0)[0]:
    res += os.read(master, 1024)
print('OUTPUT:', res.decode('utf-8', 'ignore'))
