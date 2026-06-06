from pathlib import Path
import os
import stat
import time

RAIZ_SERVIDOR = Path("archivos_servidor").resolve()


def preparar_raiz():
    RAIZ_SERVIDOR.mkdir(exist_ok=True)


def ruta_segura(directorio_actual, ruta_usuario):
    actual = Path(directorio_actual)

    if ruta_usuario == "":
        nueva_ruta = actual
    else:
        nueva_ruta = (actual / ruta_usuario).resolve()

    try:
        nueva_ruta.relative_to(RAIZ_SERVIDOR)
        return nueva_ruta
    except ValueError:
        return None


def tamanio_legible(tamanio):
    unidades = ["B", "K", "M", "G", "T"]
    valor = float(tamanio)

    for unidad in unidades:
        if valor < 1024:
            return f"{valor:.1f}{unidad}"
        valor = valor / 1024

    return f"{valor:.1f}P"


def permisos_texto(ruta):
    modo = ruta.stat().st_mode

    if ruta.is_dir():
        tipo = "d"
    else:
        tipo = "-"

    permisos = ""

    for quien in [
        stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
        stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
        stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH
    ]:
        permisos += "rwx"[[stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
                           stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
                           stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH].index(quien) % 3] if modo & quien else "-"

    return tipo + permisos


def listar_simple(ruta):
    elementos = sorted(ruta.iterdir())

    if not elementos:
        return "directorio vacio\n"

    nombres = []

    for elemento in elementos:
        nombres.append(elemento.name)

    return "\n".join(nombres) + "\n"


def listar_detallado(ruta, legible=False):
    elementos = sorted(ruta.iterdir())

    if not elementos:
        return "directorio vacio\n"

    lineas = []

    for elemento in elementos:
        datos = elemento.stat()
        permisos = permisos_texto(elemento)

        if legible:
            tamanio = tamanio_legible(datos.st_size)
        else:
            tamanio = str(datos.st_size)

        fecha = time.strftime("%Y-%m-%d %H:%M", time.localtime(datos.st_mtime))

        lineas.append(f"{permisos} {tamanio:>8} {fecha} {elemento.name}")

    return "\n".join(lineas) + "\n"


def procesar_comando(comando, directorio_actual):
    partes = comando.strip().split()

    if len(partes) == 0:
        return "\n", directorio_actual

    cmd = partes[0]

    if cmd == "help":
        ayuda = """
Comandos disponibles:

help                 muestra esta ayuda
pwd                  muestra el directorio actual
cd <carpeta>         cambia de directorio
mkdir <nombre>       crea una carpeta
ls                   lista archivos y carpetas
ls <ruta>            lista una ruta
ls -l                lista con detalles
ls -lh               lista con detalles y tamanio legible
cat <archivo>        muestra el contenido de un archivo
exit                 cierra la conexion
"""
        return ayuda, directorio_actual

    elif cmd == "pwd":
        return str(Path(directorio_actual)) + "\n", directorio_actual

    elif cmd == "cd":
        if len(partes) != 2:
            return "uso correcto: cd <carpeta>\n", directorio_actual

        nueva_ruta = ruta_segura(directorio_actual, partes[1])

        if nueva_ruta is None:
            return "acceso denegado: no se puede salir de la raiz del servidor\n", directorio_actual

        if not nueva_ruta.exists():
            return "error: la ruta no existe\n", directorio_actual

        if not nueva_ruta.is_dir():
            return "error: no es un directorio\n", directorio_actual

        return "directorio cambiado correctamente\n", nueva_ruta

    elif cmd == "mkdir":
        if len(partes) != 2:
            return "uso correcto: mkdir <nombre>\n", directorio_actual

        nueva_carpeta = ruta_segura(directorio_actual, partes[1])

        if nueva_carpeta is None:
            return "acceso denegado: ruta no permitida\n", directorio_actual

        try:
            nueva_carpeta.mkdir()
            return "carpeta creada correctamente\n", directorio_actual

        except FileExistsError:
            return "error: la carpeta ya existe\n", directorio_actual

        except Exception as e:
            return "error al crear carpeta: " + str(e) + "\n", directorio_actual

    elif cmd == "ls":
        legible = False
        detallado = False
        ruta_pedida = ""

        for parte in partes[1:]:
            if parte == "-l":
                detallado = True
            elif parte == "-lh":
                detallado = True
                legible = True
            else:
                ruta_pedida = parte

        ruta = ruta_segura(directorio_actual, ruta_pedida)

        if ruta is None:
            return "acceso denegado: ruta no permitida\n", directorio_actual

        if not ruta.exists():
            return "error: la ruta no existe\n", directorio_actual

        if ruta.is_file():
            return ruta.name + "\n", directorio_actual

        if detallado:
            return listar_detallado(ruta, legible), directorio_actual
        else:
            return listar_simple(ruta), directorio_actual

    elif cmd == "cat":
        if len(partes) != 2:
            return "uso correcto: cat <archivo>\n", directorio_actual

        ruta = ruta_segura(directorio_actual, partes[1])

        if ruta is None:
            return "acceso denegado: ruta no permitida\n", directorio_actual

        if not ruta.exists():
            return "error: el archivo no existe\n", directorio_actual

        if not ruta.is_file():
            return "error: no es un archivo\n", directorio_actual

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()

            if contenido == "":
                return "\n", directorio_actual

            return contenido + "\n", directorio_actual

        except Exception as e:
            return "error al leer archivo: " + str(e) + "\n", directorio_actual

    else:
        return "comando no reconocido. escribi help\n", directorio_actual
