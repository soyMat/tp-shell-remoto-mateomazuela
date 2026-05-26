import socket
import threading
import subprocess
import os

# diccionario con los usuarios de mis compañeros
usuarios_validos = {
    "jeremias": "tuda",
    "luca": "tuda",
    "marcos": "tuda",
    "sebastian": "tuda",
    "guillermo": "tuda",
    "lucas": "tuda",
    "abigail": "tuda",
    "mateo": "tuda",
    "admin": "1234" # dejo este por las dudas para probar rapido
}

def atender_cliente(conn, addr):
    print("se conecto:", addr)
    
    try:
        # recibo los datos y los separo
        datos = conn.recv(1024).decode().split()
        
        if len(datos) == 2:
            user = datos[0]
            password = datos[1]
            
            # me fijo si esta en la lista y si coincide la pass
            if user in usuarios_validos and usuarios_validos[user] == password:
                # mando ok y bienvenida juntos para que no se mezcle despues
                conn.send("ok\nbuenas! escribi 'help' para ver los comandos.\n".encode())
            else:
                conn.send("usuario o pass incorrectos".encode())
                conn.close()
                return
        else:
            conn.send("formato raro".encode())
            conn.close()
            return

        # aca arranca el shell
        while True:
            msg = conn.recv(1024).decode().strip()

            if not msg or msg == "exit":
                break

            partes = msg.split()
            cmd = partes[0]
            resp = ""

            if cmd == "help":
                resp = """
Comandos disponibles:

help              muestra esta ayuda
pwd               muestra el directorio actual
mkdir <nombre>    crea una carpeta
ls                lista archivos y carpetas
ls <ruta>         lista una ruta
ls -l             lista con detalles
ls -lh            lista con detalles y tamanios legibles
cat <archivo>     muestra el contenido de un archivo
exit              cierra la conexion
"""

            elif cmd == "pwd":
                resp = os.getcwd() + "\n"
                
            elif cmd == "mkdir":
                if len(partes) == 2:
                    carpeta = partes[1]
                    try:
                        os.mkdir(carpeta)
                        resp = "carpeta '" + carpeta + "' creada correctamente.\n"
                    except FileExistsError:
                        resp = "error: la carpeta ya existe.\n"
                    except:
                        resp = "hubo un error al crear la carpeta.\n"
                else:
                    resp = "uso correcto: mkdir <nombre>\n"

            elif cmd == "ls":
                try:
                    # solo dejo ejecutar ls con sus parametros
                    resultado = subprocess.run(partes, capture_output=True, text=True)
                    resp = resultado.stdout

                    if resultado.stderr:
                        resp = resp + resultado.stderr

                except:
                    resp = "fallo el comando ls.\n"

            elif cmd == "cat":
                if len(partes) == 2:
                    try:
                        # solo dejo ejecutar cat con un archivo
                        resultado = subprocess.run(partes, capture_output=True, text=True)
                        resp = resultado.stdout

                        if resultado.stderr:
                            resp = resp + resultado.stderr

                    except:
                        resp = "fallo el comando cat.\n"
                else:
                    resp = "uso correcto: cat <archivo>\n"

            else:
                resp = "no conozco ese comando. escribi 'help'.\n"

            # por si no devolvio nada, mando un salto de linea
            if resp == "":
                resp = "\n"
                 
            conn.send(resp.encode())

    except Exception as e:
        print("error con el cliente:", e)
        
    print("se desconecto:", addr)
    conn.close()


# configuro el server tcp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# esto ayuda cuando reinicio el server y el puerto queda ocupado
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('0.0.0.0', 5000))
server.listen(5)

print("server escuchando en el puerto 5000...")

while True:
    conn, addr = server.accept()

    # creo un hilo por cada cliente que entra
    hilo = threading.Thread(target=atender_cliente, args=(conn, addr))
    hilo.start()
