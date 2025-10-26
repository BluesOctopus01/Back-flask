import pytest
from app import create_app


@pytest.fixture
def client():
    """Client de test Flask isolé pour chaque test"""
    app = create_app()
    app.testing = True
    return app.test_client()


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
        "username": "Testeurfou1324",
        "first_name": "TestFirst",
        "last_name": "TestLast",
        "password": "Test!123456",
        "email": "test123@gmail.com",
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
    #!! USER CRER DANS LA BASE DE DONNE + ID AUGMENTE A CHAUQE ESSAIE db.session.rollback() dans le test


def test_login_user(client):
    pass


# endregion
# region GET


def test_get_all_user(client):
    pass


# endregion
