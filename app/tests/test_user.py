import pytest
from app import create_app


@pytest.fixture
def client():
    """Client de test Flask isolé pour chaque test"""
    app = create_app()
    app.testing = True
    return app.test_client()


# region GET


def test_get_all_user(client):
    # todo fournir un token pour le role admin

    response = client.get("https://localhost:5000/users/admin")
    assert response.status_code == 200
    # TODO tests


# endregion
