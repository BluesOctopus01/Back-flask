from app.models import db


class SessionCardStat(db.Model):
    """Represent the cards that are part of a deck in a session"""

    __tablename__ = "session_card_stat"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"), primary_key=True)
    attempt_count = db.Column(db.Integer, default=0, nullable=False)
    correct_count = db.Column(db.Integer, default=0, nullable=False)
    failed_count = db.Column(db.Integer, default=0, nullable=False)
    validated = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User", backref="session_cards")
    card = db.relationship("Card", backref="session_cards")
    session = db.relationship("Session", backref="session_cards")

    def to_dict(self) -> dict:
        """Return a JSON-compatible dictionary representing the SessionCardStat"""
        return {
            "user_id": self.user_id,
            "card_id": self.card_id,
            "session_id": self.session_id,
            "attempt_count": self.attempt_count,
            "correct_count": self.correct_count,
            "failed_count": self.failed_count,
            "validated": self.validated,
        }
