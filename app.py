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

# Login / Registro
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
                password TEXT,
                rol TEXT DEFAULT 'user'
            )
        """)

        if accion == "registrar":
            cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (usuario,))
            if cursor.fetchone():
                mensaje = "Usuario ya existe ❌"
            else:
                # Todos los nuevos usuarios son 'user' por defecto
                cursor.execute("INSERT INTO usuarios (nombre, password, rol) VALUES (?, ?, ?)", (usuario, password, 'user'))
                conexion.commit()
                mensaje = "Registrado ✅"

        elif accion == "login":
            cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (usuario, password))
            usuario_db = cursor.fetchone()
            if usuario_db:
                session["usuario"] = usuario
                session["rol"] = usuario_db[3]  # Guardamos el rol en la sesión
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

    # Obtener rol del usuario
    rol = session.get("rol", "user")

    if rol == "admin":
        cursor.execute("SELECT id, nombre, rol FROM usuarios")
    else:
        cursor.execute("SELECT id, nombre, rol FROM usuarios WHERE nombre=?", (session["usuario"],))

    usuarios = cursor.fetchall()
    conexion.close()

    return render_template("panel.html", usuario=session["usuario"], usuarios=usuarios, rol=rol)

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("rol", None)
    return redirect(url_for("index"))

# Canvas profesional
@app.route("/canvas_pro")
@login_required
def canvas_pro():
    return render_template("canvas_pro.html")

# Ejecutar app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)