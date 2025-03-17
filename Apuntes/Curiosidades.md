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

- Función a pegar en la **.zshrc**  para copiar pueros extraídos --> **cliports**
> nmap -p- target -oG ***nombresalidanmap***
   Uso: cliports ***nombredesalidanmap***

```bash
cliports () {
	ports="$(cat $1 | grep -oP '\d{1,5}/open' | awk '{print $1}' FS='/' | xargs | tr ' ' ',')"
	ip_address="$(cat $1 | grep -oP '^Host: .* \(\)' | head -n 1 | awk '{print $2}' )"
	echo -e "\n[*] Extracting information ... \n" > extractPorts. tmp
	echo -e "\t[*] IP Address: $ip_address" >> extractPorts.tmp
	echo -e "\t[*] Open ports: $ports\n" >> extractPorts.tmp
	echo $ports | tr -d '\n' | xclip -sel clip
	echo -e "[*] Ports copied to clipboard\n" >> extractPorts.tmp
	cat extractPorts. tmp
	rm extractPorts. tmp
}
```
