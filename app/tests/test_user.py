import pytest
from app import create_app


@pytest.fixture
def client():
    """Client de test Flask isolé pour chaque test"""
    app = create_app()
    app.testing = True
    return app.test_client()


# region GET


# def test_get_all_user(client):
#     # todo fournir un token pour le role admin
# admin token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
# eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NjEzMjIxMzYsImlhdCI6MTc2MTMxODUzNn0.
# _aWwG9VFR5_2evz4XfGo2Un7rwBJ0mXjoVtTz9kbqN8"

# user token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
# eyJ1c2VyX2lkIjoyLCJyb2xlIjoidXNlciIsImV4cCI6MTc2MTMyMjI4NCwiaWF0IjoxNzYxMzE4Njg0fQ.
# tCUdexJEfNA6GQs8Lww2J2uusvoPpSchAbtN0JkAHeQ"

#     response = client.get("https://localhost:5000/users/admin")
#     assert response.status_code == 200
#     # TODO tests


# endregion
