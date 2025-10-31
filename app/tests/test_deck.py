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


PAYLOAD_DECK = {
    "creator_id": 1,
    "name": "Biologie Cellulaire",
    "bio": "Deck pour réviser les bases de la biologie cellulaire.",
    "access": "PROTECTED",
    "image": "biologie_deck.png",
    "access_key": "Bio2025!",
}
PAYLOAD_USER = {
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
PAYLOAD_LOGIN_USER = {"password": "Test!123456", "email": "test12345@gmail.com"}


def test_create_deck(client):

    response = client.post("/users/register", json=PAYLOAD_USER)
    assert response.status_code == 201

    response_loading = client.post("/users/login", json=PAYLOAD_LOGIN_USER)
    assert response_loading.status_code == 200

    token = response_loading.get_json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    response_deck_creating = client.post(
        "/users/decks/create", json=PAYLOAD_DECK, headers=headers
    )
    assert response_deck_creating.status_code == 201
    print(response_deck_creating.get_json())
