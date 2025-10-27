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
    data = response.get_json()
    assert "token" in data
    assert data["role"] == "admin"

    # print(data["token"])
    # token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NjE1NzIyNTgsImlhdCI6MTc2MTU2ODY1OH0.2Q4TFp7-Q5GeLOAfugR5ZP20K8SXwXgSMoDgphk3CrI


def test_login_user(client):
    # crée une donnée dans la base
    payload_creation = {
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
    response_creation = client.post("/users/", json=payload_creation)
    assert response_creation.status_code == 201

    payload_login = {"password": "Test!123456", "email": "test12345@gmail.com"}
    response_loading = client.post("/users/login", json=payload_login)
    assert response_loading.status_code == 200


# endregion
# region GET


# def test_get_all_user(client):
#     # creation admin
#     payload_creation = {
#         "username": "Testeurfou13245",
#         "first_name": "TestFirst",
#         "last_name": "TestLast",
#         "password": "Test!123456",
#         "email": "test12345@gmail.com",
#         "gender": "M",
#         "phone_number": "047695872",
#         "birthdate": "1998-10-30",
#         "country": "Belgium",
#         "address": "Rue de feur, 56",
#         "user_bio": "Je test mon application tel un bon developper",
#         "image": "test.png",
#     }
#     response_creation = client.post("/users/", json=payload_creation)
#     assert response_creation.status_code == 201
#     data = response_creation.get_json()

#     # utilisation du token admin pour le get all


# endregion
