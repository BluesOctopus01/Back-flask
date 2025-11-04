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

PAYLOAD_DECKS_WITH_ID1 = [
    {
        "creator_id": 1,
        "name": "Biologie Cellulaire",
        "bio": "Deck pour réviser les bases de la biologie cellulaire.",
        "access": "PROTECTED",
        "image": "biologie_deck.png",
        "access_key": "Bio2025!",
    },
    {
        "creator_id": 1,
        "name": "Chimie Organique",
        "bio": "Deck sur les réactions organiques fondamentales.",
        "access": "PRIVATE",
        "image": "chimie_deck.jpg",
        "access_key": "ChemSecret42",
    },
    {
        "creator_id": 1,
        "name": "Physique Quantique",
        "bio": "Introduction aux concepts de la mécanique quantique.",
        "access": "PUBLIC",
        "image": "quantique_deck.webp",
        "access_key": None,
    },
    {
        "creator_id": 1,
        "name": "Histoire Médiévale",
        "bio": "Deck sur les grandes dynasties du Moyen Âge.",
        "access": "PROTECTED",
        "image": "histoire_deck.png",
        "access_key": "Medieval2025",
    },
]

PAYLOAD_MIXED_CREATORS = [
    {
        "creator_id": 1,
        "name": "Biologie Cellulaire",
        "bio": "Deck pour réviser les bases de la biologie cellulaire.",
        "access": "PROTECTED",
        "image": "biologie_deck.png",
        "access_key": "Bio2025!",
    },
    {
        "creator_id": 2,
        "name": "Philosophie Antique",
        "bio": "Deck sur les grands penseurs grecs et romains.",
        "access": "PRIVATE",
        "image": "philo_deck.jpg",
        "access_key": "Socrate42",
    },
    {
        "creator_id": 3,
        "name": "Programmation Python",
        "bio": "Deck pour apprendre les bases du langage Python.",
        "access": "PUBLIC",
        "image": "python_deck.png",
        "access_key": None,
    },
]
