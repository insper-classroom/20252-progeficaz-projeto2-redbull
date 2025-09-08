from flask import Flask, request, redirect, jsonify
import sqlite3 as sql
from utils import connect_sql
import os
from mysql.connector import Error
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/imoveis", metthot=["GET"])
def listar_imoveis():
    conn = connect_sql()
    cur = conn.cursor()
    cur.execute("SELECT id, logradouro, tipo_logradouro FROM imoveis")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    imoveis = []
    for r in rows:
        imovel = {"id": r[0], "logradouro": r[1], "tipo_logradouro": r[2]}
        imoveis.append(imovel)

    return jsonify({"todos_imoveis": imoveis}), 200


@app.route("/imoveis/<int:imovel_id", method=["GET"])
def get_imovel(imovel_id):
    conn = connect_sql()
    cur = conn.cursor()
    cur.execute("SELECT id, logradouro, tipo_logradouro FROM imoveis WHERE id=?", (imovel_id))
    row = cur.ferchone()
    cur.close()
    conn.close()
    imovel = {"id": row[0], "logradouro": row[1], "tipo_logradouro": row[2]}
    return jsonify({"imovel": imovel}), 200

if __name__ == '__main__':
    app.run(debug=True)