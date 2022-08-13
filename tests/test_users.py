from urllib import response
from app import schemas
import pytest
from jose import jwt
from app.config import settings



# def test_root(client):
#     res = client.get('/')
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Best APIzzz :3'
#     assert res.status_code == 200

def test_create_user(client):

    res = client.post('/users/', json={"email": "hello12@gmail.com", "password": "123"})

    newUser = schemas.UserOut(**res.json())
    
    assert newUser.email == "hello12@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.accessToken, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('userID')
    assert id == test_user['id']
    assert login_res.tokenType == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("asddasasd@gmail.com", "sadasasdd", 403), ("tdfgt@gmail.com", "sadadfgsasdd", 403),
    (None, "sadasasdd", 422), ("tdfgt@gmail.com", None, 422)])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={"username": email, "password": password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'