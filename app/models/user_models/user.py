from flask_login import UserMixin
from app.models import db
from datetime import datetime, timezone


class User(db.Model, UserMixin):
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
