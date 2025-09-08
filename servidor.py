from flask import Flask, request, redirect, jsonify
import sqlite3 as sql
from utils import *
import os
# from mysql.connector import Error
# from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    rows = imoveis()
    imoveis = []
    for r in rows:
        imovel = {"id": r[0], "logradouro": r[1], "tipo_logradouro": r[2]}
        imoveis.append(imovel)

    return jsonify({"todos_imoveis": imoveis}), 200


@app.route("/imoveis/<int:imovel_id>", methods=["GET"])
def get_imovel(imovel_id):
    row = especifico(imovel_id)
    imovel = {"id": row[0][0], "logradouro": row[0][1], "tipo_logradouro": row[0][2]}
    return jsonify({"imovel": imovel}), 200


@app.route("/imoveis", methods=["POST"])
def add_imovel():
    data = request.get_json()
    imovel_id = data.get("id")
    logradouro = data.get("logradouro")
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")

    novo_id = add(imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)

    return jsonify({"imovel": {"id": novo_id, "logradouro": logradouro, "tipo_logradouro": tipo_logradouro}}), 201


@app.route("/imoveis/<int:imovel_id>", methods=["PUT"])
def update_imovel(imovel_id):
    data = request.get_json()
    logradouro = data.get("logradouro")
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")
    update(imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
    
    return jsonify({"imovel": {"id": imovel_id, "logradouro": logradouro, "tipo_logradouro": tipo_logradouro}}), 200


@app.route("/imoveis/<int:imovel_id>", methods=["DELETE"])
def remove_imovel(imovel_id):
    remove(imovel_id)
    return jsonify({"mensagem": "apagado com sucesso"}), 200


@app.route("/imoveis/tipo/<string:tipo>", methods=["GET"])
def listar_por_tipo(tipo):
    rows = tipo(tipo)
    for r in rows:
        imovel = {"id": r[0], "logradouro": r[1], "tipo": r[6]}
        imoveis.append(imovel)
    return jsonify({"tipo_imóvel": imoveis}), 200
    

@app.route("/imoveis/cidade<string:cidade>", methods=["GET"])
def listar_por_cidade(cidade):
    rows = city(cidade)
    for r in rows:
        imovel = {"id": r[0], "logradouro": r[1], "tipo_logradouro": r[2], "cidade": r[4]}
        imoveis.append(imovel)

    return jsonify({"tipo_imovel": imoveis}), 200

if __name__ == '__main__':
    app.run(debug=True)