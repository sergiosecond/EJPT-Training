## DataLeaks

- https://hunter.io
- https://intelx.io -->Pago
- https://phonebook.cz
- [https://www.dehashed.com/](https://www.dehashed.com/)

Ver emails y social media --> clearbit extension chrome

- https://www.verifyemailaddress.org/
- https://pimeyes.com --> info reversa por imágenes
davidgrecas@gmail.com:Intelx,1023

## Enumerar Subdomains

### Reconocimiento pasivo

- Ctrf --> [https://github.com/UnaPibaGeek/ctfr](https://github.com/UnaPibaGeek/ctfr) (Es mejor herramienta)
- Sublist3r -d gestoria.com
### Reconocimiento activo

> Una vez averiguada  la tecnología, fuzzear por ahí --> php,js etc..
> Una buena wordlist es seclist/discovery/web-content/directory-list-2.3-medium.txt
### Gobuster  
1.  -s 200 --> para códigos de estado afirmativos
2. extensiones que quiero --> -x php,html,htm,txt ,php.bak lo que sea **.bak**
3. Añade un guión al final --> --add-slash
4. gobuster dir -u https://www.gestoriacoslada.com -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-110000.txt  --add-slash -b 403,404
5. gobuster dir -u https://www.gestoriacoslada.com -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-110000.txt  -x html -s 200 -b ' '
6. Subdominios --> gobuster vhost -u https://www.gestoriacoslada.com -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-110000.txt 

###  wfuzz 
- Escaneamos directorios, parámetros, solicitudes GET y POST
1. No sacar esos códigos de estado  --> 
	- wfuzz -c --hc=404,400,403 -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.valvonta.es" https://valvonta.es
2. -L --> seguir redirecciones
3. Subdomains --> Enseñar esos códigos de estado -->  
- wfuzz -c --sc=200,302,500 -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.valvonta.es" https://valvonta.es

4. Fuzzing Directories-->
- wfuzz -c --hc=301,404,400,403 -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-5000.txt https://valvonta.es/FUZZ

4. fuzizng extensión html -->
- wfuzz -c --hc=404,400,403 -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-5000.txt https://valvonta.es/FUZZ.html 

4. Fuzzing a extensión que digas --> 
- wfuzz -c --hc=404,400,403  -z html.php,list  -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-5000.txt https://valvonta.es/FUZZ.html 

4. Fuzzear los id a y fijarnos en las palabras o characteres que sea iguales en el `response ` -->  
- wfuzz -c --hc=404,400,403 -z range,1-2000 'https://valvonta.es/product_id=FUZZ

1. Ocultar lo que encuentre con 6154 palabras y filtar la respuesta diferente --> 
- wfuzz -c --hw=6154 --hc=404,400,403 -z range,1-2000 'https://valvonta.es/product_id=FUZZ
### ffuf (El repo tiene más opciones que el binario de kali)
- Sólo coge los códigos 200 a 200 threads (10 por default)
 ./ffuf -c -t 200 --mc 200  -w /usr/share/wordlists/dirb/common.txt -u https://valvonta.es/FUZZ/
- Fuzzea los métodos permitidos 
```bash
ffuf -u http://localhost:8888/workshop/api/shop/products -w /usr/share/SecLists/Fuzzing/http-request-methods.txt -X FUZZ  -mc 401,200
```

## Una vez en la web - Reconocimiento de tecnologías

- https://webcf.waybackmachine.org/
- https://web.archive.org/
- Joomla - Joomscan https://github.com/OWASP/joomscan.git
- whatweb hola.com
- Wappalyzer --> extensión Chrome
-  [https://builtwith.com/](https://builtwith.com/)