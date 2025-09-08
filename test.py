import pytest
from unittest.mock import patch, MagicMock
from servidor import app, connect_sql
from utils import *

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("servidor.connect_db")  
def test_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (4, "Leri", "Rua"),
        (8, "Carolina", "Avenida"),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200

    expected_response = {
        "todos_imoveis": [
            {"id": 4, "logradouro": "Leri", "tipo_logradouro": "Rua"},
            {"id": 8, "logradouro": "Carolina", "tipo_logradouro": "Avenida"},
        ]
    }
    assert response.get_json() == expected_response

@patch("servidor.connect_db")
def test_especifico(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = (8, "Carolina", "Avenida")

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis/<int:imovel_id")

    assert response.status_code == 200

    expected_response = expected_response = {
        "imovel": {
            "id": 8,
            "logradouro": "Carolina",
            "tipo_logradouro": "Avenida"
        }
    }

    assert response.get_json() == expected_response

@patch("servidor.connect_db")
def test_add(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.lastrowid = 9

    payload = {"logradouro": "Gabi", "tipo_logradouro": "Rua"}

    mock_connect_db.return_value = mock_conn

    response = client.post("/imoveis", json=payload)
    
    assert response.status_code == 201

    expected_response = (10, "Gabi", "Rua")
    assert response.get_json() == expected_response

@patch("servidor.connect_db")
def test_update(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    payload = {"logradouro": "Julia", "tipo_logradouro": "Rua"}

    mock_connect_db.return_value = mock_conn

    response = client.put("/imoveis/<int:imovel_id>", json=payload)
    
    assert response.status_code == 200

    expected_response = {
        "imovel": {
            "id": 9,
            "logradouro": "Julia",
            "tipo_logradouro": "Rua"
        }
    }
    assert response.get_json() == expected_response


@patch("servidor.connect_db")
def test_remove(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (4, "Leri", "Rua"),
        (8, "Carolina", "Avenida"),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.delete("/imoveis/<int:imovel_id>")

    assert response.status_code == 200

    expected_response = {"mensagem":"Apagado com sucesso"}
    assert response.get_json() == expected_response


@patch("servidor.connect_db")  
def test_tipo(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Leri", "casa"),
        (2, "Carolina", "casa"),
        (3, "Gabi", "casa"),
        (4, "Alvaro", "apartamento")
        (5, "Emily", "apartamento"),
        (6, "Rafa", "apartamento")
    ]

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis/tipo/<string:tipo>")

    assert response.status_code == 200

    expected_response = {
        "tipo_imovel": [
            {"id": 1, "logradouro": "Leri", "tipo": "casa"},
            {"id": 2, "logradouro": "Carolina", "tipo": "casa"},
            {"id": 3, "logradouro": "Gabi", "tipo": "casa"}
        ]
    }
    assert response.get_json() == expected_response



@patch("servidor.connect_db")
def test_city(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Leri", "casa","Salvador"),
        (2, "Carolina", "casa", "São Paulo"),
        (3, "Gabi", "casa"),
        (4, "Alvaro", "apartamento", "Salvador")
        (5, "Emily", "apartamento", "Taubaté"),
        (6, "Rafa", "apartamento", "Curitiba")
    ]
    
    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis/cidade<string:cidade>")

    assert response.status_code == 200

    expected_response = {
        "tipo_imovel": [
            {"id": 1, "logradouro": "Leri", "tipo_logradouro": "Rua", "cidade": "Salvador"},
            {"id": 3, "logradouro": "Gabi", "tipo_logradouro": "Rua", "cidade": "Salvador"}
        ]
    }
    assert response.get_json() == expected_response

