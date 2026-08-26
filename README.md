# Emulador RTM32 - Suite de Pruebas en Assembly

Con la llegada del compilador oficial \tm32.asm\, hemos migrado nuestra suite de pruebas generada en Python a código Assembly real (\.rtm\). Estos scripts evalúan exhaustivamente los subsistemas de la CPU RTM32.

## Instalación del Ensamblador

El compilador \tm32.asm\ ya se encuentra configurado en la raíz del proyecto para Linux. Para compilar los scripts de prueba a formato ROM (\.bin\), utiliza el siguiente formato:

\\ash
./rtm32.asm test_alu.rtm -o test_alu.bin
\
## Instrucciones de Uso de las ROMs

Para probar la máquina, carga la ROM correspondiente en el emulador y activa el depurador por telnet:

\\ash
./rtm32 --rom=test_alu.bin --debug=telnet
\
Luego, conéctate en otra terminal (\lwrap telnet localhost 4444\), ejecuta el comando \step N\ para correr la simulación y usa \\ para inspeccionar los registros.

---

## 1. Test ALU y Lógica (\	est_alu.rtm\)

Pone a prueba la Unidad Aritmético-Lógica (ADD, DIV, REST), lógica inmediata (ANDI, ORI) y comparaciones (SLTI).

**Ejecución:**
\step 9
---

## 2. Test de Subsistema de Memoria (\	est_mem.rtm\)

Pone a prueba Load/Store utilizando direccionamiento indexado simple y extendido (SWX) probando varios anchos de palabra.

**Ejecución:**
\step 10
---

## 3. Test de Sistema y Saltos (\	est_sys.rtm\)

Pone a prueba el ruteo interno: saltos (\JAL\, \JR\), lecturas/escrituras de registros especiales (\CFS\, \CTS\) y las excepciones de software (\TRAP\, \RFT\).

**Ejecución:**
\step 12EOF
