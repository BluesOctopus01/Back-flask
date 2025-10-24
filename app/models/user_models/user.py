from flask_login import UserMixin
from app.models import db
from datetime import datetime, timezone


class User(db.Model, UserMixin):
    """Represent a User in Balto"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)

    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    phone_number = db.Column(db.String(20), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(200), nullable=True)
    user_bio = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    role = db.Column(db.String(50), default="user")
    is_active = db.Column(db.Boolean, default=True)

    decks = db.relationship("Deck", backref="creator", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        """Return a JSON compatible dictionnary without psw"""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "address": self.address,
            "user_bio": self.user_bio,
            "image": self.image,
            "created_at": self.created_at.isoformat(),
            "last_login_at": self.last_login_at.isoformat(),
            "role": self.role,
            "is_active": self.is_active,
        }
