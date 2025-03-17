+ Utilizaremos Docker para levantar los laboratorios
+ Los contenedores vienen sin tools instaladas

## Estructura DockerFIle

- SIEMPRE LLAMAREMOS AL ARCHIVO `Dockerfile`
- **FROM**: se utiliza para especificar la imagen base desde la cual se construirá la nueva imagen.
- **RUN**: se utiliza para ejecutar comandos en el interior del contenedor, como la instalación de paquetes o la configuración del entorno.
- **COPY**: se utiliza para copiar archivos desde el sistema host al interior del contenedor.
- **CMD**: se utiliza para especificar el comando que se ejecutará cuando se arranque el contenedor.


## Comandos docker

- Levantar docker:
1. sudo docker build -t primerdocker:v1 . 

- Descargar imagen de debian
1. docker pull debian:latest

- Arrancar docker en terminal interactiva, en segundo plano y  dándole un nombre
1. docker run -dit --name {NombreMNuevocontenedor} {imagen:etiqueta}

- Ejecutar container en una terminal
1. sudo docker exec -it 30c4c08dbf35 bash

- Parar docker
1. sudo docker stop {image}

- Borrar contenedores y me quito de vainas 1 imagen o todas las imágenes
1. sudo docker rm -f {image}
2. sudo docker rm $(sudo docker ps -a -q) -f

- Borrar imágenes
1. sudo docker rmi $(sudo docker images -q)

- Listar y borrar Volúmenes
1. sudo docker volume ls -q
2. sudo docker volume rm $(sudo docker volume ls -q)


- Borrar las imágenes a none
1. sudo docker rmi $(sudo docker images --filter="dangling=true" -q) -f
2

### Portforwarding

Si vulneran algún servicio de nuestra máquina expuesta, podemos hacer portforwarding para que caigan dentro del docker y no a la máquina real

- Dockerfile utilizado:
![[Pasted image 20250309135033.png]]

- sudo docker run -dit -p 80:8889 --name dockerportforwarding webserver
- Por le protocolo que queramos 
1. sudo docker run -p 53:53/udp mi_imagen

### Montura
Realiza lo mimso que COPY pero fuera del dockerfile

- docker run -v /home/usuario/datos:/datos mi_imagen
- solo lectura
1. docker run -v /home/usuario/datos:/datos:mi_imagen


### Levantar dockerCompose.yaml

- Sudo docker-compose up -d
- Ver logs 
1. sudo docker-compose logs