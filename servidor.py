from flask import Flask, request, redirect
import views
import sqlite3 as sql
# import mysql.connector   # ou o driver que você estiver usando

app = Flask(__name__)

# def connect_db():
#     """Função que retorna a conexão real com o banco."""
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="senha",
#         database="imobiliaria"
#     )

# @app.route("/imoveis/<int:imovel_id>")
# def get_imovel(imovel_id):
#     conn = connect_db()
#     cursor = conn.cursor()

#     # Busca um único imóvel pelo id
#     cursor.execute(
#         "SELECT id, logradouro, tipo_logradouro FROM imoveis WHERE id = %s",
#         (imovel_id,)
#     )
#     row = cursor.fetchone()

#     cursor.close()
#     conn.close()

#     if row:
#         imovel = {
#             "id": row[0],
#             "logradouro": row[1],
#             "tipo_logradouro": row[2],
#         }
#         return jsonify({"imovel": imovel}), 200
#     else:
#         return jsonify({"error": "Imóvel não encontrado"}), 404