# Emulador RTM32 - Suite de Pruebas en Assembly

Con la llegada del compilador oficial `rtm32.asm`, hemos migrado nuestra suite de pruebas generada en Python a código Assembly real (`.rtm`). Estos scripts evalúan exhaustivamente los subsistemas de la CPU RTM32.

## Instalación del Ensamblador

El compilador `rtm32.asm` ya se encuentra configurado en la raíz del proyecto para Linux. Para compilar los scripts de prueba a formato ROM (`.bin`), utiliza el siguiente formato:

```bash
./rtm32.asm test_alu.rtm -o test_alu.bin
```

## Instrucciones de Uso de las ROMs

Para probar la máquina, carga la ROM correspondiente en el emulador y activa el depurador por telnet:

```bash
./maquina\ rtm32/rtm32 --rom=test_alu.bin --debug=telnet
```

Luego, conéctate en otra terminal (`rlwrap telnet localhost 4444`), ejecuta el comando `step N` para correr la simulación y usa `r` para inspeccionar los registros.

---

## 1. Test ALU y Lógica (`test_alu.rtm`)

Pone a prueba la Unidad Aritmético-Lógica (ADD, DIV, REST), lógica inmediata (ANDI, ORI) y comparaciones (SLTI).

**Ejecución:**
`step 9`
---

## 2. Test de Subsistema de Memoria (`test_mem.rtm`)

Pone a prueba Load/Store utilizando direccionamiento indexado simple y extendido (SWX) probando varios anchos de palabra.

**Ejecución:**
`step 10`
---

## 3. Test de Sistema y Saltos (`test_sys.rtm`)

Pone a prueba el ruteo interno: saltos (`JAL`, `JR`), lecturas/escrituras de registros especiales (`CFS`, `CTS`) y las excepciones de software (`TRAP`, `RFT`).

**Ejecución:**
`step 12`

---

## 4. Prueba de Concepto: Secuencia de Fibonacci (`test_fibonacci.rtm`)

Esta es una prueba de concepto avanzada que demuestra la capacidad de la CPU para resolver problemas de la vida real. Calcula e imprime los primeros 25 números de la secuencia de Fibonacci. 

Este test pone a prueba múltiples características clave de la máquina al mismo tiempo:
- **Bucles y Control de Flujo:** Para generar la secuencia iterativamente.
- **Manejo de la Pila (Stack):** Uso del puntero `$sp` para guardar valores temporales.
- **Matemática y Conversión:** Incluye una subrutina personalizada `itoa` (Integer-to-ASCII) escrita en ensamblador que utiliza las instrucciones nativas de división (`divu`) y módulo (`restu`) de la CPU para convertir números binarios a texto legible y enviarlos por la UART.

**Ejecución automatizada:**
Para facilitar la ejecución, se incluye un script en Python que arranca el emulador, se conecta al depurador por telnet, carga el programa en memoria y redirige la salida serial directamente a tu consola. Solo ejecuta:

```bash
python3 run_fibonacci.py
```
