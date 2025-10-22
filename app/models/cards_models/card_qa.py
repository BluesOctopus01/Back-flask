from app.models import db
from .card_base import Card


class Qa(Card):
    __tablename__ = "qa"

    id = db.Column(db.Integer, db.ForeignKey("card.id"), primary_key=True)

    answer = db.Column(db.String(80), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "qa",
    }
