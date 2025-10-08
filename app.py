from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    db_url = os.environ.get("DB_URL")
    return psycopg2.connect(db_url)

@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nombre, calificacion FROM sda_tabla")
    datos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", datos=datos)

@app.route("/saludo")
def saludo():
    return "¡Hola desde Flask en Render!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)