from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    db_url = os.environ.get("DB_url")
    return psycopg2.connect(db_url)

# Ruta principal: módulo de victimizacion
@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT entidad, viv, hogar, upm, renglon,
               tipo_delito, num_delito, nombre, apellido, perdida
        FROM modulo_victimizacion
    """)

    columnas = [desc[0] for desc in cur.description]
    datos = [dict(zip(columnas, fila)) for fila in cur.fetchall()]

    cur.close()
    conn.close()

    return render_template("index.html", datos=datos)

# Ruta extendida: registro y visualización de clientes
@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        nombre = request.form.get("nombre")
        fechaNacimiento = request.form.get("fechaNacimiento")

        if nombre and fechaNacimiento:
            try:
                cur.execute("""
                    INSERT INTO cliente (nombre, fechaNacimiento)
                    VALUES (%s, %s)
                """, (nombre, fechaNacimiento))
                conn.commit()
            except Exception as e:
                print("Error al insertar cliente:", e)

    cur.execute("SELECT idCliente, nombre, fechaNacimiento FROM cliente ORDER BY idCliente")
    columnas = [desc[0] for desc in cur.description]
    clientes = [dict(zip(columnas, fila)) for fila in cur.fetchall()]

    cur.close()
    conn.close()

    return render_template("clientes.html", clientes=clientes)

@app.route("/saludo")
def saludo():
    return "¡Hola desde Flask en Render!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
