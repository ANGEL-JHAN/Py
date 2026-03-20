from flask import Flask, render_template, request, redirect, url_for, session, make_response
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Conexión DB
def get_db():
    return sqlite3.connect("mi_base.db")

# Decorador para rutas protegidas
def login_required(f):
    def wrap(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Login/Registro
@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        accion = request.form["accion"]

        conexion = get_db()
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                password TEXT
            )
        """)

        if accion == "registrar":
            cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (usuario,))
            if cursor.fetchone():
                mensaje = "Usuario ya existe ❌"
            else:
                cursor.execute("INSERT INTO usuarios (nombre, password) VALUES (?, ?)", (usuario, password))
                conexion.commit()
                mensaje = "Registrado ✅"

        elif accion == "login":
            cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (usuario, password))
            if cursor.fetchone():
                session["usuario"] = usuario
                conexion.close()
                return redirect(url_for("panel"))
            else:
                mensaje = "Datos incorrectos ❌"

        conexion.close()

    return render_template("index.html", mensaje=mensaje)

# Panel usuarios
@app.route("/panel")
@login_required
def panel():
    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM usuarios")
    usuarios = cursor.fetchall()
    conexion.close()

    response = make_response(render_template("panel.html", usuario=session["usuario"], usuarios=usuarios))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))

# Canvas profesional
@app.route("/canvas_pro")
@login_required
def canvas_pro():
    return render_template("canvas_pro.html")

# Ejecutar app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)