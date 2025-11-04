from datetime import datetime, timezone
from typing import Optional, Tuple, Dict
from app.models.deck import Deck
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db


# region POST
def post_deck(
    name: str,
    bio: str,
    access: str,
    image: str,
    access_key: str,
    creator_id: int,
) -> Deck:
    """Return a created Deck"""
    hashed_access_key = generate_password_hash(access_key) if access_key else None

    new_deck = Deck(
        name=name,
        bio=bio,
        access=access,
        image=image,
        access_key=hashed_access_key,
        creator_id=creator_id,
    )
    db.session.add(new_deck)
    db.session.commit()

    return new_deck

    # endregion

    # region GET


def get_deck_search(
    user_id: int, deck_id: int, data_access: str
) -> Tuple[Optional["Deck"], Optional[Dict]]:
    """Return a deck and None or None and an error"""

    deck: Deck = get_deck(deck_id)
    # Deck introuvable
    if not deck:
        return None, {"error": "Deck not found"}

    # Si l'utilisateur est le créateur
    if deck.creator_id == user_id:
        return deck, None

    # Accès public
    if deck.access == "PUBLIC":
        return deck, None

    # Accès protégé : mot de passe requis
    if deck.access == "PROTECTED":
        if check_password_hash(deck.access_key, data_access["access_key"]):
            return deck, None
        else:
            return None, {"error": "Invalid credentials"}

    # Accès privé : refusé
    if deck.access == "PRIVATE":
        return None, {"error": "Unauthorized"}

    # Cas inattendu
    return None, {"error": "Unknown access type"}


def get_deck_user(user_id: int) -> list[Deck] | None:
    """Return a list of Decks from a user, or None if none found"""
    decks = Deck.query.filter_by(creator_id=user_id).all()
    if not decks:
        return None
    return decks


def get_deck(deck_id: int) -> Deck | None:
    """Return a Deck from a deck id, or None if none found"""
    deck: Deck = Deck.query.filter_by(id=deck_id).first()
    if not deck:
        return None
    return deck


# endregion


# region UPDATE
def patch_deck_user(
    deck_id: int,
    name: str | None,
    bio: str | None,
    access: str | None,
    image: str | None,
    access_key: str | None,
) -> Deck | None:
    """Patch a deck with informations from User, if there is no information the old one is kept"""
    deck = get_deck(deck_id)
    if not deck:
        return None
    deck.last_modification_at = datetime.now(timezone.utc)

    if name is not None:
        deck.name = name

    if bio is not None:
        deck.bio = bio

    if access is not None:
        deck.access = access

    if image is not None:
        deck.image = image

    if access_key is not None:
        deck.access_key = generate_password_hash(access_key)

    db.session.commit()

    return deck


# endregion


# region DELETE/SOFT

# endregion
