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
    data = sql.connect('banco.db')
    cur = data.cursor()
    cur.execute(
    'INSERT INTO imoveis (imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisição) VALUES (?,?,?,?,?,?,?,?,?)', (imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisição)
    )
    novo_imovel = cur.fetchall()
    data.commit()
    data.close()
    
    return novo_imovel

# def update():

# def remove():

# def type():

# def city():

