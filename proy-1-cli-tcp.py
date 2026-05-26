import socket
import getpass

# aca tenes que poner la ip de tu vm servidor
IP = '192.168.56.10'
PUERTO = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((IP, PUERTO))
    print("conectado al server!")
    
    # pido los datos de login
    user = input("usuario: ")

    # getpass sirve para que no se vea lo que tipias
    password = getpass.getpass("pass: ")
    
    # junto el usuario y la pass y lo mando
    credenciales = user + " " + password
    cliente.send(credenciales.encode())
    
    # espero a ver si me deja entrar
    respuesta_login = cliente.recv(1024).decode()
    
    if respuesta_login.startswith("ok"):
        print("\nentraste bien!")

        # saco el ok y muestro el resto como bienvenida
        bienvenida = respuesta_login.replace("ok", "", 1)
        print(bienvenida)
        
        # empieza el bucle para mandar comandos
        while True:
            comando = input("shell> ")

            if comando == "":
                continue
                
            cliente.send(comando.encode())
            
            if comando == "exit":
                print("saliendo...")
                break
                
            # recibo lo que me contesta el servidor y lo imprimo
            respuesta = cliente.recv(4096).decode()
            print(respuesta, end="")

    else:
        # si me rechaza imprimo el error
        print("\nerror:", respuesta_login)
        
except Exception as e:
    print("no se pudo conectar:", e)

cliente.close()
