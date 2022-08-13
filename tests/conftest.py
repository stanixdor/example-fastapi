from pyexpat import model
from turtle import title
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import createAccessToken
from app import models
import pytest


#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:aritz1997@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#@pytest.fixture(scope='module')
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    #run our code before we run out test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    #run our code after our test finishes

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello1@gmail.com", "password": "123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello2@gmail.com", "password": "123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return createAccessToken({"userID": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
    "title" : "zz",
    "content" : "ssssssszzsssss",
    "owner_id": test_user['id']
    },{
        "title" : "22",
        "content" : "dddddddd",
        "owner_id": test_user['id']
    },{
        "title" : "33",
        "content" : "cccccc",
        "owner_id": test_user['id']
    },{
        "title" : "33",
        "content" : "cccccc",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all([models.Post(title="zz", content="ssssssszzsssss", owner_id=test_user['id']),
    #                 models.Post(title="22", content="dddddddd", owner_id=test_user['id']),
    #                 models.Post(title="33", content="cccccc", owner_id=test_user['id'])])
    session.commit()
    session.query(models.Post).all()
    return posts