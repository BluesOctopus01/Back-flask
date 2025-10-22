from app.models import db
from .card_base import Card


class Gapfill(Card):
    __tablename__ = "gapfill"

    id = db.Column(db.Integer, db.ForeignKey("card.id"), primary_key=True)
    text1 = db.Column(db.String(100), nullable=False)
    text2 = db.Column(db.String(100), nullable=True)
    answer = db.Column(db.String(80), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "gapfill",
    }
