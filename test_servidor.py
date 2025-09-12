import pytest
from unittest.mock import patch, MagicMock
from servidor import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("servidor.todos_imoveis")  
def test_imoveis(mock_todos_imoveis, client):
    mock_todos_imoveis.return_value = [
        (4, "Leri", "Rua", "Horto", "Salvador", "88888", "casa", 105000, "2007-05-17"),
        (8, "Carolina", "Avenida", "Itaim", "Sao Paulo", "44444", "apartamento", 105000, "2025-05-17"),
    ]

    response = client.get("/imoveis")
    assert response.status_code == 200
    assert response.get_json()["todos_imoveis"][0]["id"] == 4

@patch("servidor.especifico")
def test_especifico(mock_especifico, client):
    mock_especifico.return_value = [(8, "Carolina", "Avenida", "Itaim", "Sao Paulo", "44444", "apartamento", 105000, "2025-05-17")]

    response = client.get("/imoveis/8")
    assert response.status_code == 200
    assert response.get_json()["imovel"]["id"] == 8

@patch("servidor.add")
def test_add(mock_add, client):
    mock_add.return_value = 10
    payload = {"logradouro": "Gabi", "tipo_logradouro": "Rua"}

    response = client.post("/imoveis", json=payload)
    assert response.status_code == 201
    assert response.get_json()["imovel"]["id"] == 10

@patch("servidor.update")
def test_update(mock_update, client):
    payload = {"logradouro": "Julia", "tipo_logradouro": "Rua"}
    response = client.put("/imoveis/9", json=payload)
    assert response.status_code == 200
    assert response.get_json()["imovel"]["id"] == 9

@patch("servidor.remove")
def test_remove(mock_remove, client):
    response = client.delete("/imoveis/4")
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Apagado com sucesso"}

@patch("servidor.filtro_tipo")  
def test_tipo(mock_filtro_tipo, client):
    mock_filtro_tipo.return_value = [
        (1, "Leri", "Rua", "Horto", "Salvador", "88888", "casa", 105000, "2007-05-17"),
        (2, "Carolina", "Rua", "Horto", "Salvador", "88888", "casa", 105000, "2007-05-17"),
        (3, "Gabi", "Rua", "Horto", "Salvador", "88888", "casa", 105000, "2007-05-17")
    ]

    response = client.get("/imoveis/tipo/casa")
    assert response.status_code == 200
    assert all(im["tipo"] == "casa" for im in response.get_json()["tipo_imovel"])

@patch("servidor.filtro_city")
def test_city(mock_filtro_city, client):
    mock_filtro_city.return_value = [
        (1, "Leri", "Rua", "Horto", "Salvador", "88888", "casa", 105000, "2007-05-17"),
        (2, "Carolina", "Avenida", "Itaim", "Salvador", "44444", "apartamento", 105000, "2025-05-17"),
    ]

    response = client.get("/imoveis/cidade/Salvador")
    assert response.status_code == 200
    assert all(im["cidade"] == "Salvador" for im in response.get_json()["tipo_imovel"])

@patch("servidor.connect_db")
def test_erro(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Nenhum imóvel encontrado"}