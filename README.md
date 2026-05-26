# Proyecto: Shell Remoto Multihilo

Este es mi proyecto para el laboratorio de redes. Consiste en un sistema cliente-servidor hecho en Python usando Sockets TCP y la libreria threading para que puedan conectarse multiples clientes a la vez.

## Caracteristicas
- **Login:** Tiene un sistema de autenticacion al entrar. Las contraseñas estan ocultas usando la libreria `getpass`. Agregue a mis compañeros de clase en la lista de usuarios.
- **Multihilo:** Cada cliente que entra es manejado por un hilo distinto, asi el servidor no se traba.
- **Comandos:** - `help`: Muestra la ayuda.
  - `mkdir`: Crea carpetas.
  - `ls`: Soporta comandos nativos pasandole parametros a Linux por debajo (como `ls -l` o `ls -lh`).

## Diagrama de la arquitectura
[Haz clic aqui para ver el diagrama de flujo del programa en Draw.io](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&dark=auto#G1ScLsl_wlV1biMt02NpqP4z0vj5coICF8)

## Como ejecutarlo
1. En la maquina servidor iniciar: `python3 proy-1-srv-tcp.py`
2. En la maquina cliente iniciar: `python3 proy-1-cli-tcp.py`
3. Usar algun usuario valido, por ejemplo `mateo` y la contraseña `tuda`.