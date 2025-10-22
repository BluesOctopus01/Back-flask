from app.models import db
from datetime import datetime, timezone


class Deck(db.Model):
    __tablename__ = "deck"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(100), nullable=True)

    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"
    ACCESS_CHOICES = [PUBLIC, PRIVATE, PROTECTED]

    access = db.Column(db.String(10), default=PUBLIC, nullable=False)

    size = db.Column(db.Integer, default=0)
    creation_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    deck_image = db.Column(db.String(200), nullable=True)

    access_key = db.Column(db.String(150), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    last_modification_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    cards = db.relationship(
        "Card", backref="deck", lazy=True, cascade="all, delete-orphan"
    )
