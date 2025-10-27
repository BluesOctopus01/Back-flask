import pytest
from app import create_app, db
from app.configs.config import TestConfig


@pytest.fixture
def client():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()
    # TODO comprendre


# !! Clé d'accès
# admin token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
# eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NjEzMjIxMzYsImlhdCI6MTc2MTMxODUzNn0.
# _aWwG9VFR5_2evz4XfGo2Un7rwBJ0mXjoVtTz9kbqN8"

# user token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
# eyJ1c2VyX2lkIjoyLCJyb2xlIjoidXNlciIsImV4cCI6MTc2MTMyMjI4NCwiaWF0IjoxNzYxMzE4Njg0fQ.
# tCUdexJEfNA6GQs8Lww2J2uusvoPpSchAbtN0JkAHeQ"


# region POST
def test_create_user(client):
    payload = {
        "username": "Testeurfou13245",
        "first_name": "TestFirst",
        "last_name": "TestLast",
        "password": "Test!123456",
        "email": "test12345@gmail.com",
        "gender": "M",
        "phone_number": "047695872",
        "birthdate": "1998-10-30",
        "country": "Belgium",
        "address": "Rue de feur, 56",
        "user_bio": "Je test mon application tel un bon developper",
        "image": "test.png",
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 201


def test_login_user(client):
    pass


# endregion
# region GET


def test_get_all_user(client):
    pass


# endregion
