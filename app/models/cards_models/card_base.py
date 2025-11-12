from app.models import db
from datetime import datetime, timezone


class Card(db.Model):
    __tablename__ = "card"

    id = db.Column(db.Integer, primary_key=True)
    card_type = db.Column(db.String(50))
    question = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_modification = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "card", "polymorphic_on": card_type}

    def to_dict(self) -> dict:
        """Return a JSON-compatible dictionary representing the Card without sensitive informations"""
        return {
            "id": self.id,
            "card_type": self.card_type,
            "question": self.question,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_modification": (
                self.last_modification.isoformat() if self.last_modification else None
            ),
            "deck_id": self.deck_id,
        }
