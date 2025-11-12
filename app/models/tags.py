from app.models import db

from datetime import datetime, timezone


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    decks = db.relationship("Deck", secondary="tag_deck", back_populates="tags")

    def to_dict(self) -> dict:
        """Return a JSON-compatible dictionary representing the Deck without sensitive informations"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class TagDeck(db.Model):
    __tablename__ = "tag_deck"

    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)
