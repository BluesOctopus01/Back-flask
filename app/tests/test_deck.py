import pytest
from app import create_app, db
from app.configs.config import TestConfig
from app.utils.data_utils import *


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


@pytest.fixture
def auth_headers(client):
    client.post("/users/register", json=PAYLOAD_USER)
    response = client.post("/users/login", json=PAYLOAD_LOGIN_USER)
    token = response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_with_decks(client, auth_headers):
    for decks in PAYLOAD_DECKS_WITH_ID1:
        response = client.post("/users/decks/create", json=decks, headers=auth_headers)
        assert response.status_code == 201
    return auth_headers


def test_create_deck(client, auth_headers):
    response_deck_creating = client.post(
        "/users/decks/create", json=PAYLOAD_DECK, headers=auth_headers
    )
    assert response_deck_creating.status_code == 201


def test_get_decks(client, user_with_decks):
    response = client.get("/users/decks/", headers=user_with_decks)
    assert response.status_code == 200
    assert len(response.get_json()) == 4


def test_get_deck_controller(client, user_with_decks):
    response = client.get("/users/decks/1", headers=user_with_decks)
    assert response.status_code == 200
    print(response.get_json())
    response_wrong = client.get("/users/deck/999", headers=user_with_decks)
    assert response_wrong.status_code == 404
