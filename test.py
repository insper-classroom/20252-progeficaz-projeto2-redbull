import pytest
from unittest.mock import patch, MagicMock
from servidor import app, connect_db
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

    expected_response = {
        "imovel": {
            "id": 9,
            "logradouro": "Gabi",
            "tipo_logradouro": "Rua"
        }
    }
    assert response.get_json() == expected_response

# def test_update():

# def test_remove():

# def test_type():

# def test_city():