from flask import Flask
import sqlite3
import hashlib

app = Flask(__name__)

DATABASE = "usuarios.db"

# Integrantes del grupo
usuarios = [
    ("Cristobal", "123456"),
    ("Francisco", "654321"),
    ("user", "user")
]


def crear_bd():

    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        password TEXT
    )
    """)

    conexion.commit()

    for usuario, password in usuarios:

        hash_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            cursor.execute(
                "INSERT INTO usuarios(usuario,password) VALUES(?,?)",
                (usuario, hash_password)
            )

        except sqlite3.IntegrityError:
            pass

    conexion.commit()
    conexion.close()


def validar_usuario(usuario, password):

    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    hash_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND password=?",
        (usuario, hash_password)
    )

    resultado = cursor.fetchone()

    conexion.close()

    return resultado


@app.route("/")
def inicio():

    return """
    <h1>Examen DRY7122</h1>

    <h2>Servidor funcionando correctamente.</h2>

    <p>Base de datos SQLite creada.</p>

    <p>Puerto 7500.</p>
    """


if __name__ == "__main__":

    crear_bd()

    print("\n===== VALIDACIÓN DE USUARIO =====\n")

    usuario = input("Usuario: ")

    password = input("Contraseña: ")

    if validar_usuario(usuario, password):

        print("\nAcceso Correcto\n")

    else:

        print("\nAcceso Denegado\n")

    app.run(host="0.0.0.0", port=7500)