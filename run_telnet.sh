./maquina\ rtm32/rtm32 --rom=snake.mdbg --trace=exec -d telnet > emu.log 2>&1 &
sleep 1
(sleep 1; echo ""; sleep 1; echo "c"; sleep 2) | telnet localhost 4444 > telnet.log 2>&1
killall rtm32
cat emu.log
cat telnet.log
