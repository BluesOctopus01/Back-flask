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
    response = client.post("/users/register", json=payload)
    assert response.status_code == 201
    data = response.get_json()

    # print(data["token"])
    # token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NjE1NzIyNTgsImlhdCI6MTc2MTU2ODY1OH0.2Q4TFp7-Q5GeLOAfugR5ZP20K8SXwXgSMoDgphk3CrI


def test_login_user(client):
    # rajout artificiel d'utilisateur
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
    response_creation = client.post("/users/register", json=payload_creation)
    assert response_creation.status_code == 201

    payload_login = {"password": "Test!123456", "email": "test12345@gmail.com"}
    response_loading = client.post("/users/login", json=payload_login)
    assert response_loading.status_code == 200
    data = response_loading.get_json()
    assert "token" in data
    assert data["role"] == "admin"


# endregion
# region GET
def test_get_a_user(client):
    # creation d'un user dans la db
    user = {
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
    response_creation = client.post("users/register", json=user)
    assert response_creation.status_code == 201
    user_id = response_creation.get_json()["id"]

    response_get_user = client.get(f"users/profiles/{user_id}")
    assert response_get_user.status_code == 200

    data = response_get_user.get_json()["image"]
    assert data == "test.png"


def test_get_all_user(client):
    # creation d'un admin pour les droits
    users_payloads = [
        {
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
        },
        {
            "username": "CodeMasterX",
            "first_name": "Alice",
            "last_name": "Durand",
            "password": "SecurePass!789",
            "email": "alice.durand@example.com",
            "gender": "F",
            "phone_number": "0485123456",
            "birthdate": "1995-04-12",
            "country": "France",
            "address": "12 Rue des Lilas",
            "user_bio": "Développeuse passionnée par l'IA et les jeux vidéo.",
            "image": "alice.png",
        },
        {
            "username": "BackendNinja77",
            "first_name": "Karim",
            "last_name": "Benali",
            "password": "KarimDev@2024",
            "email": "karim.benali@devmail.com",
            "gender": "M",
            "phone_number": "0478123499",
            "birthdate": "1990-08-22",
            "country": "Belgium",
            "address": "Avenue des Cerisiers, 89",
            "user_bio": "Spécialiste backend, amateur de café et de clean code.",
            "image": "karim.png",
        },
        {
            "username": "PixelQueen88",
            "first_name": "Sophie",
            "last_name": "Lemoine",
            "password": "SophieArt#321",
            "email": "sophie.lemoine@artmail.com",
            "gender": "F",
            "phone_number": "0499123456",
            "birthdate": "1992-12-05",
            "country": "Canada",
            "address": "123 Maple Street",
            "user_bio": "Graphiste freelance, fan de typographie et de design minimaliste.",
            "image": "sophie.png",
        },
        {
            "username": "DevWizard42",
            "first_name": "Julien",
            "last_name": "Moreau",
            "password": "Wizard42!Code",
            "email": "julien.moreau@wizarddev.com",
            "gender": "M",
            "phone_number": "0476123450",
            "birthdate": "1988-03-18",
            "country": "Switzerland",
            "address": "Chemin du Lac, 42",
            "user_bio": "Architecte logiciel, passionné par les algorithmes et les montagnes.",
            "image": "julien.png",
        },
    ]
    for payload in users_payloads:
        response_creation = client.post("/users/register", json=payload)

    assert response_creation.status_code == 201
    # connection du profil admin
    payload_login = {"password": "Test!123456", "email": "test12345@gmail.com"}
    response_loading = client.post("/users/login", json=payload_login)
    assert response_loading.status_code == 200
    data = response_loading.get_json()["role"]
    assert data == "admin"
    # token récupérer du login
    token = response_loading.get_json()["token"]

    # mise en place du token dans le bearer
    headers = {"Authorization": f"Bearer {token}"}
    admin_response = client.get("users/admin", headers=headers)
    assert admin_response.status_code == 200


# endregion


# region PUT/PATCH
# def update_user

# endregion


# region DELETE/SOFT


# endregion
