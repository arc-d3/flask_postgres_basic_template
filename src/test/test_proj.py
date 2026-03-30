from app.models.user import User
import re

def get_csrf_token(client, url):
    response = client.get(url)
    match = re.search(r'name="csrf_token"[^>]*value="(.+?)"', response.data.decode())
    return match.group(1)

def test_home(client):

    response = client.get("/")
    assert b"<title>Home</title>" in response.data

def test_register(client):
    token = get_csrf_token(client, "/register")
    response = client.post("/register", data={
        "csrf_token": token,
        "name": "test",
        "email": "testemail@gmail.com",
        "password": "fewfskdfjewww97"
    })

    assert response.status_code == 302

def test_login(client, app):
    token = get_csrf_token(client, "/register")
    response = client.post("/register", data={
        "csrf_token": token,
        "name": "test",
        "email": "testemail@gmail.com",
        "password": "fewfskdfjewww97"
    })

    token = get_csrf_token(client, "/login")
    response = client.post("/login", data={
        "csrf_token": token,
        "email": "testemail@gmail.com",
        "password": "fewfskdfjewww97"
    })

    assert response.status_code == 302