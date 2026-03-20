from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Función para conectar a la base de datos
def get_db():
    return sqlite3.connect("mi_base.db")

# Página principal: login / registro
@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""

    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        accion = request.form["accion"]

        conexion = get_db()
        cursor = conexion.cursor()

        # Crear tabla si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            password TEXT
        )
        """)

        # REGISTRO
        if accion == "registrar":
            cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (usuario,))
            if cursor.fetchone():
                mensaje = "Usuario ya existe ❌"
            else:
                cursor.execute("INSERT INTO usuarios (nombre, password) VALUES (?, ?)", (usuario, password))
                conexion.commit()
                mensaje = "Registrado ✅"

        # LOGIN
        elif accion == "login":
            cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (usuario, password))
            usuario_db = cursor.fetchone()

            if usuario_db:
                session["usuario"] = usuario
                conexion.close()
                return redirect(url_for("panel"))
            else:
                mensaje = "Datos incorrectos ❌"

        conexion.close()

    return render_template("index.html", mensaje=mensaje)

# PANEL DE USUARIO
@app.route("/panel")
def panel():
    if "usuario" in session:
        return render_template("panel.html", usuario=session["usuario"])
    else:
        return redirect(url_for("index"))

# CERRAR SESIÓN
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))

# SOLO se ejecuta si es local
if __name__ == "__main__":
    app.run()
