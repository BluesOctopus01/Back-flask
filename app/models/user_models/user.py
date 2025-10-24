from flask_login import UserMixin
from app.models import db
from datetime import datetime, timezone


class User(db.Model, UserMixin):
    """Represent a User in Balto"""

    __tablename__ = "user"

    MALE = "M"
    FEMALE = "F"
    UNDEFINED = "U"
    GENDER = [MALE, FEMALE, UNDEFINED]

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)

    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(1), nullable=False, default=UNDEFINED)

    phone_number = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    country = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    user_bio = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # todo potentiellement table ext role/country/adresse
    role = db.Column(db.String(50), default="user")
    is_active = db.Column(db.Boolean, default=True)

    decks = db.relationship("Deck", backref="creator", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


def to_dict(self, include_private: bool = False) -> dict:
    """
    Return a JSON-compatible dictionary representing the user.

    Args:
        include_private (bool): If True, include sensitive fields like email.
                                Defaults to False for safety.

    Returns:
        dict: Serialized representation of the user.
    """

    user_data = {
        "id": self.id,
        "username": self.username,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "gender": self.gender,
        "phone_number": self.phone_number,
        "birth_date": self.birth_date.isoformat() if self.birth_date else None,
        "country": self.country,
        "address": self.address,
        "user_bio": self.user_bio,
        "image": self.image,
        "role": self.role,
        "is_active": self.is_active,
        "created_at": self.created_at.isoformat() if self.created_at else None,
        "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
    }

    if include_private:
        user_data["email"] = self.email

    return user_data
