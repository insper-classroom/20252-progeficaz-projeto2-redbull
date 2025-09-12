import pytest
from unittest.mock import patch, MagicMock
from servidor import app
from utils import *

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("servidor.todos_imoveis")  
def test_imoveis(mock_todos_imoveis, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (4, "Leri", "Rua", "Horto", "Salvador", "88888", "casa", 105000, "2007-05-17"),
        (8, "Carolina", "Avenida", "Itaim", "Sao Paulo", "44444", "apartamento", 105000, "2025-05-17"),
    ]

    mock_todos_imoveis.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200

    expected_response = {
        "todos_imoveis": [
            {"id": 4, "logradouro": "Leri", "tipo_logradouro": "Rua", "bairro": "Horto", "cidade": "Salvador", "cep": "88888", "tipo": "casa", "valor": 105000, "data_aquisicao": "2007-05-17"},
            {"id": 8, "logradouro": "Carolina", "tipo_logradouro": "Avenida", "bairro": "Itaim", "cidade": "Sao Paulo", "cep": "44444", "tipo": "apartamento", "valor": 105000, "data_aquisicao": "2025-05-17"},
        ]
    }
    assert response.get_json() == expected_response

@patch("servidor.get_imovel")
def test_especifico(mock_get_imovel, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = (8, "Carolina", "Avenida")

    mock_get_imovel.return_value = mock_conn

    response = client.get("/imoveis/8")

    assert response.status_code == 200

    expected_response = expected_response = {
        "imovel": {
            "id": 8,
            "logradouro": "Carolina",
            "tipo_logradouro": "Avenida"
        }
    }

    assert response.get_json() == expected_response

@patch("servidor.add_imovel")
def test_add(mock_add_imovel, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.lastrowid = 9

    payload = {"logradouro": "Gabi", "tipo_logradouro": "Rua"}

    mock_add_imovel.return_value = mock_conn

    response = client.post("/imoveis", json=payload)
    
    assert response.status_code == 201

    expected_response = (10, "Gabi", "Rua")
    assert response.get_json() == expected_response

@patch("servidor.update_imovel")
def test_update(mock_update_imovel, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    payload = {"logradouro": "Julia", "tipo_logradouro": "Rua"}

    mock_update_imovel.return_value = mock_conn

    response = client.put("/imoveis/9", json=payload)
    
    assert response.status_code == 200

    expected_response = {
        "imovel": {
            "id": 9,
            "logradouro": "Julia",
            "tipo_logradouro": "Rua"
        }
    }
    assert response.get_json() == expected_response

@patch("servidor.remove_imovel")
def test_remove(mock_remove_imovel, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (4, "Leri", "Rua"),
        (8, "Carolina", "Avenida"),
    ]

    mock_remove_imovel.return_value = mock_conn

    response = client.delete("/imoveis/4")

    assert response.status_code == 200

    expected_response = {"mensagem":"Apagado com sucesso"}
    assert response.get_json() == expected_response

@patch("servidor.listar_por_tipo")  
def test_tipo(mock_listar_por_tipo, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Leri", "casa"),
        (2, "Carolina", "casa"),
        (3, "Gabi", "casa"),
        (4, "Alvaro", "apartamento"),
        (5, "Emily", "apartamento"),
        (6, "Rafa", "apartamento")
    ]

    mock_listar_por_tipo.return_value = mock_conn

    response = client.get("/imoveis/tipo/casa")

    assert response.status_code == 200

    expected_response = {
        "tipo_imovel": [
            {"id": 1, "logradouro": "Leri", "tipo": "casa"},
            {"id": 2, "logradouro": "Carolina", "tipo": "casa"},
            {"id": 3, "logradouro": "Gabi", "tipo": "casa"}
        ]
    }
    assert response.get_json() == expected_response

@patch("servidor.listar_por_cidade")
def test_city(mock_listar_por_cidade, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Leri", "casa","Salvador"),
        (2, "Carolina", "casa", "São Paulo"),
        (3, "Gabi", "casa"),
        (4, "Alvaro", "apartamento", "Salvador"),
        (5, "Emily", "apartamento", "Taubaté"),
        (6, "Rafa", "apartamento", "Curitiba")
    ]
    
    mock_listar_por_cidade.return_value = mock_conn

    response = client.get("/imoveis/cidade/Salvador")

    assert response.status_code == 200

    expected_response = {
        "tipo_imovel": [
            {"id": 1, "logradouro": "Leri", "tipo_logradouro": "Rua", "cidade": "Salvador"},
            {"id": 3, "logradouro": "Gabi", "tipo_logradouro": "Rua", "cidade": "Salvador"}
        ]
    }
    assert response.get_json() == expected_response

