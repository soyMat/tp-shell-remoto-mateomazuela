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
                conn.send("ok".encode())
            else:
                conn.send("usuario o pass incorrectos".encode())
                conn.close()
                return
        else:
            conn.send("formato raro".encode())
            conn.close()
            return

        # le mando el msj de bienvenida
        conn.send("\nbuenas! escribi 'help' para ver los comandos.\n".encode())

        # aca arranca el shell
        while True:
            msg = conn.recv(1024).decode().strip()
            if not msg or msg == "exit":
                break

            partes = msg.split()
            cmd = partes[0]
            resp = ""

            if cmd == "help":
                resp = "Comandos:\n help - muestra esta lista\n mkdir <nombre> - crea una carpeta\n ls - lista archivos solos\n ls -l - lista con detalles\n ls -lh - lista detalles y tamaños legibles\n exit - cerrar\n"
                
            elif cmd == "mkdir":
                if len(partes) > 1:
                    carpeta = partes[1]
                    try:
                        os.mkdir(carpeta)
                        resp = "carpeta '" + carpeta + "' creada piola.\n"
                    except:
                        resp = "hubo un error al crear, capaz ya existe.\n"
                else:
                    resp = "te falto poner el nombre de la carpeta.\n"

            elif cmd == "ls":
                try:
                    # le paso directamente la lista a linux para que lo corra
                    resultado = subprocess.run(partes, capture_output=True, text=True)
                    resp = resultado.stdout
                    if resultado.stderr:
                        resp = resp + resultado.stderr
                except:
                    resp = "fallo el comando ls.\n"

            else:
                resp = "no conozco ese comando.\n"

            # por si no devolvio nada, le mando un salto de linea para que no se trabe
            if resp == "":
                 resp = "\n"
                 
            conn.send(resp.encode())

    except Exception as e:
        print("error con el cliente:", e)
        
    print("se desconecto:", addr)
    conn.close()

# configuro el server tcp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000))
server.listen(5)
print("server escuchando en el puerto 5000...")

while True:
    conn, addr = server.accept()
    # creo un hilo por cada cliente que entra
    hilo = threading.Thread(target=atender_cliente, args=(conn, addr))
    hilo.start()
