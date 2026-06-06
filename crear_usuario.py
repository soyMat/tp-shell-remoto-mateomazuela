import getpass
from seguridad import crear_bd, registrar_usuario

crear_bd()

print("crear usuario para el shell remoto")

usuario = input("usuario: ")
password = getpass.getpass("password: ")

registrar_usuario(usuario, password)