import sqlite3
import hashlib
import os

BASE_DATOS = "usuarios.db"


def crear_bd():
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        usuario TEXT PRIMARY KEY,
        salt TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()


def generar_salt():
    return os.urandom(16).hex()


def crear_hash(password, salt):
    texto = salt + password
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def registrar_usuario(usuario, password):
    salt = generar_salt()
    password_hash = crear_hash(password, salt)

    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, salt, password_hash) VALUES (?, ?, ?)",
            (usuario, salt, password_hash)
        )

        conexion.commit()
        print("usuario creado correctamente")

    except sqlite3.IntegrityError:
        print("ese usuario ya existe")

    conexion.close()


def validar_usuario(usuario, password):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT salt, password_hash FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    fila = cursor.fetchone()
    conexion.close()

    if fila is None:
        return False

    salt = fila[0]
    hash_guardado = fila[1]

    hash_ingresado = crear_hash(password, salt)

    return hash_ingresado == hash_guardado