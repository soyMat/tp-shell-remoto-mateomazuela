import socket
import threading
import ssl

from red import enviar_mensaje, recibir_mensaje
from seguridad import crear_bd, validar_usuario
from comandos import procesar_comando, preparar_raiz, RAIZ_SERVIDOR

HOST = "0.0.0.0"
PUERTO = 5000
MAX_CLIENTES = 5

clientes_activos = 0
lock_clientes = threading.Lock()


def atender_cliente(conn, addr):
    global clientes_activos

    print("se conecto:", addr)

    directorio_actual = RAIZ_SERVIDOR

    try:
        usuario = recibir_mensaje(conn)
        password = recibir_mensaje(conn)

        if usuario is None or password is None:
            return

        if validar_usuario(usuario, password):
            enviar_mensaje(conn, "ok\nbuenas! escribi help para ver los comandos.\n")
        else:
            enviar_mensaje(conn, "error: usuario o password incorrectos\n")
            return

        while True:
            comando = recibir_mensaje(conn)

            if comando is None:
                break

            if comando.strip() == "exit":
                enviar_mensaje(conn, "conexion cerrada\n")
                break

            respuesta, directorio_actual = procesar_comando(comando, directorio_actual)

            enviar_mensaje(conn, respuesta)

    except Exception as e:
        print("error con el cliente:", e)

    finally:
        conn.close()

        with lock_clientes:
            clientes_activos -= 1
            print("clientes activos:", clientes_activos)

        print("se desconecto:", addr)


crear_bd()
preparar_raiz()

contexto_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
contexto_ssl.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PUERTO))
server.listen(5)

print("server seguro escuchando en el puerto 5000...")

while True:
    socket_cliente, addr = server.accept()

    with lock_clientes:
        if clientes_activos >= MAX_CLIENTES:
            print("conexion rechazada, servidor lleno:", addr)
            socket_cliente.close()
            continue

        clientes_activos += 1
        print("clientes activos:", clientes_activos)

    try:
        conexion_ssl = contexto_ssl.wrap_socket(socket_cliente, server_side=True)

        hilo = threading.Thread(target=atender_cliente, args=(conexion_ssl, addr))
        hilo.start()

    except Exception as e:
        print("error iniciando ssl:", e)
        socket_cliente.close()

        with lock_clientes:
            clientes_activos -= 1