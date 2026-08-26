# Snake en RTM32 Assembly

¡El clásico juego de Snake corriendo de forma nativa en la máquina RTM32!

## Instrucciones para jugar

1. Abre una terminal y arranca la máquina con la ROM del juego:
   \\ash
   ./maquina\ rtm32/rtm32 --rom=snake.bin
   \2. La máquina te dirá en qué terminal virtual se abrió el UART (la pantalla/teclado). Verás un mensaje como:
   \UART available on /dev/pts/93. Abre **otra** pestaña de terminal y conéctate usando \picocom\ (reemplaza el 9 con tu número):
   \\ash
   picocom /dev/pts/9
   \4. ¡Listo! Usa las teclas **W, A, S, D** para mover la serpiente.
