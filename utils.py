from flask import Flask, request
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
    print(imovel_id)
    imovel_especifico = cur.fetchall()
    return imovel_especifico

def add(imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisição):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'INSERT INTO imoveis (imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisição) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
    (imovel_id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisição)
    )
    novo_imovel = cur.fetchall()
    conn.commit()
    conn.close()
    
    return novo_imovel

def update(imovel_id, novo_logradouro, novo_tipo_logradouro, novo_bairro, novo_cidade, novo_cep, novo_tipo, novo_valor, novo_data_aquisição):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisição = %s WHERE id = %s ',
    (novo_logradouro, novo_tipo_logradouro, novo_bairro, novo_cidade, novo_cep, novo_tipo, novo_valor, novo_data_aquisição, imovel_id))
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

def tipo(tipo):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'SELECT * FROM imoveis WHERE tipo = %s ',
    (tipo, ))
    imoveis_tipo = cur.fetchall()
    return imoveis_tipo

def city(cidade):
    conn = connect_db()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
    'SELECT * FROM imoveis WHERE cidade = %s ',
    (cidade, ))
    imoveis_cidade = cur.fetchall()
    return imoveis_cidade
