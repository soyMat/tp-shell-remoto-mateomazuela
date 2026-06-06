import socket
import ssl
import getpass

from red import enviar_mensaje, recibir_mensaje

IP = "192.168.56.101"
PUERTO = 5000

contexto_ssl = ssl.create_default_context()

# como usamos certificado propio, desactivo la verificacion del certificado
contexto_ssl.check_hostname = False
contexto_ssl.verify_mode = ssl.CERT_NONE

socket_normal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente = contexto_ssl.wrap_socket(socket_normal, server_hostname=IP)

try:
    cliente.connect((IP, PUERTO))
    print("conectado al server seguro!")

    usuario = input("usuario: ")
    password = getpass.getpass("password: ")

    enviar_mensaje(cliente, usuario)
    enviar_mensaje(cliente, password)

    respuesta_login = recibir_mensaje(cliente)

    if respuesta_login is None:
        print("no se recibio respuesta del servidor")

    elif respuesta_login.startswith("ok"):
        bienvenida = respuesta_login.replace("ok", "", 1)
        print(bienvenida)

        while True:
            comando = input("shell> ")

            if comando == "":
                continue

            enviar_mensaje(cliente, comando)

            respuesta = recibir_mensaje(cliente)

            if respuesta is None:
                print("conexion cerrada por el servidor")
                break

            print(respuesta, end="")

            if comando.strip() == "exit":
                break

    else:
        print(respuesta_login)

except Exception as e:
    print("no se pudo conectar:", e)

finally:
    cliente.close()