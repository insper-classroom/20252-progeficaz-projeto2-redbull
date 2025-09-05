import pytest
from unittest.mock import patch, MagicMock
from api import app, connect_db
from utils import *

@pytest.fixture
def client():
    """Cria um cliente de teste para a API."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("api.connect_db")  # Substituímos a função que conecta ao banco por um Mock
def test_get_list(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (4, "Leri", "Rua"),
        (2, "Carolina", "Avenida"),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveismock")

    expected_response = {
        "imoveismock": [
            {"id": 4, "logradouro": "Leri", "tipo_logradouro": "Rua"},
            {"id": 8, "logradouro": "Carolina", "tipo_logradouro": "Avenida"},
        ]
    }
    assert response.get_json() == expected_response

@pytest.fixture
def test_list_especific():
    magic_conn = MagicMock()
    magic_cursor = MagicMock()
    mock_imoveis = [(8, 'Carolina', 'avenida')]
    magic_cursor.execute.return_value = mock_imoveis

    assert list_toda(magic_cursor, 8) == [(8, 'Carolina', 'avenida')]

# def test_add():
#     magic_conn = MagicMock()
#     magic_cursor = MagicMock()
#     mock_imoveis = [(8, 'Carolina', 'avenida'), (4, 'Leri', 'rua')]
#     magic_cursor.execute.return_value = mock_imoveis

#     assert add(magic_cursor) == [(8, 'Carolina', 'avenida'), (4, 'Leri', 'rua')]

# def test_update():

# def test_remove():

# def test_type():

# def test_city():