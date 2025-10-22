from app.models import db
from .card_base import Card


class Image(Card):
    __tablename__ = "image"

    id = db.Column(db.Integer, db.ForeignKey("card.id"), primary_key=True)
    text_alt = db.Column(db.String(80), nullable=True)
    url = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(80), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "image",
    }
