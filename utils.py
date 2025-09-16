import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv('.cred')

config = {
    'host': os.getenv('DB_HOST', 'localhost'),  
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),  
    'database': os.getenv('DB_NAME', 'db_escola'),  
    'port': int(os.getenv('DB_PORT', 3306)),  
    'ssl_ca': os.getenv('SSL_CA_PATH')
}

def connect_db():
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        print(f"Erro: {err}")
        return None

def todos_imoveis():
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis")
    todos_imoveis = cur.fetchall()
    conn.close()
    return todos_imoveis

def especifico(imovel_id):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM imoveis WHERE id = %s; ', (imovel_id, ))
    imovel_especifico = cur.fetchall()
    return imovel_especifico

def add(logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', 
    (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
    )
    conn.commit()
    novo_id = cur.lastrowid
    conn.close()
    
    return novo_id

def update(imovel_id, novo_logradouro, novo_tipo_logradouro, novo_bairro, novo_cidade, novo_cep, novo_tipo, novo_valor, novo_data_aquisicao):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s ',
    (novo_logradouro, novo_tipo_logradouro, novo_bairro, novo_cidade, novo_cep, novo_tipo, novo_valor, novo_data_aquisicao, imovel_id))
    conn.commit()
    conn.close()

def remove(imovel_id):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'DELETE FROM imoveis WHERE id = %s ',
    (imovel_id,))
    conn.commit()
    conn.close()

def filtro_tipo(tipo):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'SELECT * FROM imoveis WHERE tipo = %s ',
    (tipo, ))
    imoveis_tipo = cur.fetchall()
    return imoveis_tipo

def filtro_city(cidade):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'SELECT * FROM imoveis WHERE cidade = %s ',
    (cidade, ))
    imoveis_cidade = cur.fetchall()
    return imoveis_cidade
