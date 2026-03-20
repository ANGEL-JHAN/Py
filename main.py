import sqlite3

conexion = sqlite3.connect("mi_base.db")
cursor = conexion.cursor()

# Crear tabla usuarios con contraseña
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    password TEXT
)
""")

conexion.commit()

# MENÚ
print("1. Registrarse")
print("2. Iniciar sesión")

opcion = input("Elige una opción: ")

# REGISTRO
if opcion == "1":
    nombre = input("Usuario: ")
    password = input("Contraseña: ")

    cursor.execute("INSERT INTO usuarios (nombre, password) VALUES (?, ?)", (nombre, password))
    conexion.commit()

    print("Usuario registrado ✅")

# LOGIN
elif opcion == "2":
    nombre = input("Usuario: ")
    password = input("Contraseña: ")

    cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (nombre, password))
    usuario = cursor.fetchone()

    if usuario:
        print("Login correcto 😎")
    else:
        print("Usuario o contraseña incorrectos ❌")

else:
    print("Opción inválida")

conexion.close()