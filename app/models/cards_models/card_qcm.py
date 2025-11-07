from app.models import db
from .card_base import Card


class Qcm(Card):
    __tablename__ = "qcm"

    id = db.Column(db.Integer, db.ForeignKey("card.id"), primary_key=True)

    answers = db.relationship(
        "AnswerQcm", backref="qcm", lazy="joined", cascade="all, delete-orphan"
    )
    __mapper_args__ = {
        "polymorphic_identity": "qcm",
    }

    def to_dict(self):
        data = super().to_dict()
        # Convertir les  en liste de dicts pour json
        data["answers"] = [a.to_dict() for a in self.answers]
        return data
