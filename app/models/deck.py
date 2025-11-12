from app.models import db
from datetime import datetime, timezone
from app.models.cards_models.card_base import Card
from app.models.tags import Tag
from typing import List


class Deck(db.Model):
    __tablename__ = "deck"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(100), nullable=True, default="")
    # todo Verifier si on ne peut pas changer, le acess_choice pour le rendre restrictif dans la db au lieu de rajouter une couche de verification
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    PROTECTED = "PROTECTED"
    ACCESS_CHOICES = [PUBLIC, PRIVATE, PROTECTED]

    access = db.Column(db.String(10), default=PUBLIC, nullable=False)
    creation_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    image = db.Column(db.String(200), nullable=True)

    access_key = db.Column(db.String(250), nullable=True, default="")

    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    last_modification_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    cards = db.relationship(
        "Card", backref="deck", lazy=True, cascade="all, delete-orphan"
    )
    tags = db.relationship("Tag", secondary="tag_deck", back_populates="decks")

    def __repr__(self):
        return f"<Deck {self.name}"

    def to_dict(self) -> dict:
        """Return a JSON-compatible dictionary representing the Deck without sensitive informations"""
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "access": self.access,
            "creation_at": self.creation_at.isoformat() if self.creation_at else None,
            "image": self.image,
            "last_modification_at": (
                self.last_modification_at.isoformat()
                if self.last_modification_at
                else None
            ),
            "creator_id": self.creator_id,
            "cards": [card.to_dict() for card in self.cards],
            "tags": [tag.to_dict() for tag in self.tags],
        }

    # todo verifier si card.to_dict() et tag fonctionne bien sans le typage plus autorisé
    def to_summary_dict(self) -> dict:
        """Return the summary of a deck"""
        return {
            "id": self.id,
            "name": self.name,
            "access": self.access,
            "creator_id": self.creator_id,
        }
