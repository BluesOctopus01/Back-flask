from app.models import db
from .card_base import Card


class Qcm(Card):
    __tablename__ = "qcm"

    id = db.Column(db.Integer, db.ForeignKey("card.id"), primary_key=True)

    answers = db.relationship(
        "AnswerQcm", backref="qcm", lazy=True, cascade="all, delete-orphan"
    )
    __mapper_args__ = {
        "polymorphic_identity": "qcm",
    }

    def to_dict(self):
        data = super().to_dict()
        data.update({"answers": self.answers})
