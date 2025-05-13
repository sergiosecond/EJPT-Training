- 18 Most used DORKS
1. https://pentest-tools.com/information-gathering/google-hacking 

- Reverse shells NodeJS
1. [https://github.com/appsecco/vulnerable-apps/tree/master/node-reverse-shell](https://github.com/appsecco/vulnerable-apps/tree/master/node-reverse-shell) 

- Limpiar Dockers pegar en **.zshrz**

```bash
function cleandocker () {
        sudo docker rm $(sudo docker ps -a -q) -f
        sudo docker rmi $(sudo docker images -q) --force
        sudo docker volume rm $(sudo docker volume ls -q)
        sudo docker network rm $(sudo docker network ls -q )
} 
```
```bash
source .zshrc
```

- Función a pegar en la **.zshrc**  para copiar pueros extraídos --> **cliports**
> nmap -p- target -oA ***nombresalidanmap***
   Uso: cliports ***nombredesalidanmap.gmap***

```bash
cliports () {
	ports="$(cat $1 | grep -oP '\d{1,5}/open' | awk '{print $1}' FS='/' | xargs | tr ' ' ',')"
	ip_address="$(cat $1 | grep -oP '^Host: .* \(\)' | head -n 1 | awk '{print $2}' )"
	echo -e "\n[*] Extracting information ... \n" > extractPorts.tmp
	echo -e "\t[*] IP Address: $ip_address" >> extractPorts.tmp
	echo -e "\t[*] Open ports: $ports\n" >> extractPorts.tmp
	echo $ports | tr -d '\n' | xclip -sel clip
	echo -e "[*] Ports copied to clipboard\n" >> extractPorts.tmp
	cat extractPorts.tmp
	rm extractPorts.tmp
}
```


>Enumeramos puertos desde una máquina vulnerada

```bash
#!/bin/bash

for i in $(seq 1 254); do
	for port in 21 22 80 443 445 8080; do
		timeout 1 bash -c "echo '' > /dev/tcp/10.10.0.$i/$port" &>/dev/null && echo "[+] Host 10.10.0.$i - PORT $port - OPEN| &

	done
done; wait
```