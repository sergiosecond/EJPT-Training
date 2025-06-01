
-----

## Fase de Escaneo
- Utilizar arpscan, ping, netdiscover y nmap -sn
```bash
sudo nmap -sn 192.168.1.0/24 -oA netscan 
sudo netdiscover -r red/24
sudo arp-scan --localnet --ignoredup -ITarjetaRed
```

## Fase de Enumeración
```bash
gobuster dir -u -w -b 404,403,301,400 -x php.php.bak,txt,txt.bak.html,htm,php
gobuster dir -u http://192.168.1.167 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -k -x ~,swp,txt,txt.bak,php,php.bak,jpg,bak,js,png,auth.log,log,config,json,git,sh,kdbx,db
gobuster vhost -u http://pl0t.nyx/ -w /home/kuser/cosas/repositorios/SecLists/Discovery/DNS/subdomains-top1million-110000.txt --append-domain | grep -v "400"
```

## Explotación
```bash
hydra -l butthead -P /usr/share/wordlists/rockyou.txt mysql://192.168.1.134 -I -F -t 20
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.182 http-post-form "/my_weblog/admin.php:username=admin&password=^PASS^:Incorrect username or password." -f -V

```

#### Windows
- Si conseguimos archyvo **sam** y **system**
```bash
samdump2 system.bak sam.bak
impacket-secretsdump -sam sam.bak -system system.bak LOCAL
```
## Comandos de Windows

- Saber el user
```power-shell
Get-LocalGroupMember -Group "Administrators"
```
- Por si nos preguntan los **Hotfix**
```Power-shell
(Get-Hotfix).Count
```
- Una vez ganado acceso Ver **Hotfixes**
```
enum_computers
enum_patches
# O en la shell, te da todos los parches
systeminfo
```


## Tips Exam

- Mejor no resetear el lab o la machine
- SI alguna tecla  falla, utilizar el **screen keyboard**
- Todas las redes serán **/24**
- Coger apuntes fuera de la MV


>Herramientas Recomendadas

● Nmap
● Dirb
● Nikto
● WPScan
● CrackMapExec
● The Metasploit Framework
● Searchsploit
● Hydra