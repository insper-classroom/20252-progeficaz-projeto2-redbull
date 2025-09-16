from flask import Flask, request, jsonify
import sqlite3 as sql
from utils import *

app = Flask(__name__)

@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    rows = todos_imoveis()
    imoveis = []
    for r in rows:
        imovel = {
            "id": r[0],
            "logradouro": r[1],
            "tipo_logradouro": r[2],
            "bairro": r[3],
            "cidade": r[4],
            "cep": r[5],
            "tipo": r[6],
            "valor": r[7],
            "data_aquisicao": r[8]
        }
        acoes = {
            "editar": f"/imoveis/{r[0]}",
            "adicionar": "/imoveis",
            "deletar": f"/imoveis/{r[0]}",
            "filtrar_por_cidade": f"/imoveis/cidade/{r[4]}",
            "filtrar_por_tipo": f"/imoveis/tipo/{r[6]}"
        }
        imoveis.append({"imovel": imovel, "acoes": acoes})
    if len(imoveis) == 0:
        return jsonify({"erro": "Nenhum imovel encontrado"}), 404
    return jsonify({"todos_imoveis": imoveis}), 200


@app.route("/imoveis/<int:imovel_id>", methods=["GET"])
def get_imovel(imovel_id):
    row = especifico(imovel_id)
    if not row:
        return jsonify({"erro": f"Imovel com id {imovel_id} nao encontrado"}), 404
    imovel = {
        "id": row[0][0],
        "logradouro": row[0][1],
        "tipo_logradouro": row[0][2],
        "bairro": row[0][3],
        "cidade": row[0][4],
        "cep": row[0][5],
        "tipo": row[0][6],
        "valor": row[0][7],
        "data_aquisicao": row[0][8]
    }
    acoes = {
        "editar": f"/imoveis/{row[0][0]}",
        "adicionar": "/imoveis",
        "deletar": f"/imoveis/{row[0][0]}",
        "filtrar_por_cidade": f"/imoveis/cidade/{row[0][4]}",
        "filtrar_por_tipo": f"/imoveis/tipo/{row[0][6]}"
    }
    return jsonify({"imovel": imovel, "acoes": acoes}), 200


@app.route("/imoveis", methods=["POST"])
def add_imovel():
    data = request.get_json()
    logradouro = data.get("logradouro")
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")

    novo_id = add(logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)

    imovel = {
        "id": novo_id,
        "logradouro": logradouro,
        "tipo_logradouro": tipo_logradouro,
        "bairro": bairro,
        "cidade": cidade,
        "cep": cep,
        "tipo": tipo,
        "valor": valor,
        "data_aquisicao": data_aquisicao
    }
    acoes = {
        "editar": f"/imoveis/{novo_id}",
        "adicionar": "/imoveis",
        "deletar": f"/imoveis/{novo_id}",
        "filtrar_por_cidade": f"/imoveis/cidade/{cidade}",
        "filtrar_por_tipo": f"/imoveis/tipo/{tipo}"
    }
    return jsonify({"imovel": imovel, "acoes": acoes}), 201


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

    imovel = {
        "id": imovel_id,
        "logradouro": logradouro,
        "tipo_logradouro": tipo_logradouro,
        "bairro": bairro,
        "cidade": cidade,
        "cep": cep,
        "tipo": tipo,
        "valor": valor,
        "data_aquisicao": data_aquisicao
    }
    acoes = {
        "editar": f"/imoveis/{imovel_id}",
        "adicionar": "/imoveis",
        "deletar": f"/imoveis/{imovel_id}",
        "filtrar_por_cidade": f"/imoveis/cidade/{cidade}",
        "filtrar_por_tipo": f"/imoveis/tipo/{tipo}"
    }
    return jsonify({"imovel": imovel, "acoes": acoes}), 200


@app.route("/imoveis/<int:imovel_id>", methods=["DELETE"])
def remove_imovel(imovel_id):
    remove(imovel_id)
    acoes = {
        "adicionar": "/imoveis"
    }
    return jsonify({"mensagem": "Apagado com sucesso", "acoes": acoes}), 200


@app.route("/imoveis/tipo/<string:tipo>", methods=["GET"])
def listar_por_tipo(tipo):
    rows = filtro_tipo(tipo)
    if not rows:
        return jsonify({"erro": f"Nao há imoveis do tipo '{tipo}'"}), 404
    imoveis = []
    for r in rows:
        imovel = {
            "id": r[0],
            "logradouro": r[1],
            "tipo_logradouro": r[2],
            "bairro": r[3],
            "cidade": r[4],
            "cep": r[5],
            "tipo": r[6],
            "valor": r[7],
            "data_aquisicao": r[8]
        }
        acoes = {
            "editar": f"/imoveis/{r[0]}",
            "adicionar": "/imoveis",
            "deletar": f"/imoveis/{r[0]}",
            "filtrar_por_cidade": f"/imoveis/cidade/{r[4]}",
            "filtrar_por_tipo": f"/imoveis/tipo/{r[6]}"
        }
        imoveis.append({"imovel": imovel, "acoes": acoes})
    return jsonify({"tipo_imovel": imoveis}), 200


@app.route("/imoveis/cidade/<string:cidade>", methods=["GET"])
def listar_por_cidade(cidade):
    rows = filtro_city(cidade)
    if not rows:
        return jsonify({"erro": f"Nao ha imoveis na cidade '{cidade}'"}), 404
    imoveis = []
    for r in rows:
        imovel = {
            "id": r[0],
            "logradouro": r[1],
            "tipo_logradouro": r[2],
            "bairro": r[3],
            "cidade": r[4],
            "cep": r[5],
            "tipo": r[6],
            "valor": r[7],
            "data_aquisicao": r[8]
        }
        acoes = {
            "editar": f"/imoveis/{r[0]}",
            "adicionar": "/imoveis",
            "deletar": f"/imoveis/{r[0]}",
            "filtrar_por_cidade": f"/imoveis/cidade/{r[4]}",
            "filtrar_por_tipo": f"/imoveis/tipo/{r[6]}"
        }
        imoveis.append({"imovel": imovel, "acoes": acoes})
    return jsonify({"cidade_imoveis": imoveis}), 200


if __name__ == '__main__':
    app.run(debug=True)
