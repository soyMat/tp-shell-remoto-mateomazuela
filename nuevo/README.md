# Proyecto: Shell Remoto Multihilo

Este es mi proyecto para el laboratorio de redes. Consiste en un sistema cliente-servidor hecho en Python usando sockets TCP y la libreria `threading`, para que puedan conectarse multiples clientes a la vez.

## Objetivo

El objetivo del proyecto es programar un Shell Remoto Multihilo. El cliente se conecta al servidor por medio de una red LAN virtual de VirtualBox y puede ejecutar comandos remotos programados sobre el servidor.

## Ambiente experimental

Para probar el proyecto se usaron dos maquinas virtuales en VirtualBox:

- VM1: Servidor
- VM2: Cliente

Configuracion de red:

- Adaptador 1: NAT, para acceso a internet.
- Adaptador 2: Red Solo-Anfitrion, para la comunicacion entre las dos VMs.

Ejemplo de IP usada:

- Servidor: `192.168.56.10`
- Puerto: `5000`

## Caracteristicas

- **Login:** tiene un sistema de autenticacion al entrar. Las contraseñas estan ocultas usando la libreria `getpass`.
- **Multihilo:** cada cliente que entra es manejado por un hilo distinto, asi el servidor no se traba.
- **Sockets TCP:** el cliente y el servidor se comunican usando sockets TCP.
- **Comandos:** el servidor interpreta comandos enviados por el cliente y devuelve la respuesta.

## Comandos disponibles

- `help`: muestra la ayuda.
- `pwd`: muestra el directorio actual del servidor.
- `mkdir <nombre>`: crea una carpeta.
- `ls`: lista archivos y carpetas.
- `ls <ruta>`: lista una ruta especifica.
- `ls -l`: lista archivos con detalles.
- `ls -lh`: lista archivos con detalles y tamaños legibles.
- `cat <archivo>`: muestra el contenido de un archivo.
- `exit`: cierra la conexion.

## Diagrama de la arquitectura

[Haz clic aqui para ver el diagrama de flujo del programa en Draw.io](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&layers=1&nav=1&dark=auto#G1kXnJpY866rruHQWGFLyG78zgCwemsJ6J)

## Como ejecutarlo

### 1. Ejecutar el servidor

En la maquina servidor iniciar:

```bash
python3 proy-1-srv-tcp.py
```

### 2. Ejecutar el cliente

En la maquina cliente iniciar:

```bash
python3 proy-1-cli-tcp.py
```

### 3. Iniciar sesion

Usar algun usuario valido, por ejemplo:

```text
usuario: mateo
contraseña: tuda
```

## Explicacion del funcionamiento

El servidor crea un socket TCP y queda escuchando en el puerto `5000`.

Cuando un cliente se conecta, el servidor acepta la conexion y crea un hilo nuevo con `threading.Thread`. De esta manera, cada cliente conectado se atiende por separado y el servidor puede seguir aceptando nuevas conexiones.

El cliente solo envia texto al servidor y muestra la respuesta recibida. La logica de los comandos esta en el servidor.

## Capturas de funcionamiento

### Servidor escuchando

![Servidor escuchando](capturas/prendiendo.png)

### Servidor confirmacion

![Servidor confirmacion](capturas/confirmacion.png)

### Cliente conectado e inicio de sesion

![Login correcto](capturas/confirmacion-entro.png)

### Comando help

![Comando help](capturas/login-y-help.png)

### Comando mkdir

![Comando mkdir](capturas/mkdir.png)

### Comando ls
![Comando ls](capturas/ls.png)

### Comandos ls -l 
![Comando mkdir y ls](capturas/ls-l.png)

### Comando ls -lh

![Comando ls -lh](capturas/ls-lh.png)

### Comando cat

![Comando cat](capturas/cat.png)

### Comando pwd

![Comando pwd](capturas/pwd.png)

## Archivos del proyecto

- `proy-1-srv-tcp.py`: archivo del servidor TCP multihilo.
- `proy-1-cli-tcp.py`: archivo del cliente TCP.
- `README.md`: documentacion del proyecto.
- `capturas/`: carpeta con las imagenes de funcionamiento.

