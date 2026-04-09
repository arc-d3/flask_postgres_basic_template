import re

def test_home(client):

    response = client.get("/")
    assert b"<title>Home</title>" in response.data

def test_register(client):
    response = client.post("/register", data={
        "name": "test",
        "email": "testemail@gmail.com",
        "password": "fewfskdfjewww97"
    })

    assert response.status_code == 302

def test_login(client, app):
    response = client.post("/register", data={
        "name": "test",
        "email": "testemail@gmail.com",
        "password": "fewfskdfjewww97"
    })

    response = client.post("/login", data={
        "email": "testemail@gmail.com",
        "password": "fewfskdfjewww97"
    })

    assert response.status_code == 302