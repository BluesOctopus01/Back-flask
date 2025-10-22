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
