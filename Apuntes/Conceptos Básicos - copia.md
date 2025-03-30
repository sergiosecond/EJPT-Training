Vamos a tomar breves apuntes para recordar un poquito de  *liniiiiix*.

### Descriptores

> Los descriptores representan salidas en los sistemas Unix

- **0**: Entrada estándar (stdin), de donde lee el programa (por ejemplo, el teclado).
    
- **1**: Salida estándar (stdout), donde el programa escribe resultados (generalmente, la pantalla).
    
- **2**: Error estándar (stderr), para mensajes de error.

En este caso `burpsuite captura.cap &> /dev/null & disown`

Se redirige con `&>` tanto **stdout** como **stderr**
### bc

Comando para hacer cálculos

┌──(sergio1023k㉿secondmachine)-[~]
└─$ echo "5\*721" | bc
3605

### MAC ADDRESS

los primeros **3 bytes** (**24 bits**) representan el fabricante de la tarjeta, y los últimos **3 bytes** (**24 bits**) identifican la tarjeta particular de ese fabricante
 con `macchanger` cambiamos la MAC
### Escanear red a nivel arp
`arp-scan -I tarjeta-red --localnet

### Detectar procesos en puertos

- lsof -i:80
- wdx nºproceso --> Muestra Path donde está el server

### Puertos Comunes

/-/-/ **TCP** /-/-/

21 - FTP
22 - SSH
23 - telnet
80 - Http
139 /445 - SMB
443 - Https

/-/-/ **UDP** /-/-/

53 - DNS
67/68 - DHCP 
69 - TFTP (Trivial File Transfer Protocol)
123 -  NTP (Network Time Protocol) un protocolo simple utilizado para transferir archivos entre dispositivos en una red.
61- SNMP (Simple Network Management Protocol) – un protocolo utilizado para administrar y supervisar dispositivos en una red.

### UDP VS TCP

**TCP**  verifica si el receptor ha recibido los mensajes, three-way-handshake
**UDP** no verifica

### Remember Redes

Notación CIDR, para o desperdiciar IPs (**Classless Inter-Domain Routing**), es subnetting

Una forma rápida de saber cuántas IPs de una red son utilizables es contando los bits de una máscara que se quedan a 0 y elevándolos a 2

**EJEMPLO**
255.255.255.192
11111111.11111111.11111111.110000

2^6 =26 host utilizables

Web para calcular subnetting y rangos de red

- [https://www.ipaddressguide.com/cidr](https://www.ipaddressguide.com/cidr)
- [https://blog.jodies.de/ipcalc](https://blog.jodies.de/ipcalc)

## Un poquito de cálculo manual

192.112.114.29/13

11000000.01110000.01110010.00011101 192.112.114.29
11111111.11111000.00000000.00000000 255.248.0.0 mascara
11000000.01110000.00000000.00000000 192.112.0.0/13 dir red
11000000.01110111.11111111.11111111 192.119.255.255 broadcast --> a partir del /13 se pasa a 1 todos los 0

1º Ip utilizable --> 192.112.0.1
Última Ip utilizable --> 192.119.255.254

1.048.574 utilizables

## Samba vs SMB

- **Samba:**
>Programas de código abierto que sirven para la compartición de datos de S.O basados en unix como linux o MAC

- **SMB**
>Protocolo que se creó para compartición de aarchivos entre S.O diferentes