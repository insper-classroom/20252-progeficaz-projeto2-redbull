import sqlite3 as sql

def imoveis():
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    """SELECT * FROM imoveis"""
    )
    todos_imoveis = cur.fetchall()
    return todos_imoveis

def especifico(imovel_id):
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    'SELECT * FROM imoveis WHERE id = ? ',
    (imovel_id, ))
    imovel_especifico = cur.fetchall()
    return imovel_especifico

def add(imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisição):
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    'INSERT INTO imoveis (imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisição) VALUES (?,?,?,?,?,?,?,?,?)', 
    (imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisição)
    )
    novo_imovel = cur.fetchall()
    data.commit()
    data.close()
    
    return novo_imovel

def update(imovel_id, novo_logradouro, novo_tipo_logradouro, novo_bairro, novo_cidade, novo_cep, novo_tipo, novo_valor, novo_data_aquisição):
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    'UPDATE imoveis SET logradouro = ?, tipo_logradouro = ?, bairro = ?, cidade = ?, cep = ?, tipo = ?, valor = ?, data_aquisição = ? WHERE id = ? ',
    (novo_logradouro, novo_tipo_logradouro, novo_bairro, novo_cidade, novo_cep, novo_tipo, novo_valor, novo_data_aquisição, imovel_id))
    data.commit()
    data.close()

def remove(imovel_id):
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    'DELETE FROM imoveis WHERE id = ? ',
    (imovel_id,))
    data.commit()
    data.close()

# DUVIDA: Oque ele quer das duas últimas funções? (filtrar ou order by) --- qualquer coisa alterar arquivo do pyteste também

# Funções de filtro
def tipo(tipo):
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    'SELECT * FROM imoveis WHERE tipo = ? ',
    (tipo, ))
    imoveis_tipo = cur.fetchall()
    return imoveis_tipo

def city(cidade):
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    'SELECT * FROM imoveis WHERE cidade = ? ',
    (cidade, ))
    imoveis_cidade = cur.fetchall()
    return imoveis_cidade

# Funções de ordem 
def tipo():
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    'SELECT * FROM imoveis ORDER BY tipo ASC ')
    imoveis_tipo = cur.fetchall()
    return imoveis_tipo

def city():
    data = sql.connect('imoveis.sql')
    cur = data.cursor()
    cur.execute(
    'SELECT * FROM imoveis ORDER BY cidade ASC ')
    imoveis_cidade = cur.fetchall()
    return imoveis_cidade
