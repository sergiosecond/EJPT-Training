### Por dónde empezar

- Comando para saber las tablas del router --> `route -n  ^4242b8
## Nivel local

- IP propia --> hostname -I
- Va directamente a tu dir de red --> arp-scan -Itarjeta_red --ignoredups --localnet
- Descubre el devices especificado en la dir red --> netdiscover -r 192.168.1.0/24
- whichSystem.py --> se guía por el TTL

## Nmap 

- Todos los puertos --> nmap -p- 192.168.1.1 
- 1000 más comunes --> nmap 192.168.1.1
- 500 más comunes --> nmap --top-ports 500 192.168.1.1
- un poco de verbose --> nmap -p- --open -v 192.168.1.1
- enseña stats cada 2 min --> nmap -p- --open --stats-every 2m 192.168.1.1
- no dns, no ping --> nmap -p- -n -Pn 192.168.1.1
- lanza escaneos cada 2 min --> nmap -p- --scan-delay 2m 192.168.1.1
- aplica un barrido con ping al rango y sacar las IPs up --> nmap -sn 192.168.1.1/24 | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
- Busca versión y scripts --> nmap -sVC 192.168.1.1
### Evasión de firewall

- Poner muchas IPS, puede que el firewall permita  a una de ellas para ver si el port está up --> nmap -D 192.168.1.15,192.168.1.72,192.168.1.52, etc... 192.168.1.1
- fragmentar paquetes --> nmap -f 192.168.1.1
- ajusta el tamaño de los paquetes(Múltiplos de 8) --> nmap -f --mtu 16
- Da un puerto de origen seleccionado por si el firewall sólo acepta ese puerto --> nmap --source-port 53 192.168.1.1
- Manipular la longitud de paquete(lo que ya pesa el paquete+loquequeremos mirar en wireshark) --> nmap --data-length 21 192.168.1.1
- Spoofear MAC, hay veces que no detecta el puerto abierto --> nmap --spoof-mac {Dell,vmware} 192.168.1.1
### Scripts

**Estos scripts están escritos en LUA**

Hay 14 categorías podemos elegir entre que categorías tirar al target
- Esto es para filtrar por "" y que dentro de esas comillas haya info con `grep -oP '".*?"'`
- locate .nse | xargs grep "categories" | grep -oP '" .\*? "' | sort -u

- nmap --script="vuln and safe"
- nmap --script=vuln,dos,safe 192.168.1.1

## Masscan

- Ojo si es rápido pierdes info de los puertos -->  masscan -p 21,22,445,139 -Pn 192.168.1.0/16 --rate=1000
## Tcpdump

Para capturar el tráfico y luego abrir en wireshark
tcpdump -i tarjeta_red -v captura.cap -v
## Wireshark

No sacar output en la terminal  con errores y con `disown` cuándo cerremos terminal no se cierre wireshark --> wireshark captura.cap &> /dev/null & disown

- tshark -r captura.cap -Y "campo" 2> /dev/null
- Lo saca en JSON --> tshark -r captura.cap -Y "protocolo" -Tjson 2> /dev/null
- Transformar salida **HEXADECIMAL** a **DECIMAL** --> tshark -r captura.cap -Y "HTTP" -Tfields tcp.payload 2> /dev/null | xdd -ps -r

