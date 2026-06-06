import struct

def enviar_mensaje(sock, mensaje):
    datos = mensaje.encode("utf-8")
    tamanio = len(datos)

    # primero mando 4 bytes con el tamanio del mensaje
    sock.sendall(struct.pack("!I", tamanio))

    # despues mando el mensaje completo
    sock.sendall(datos)


def recibir_mensaje(sock):
    encabezado = recibir_completo(sock, 4)

    if not encabezado:
        return None

    tamanio = struct.unpack("!I", encabezado)[0]

    datos = recibir_completo(sock, tamanio)

    if not datos:
        return None

    return datos.decode("utf-8")


def recibir_completo(sock, cantidad):
    datos = b""

    while len(datos) < cantidad:
        parte = sock.recv(cantidad - len(datos))

        if not parte:
            return None

        datos += parte

    return datos