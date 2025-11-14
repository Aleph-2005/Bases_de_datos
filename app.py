from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    db_url = os.environ.get("DB_url")
    return psycopg2.connect(db_url)

# Ruta principal: módulo de victimizacion
@app.route("/")
@app.route("/clientes")
def clientes():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT idCliente, nombre, fechaNacimiento FROM cliente ORDER BY idCliente")
        columnas = [desc[0] for desc in cur.description]
        clientes = [dict(zip(columnas, fila)) for fila in cur.fetchall()]

        cur.close()
        conn.close()

        return render_template("clientes.html", clientes=clientes)

    except Exception as e:
        return f"Error al cargar clientes: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
