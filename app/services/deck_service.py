from datetime import datetime, timezone
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

# endregion


# region UPDATE

# endregion


# region DELETE/SOFT

# endregion
