from app.models import db
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint


class Session(db.Model):
    """Represent a session"""

    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = db.Column(
        db.DateTime,
        default=None,
    )
    ACTIVE = "ACTIVE"
    CANCEL = "CANCEL"
    FINISHED = "FINISHED"
    PAUSE = "PAUSE"

    STATUS_CHOICES = [ACTIVE, CANCEL, FINISHED, PAUSE]

    status = db.Column(db.String(50), default=ACTIVE)
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Check if the value is in STATUS_CHOICES with Constraint sql
    # plus facile que de verifier dans le DTO
    __table_args__ = (
        CheckConstraint(
            f"status IN ('{ACTIVE}', '{CANCEL}', '{FINISHED}','{PAUSE}')",
            name="check_session_status",
        ),
    )

    # def to_dict(self) -> dict:
    #     """Return a JSON-compatible dictionary respresenting the Session"""
    #     return {
    #         "id": self.id,
    #         "created_at": self.created_at.isoformat(),
    #         "ended_at": self.ended_at.isoformat() if self.ended_at else None,
    #         "status": self.status,
    #     }

    # TODO COMPRENDRE
    def to_dict(self, include_cards: bool = False) -> dict:
        """Return a JSON-compatible dictionary representing the Session with optional stats and cards"""
        stats = {
            "total_cards": len(self.session_cards),
            "validated_cards": sum(1 for s in self.session_cards if s.validated),
            "attempt_count": sum(s.attempt_count for s in self.session_cards),
            "correct_count": sum(s.correct_count for s in self.session_cards),
            "failed_count": sum(s.failed_count for s in self.session_cards),
        }

        session_dict = {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "status": self.status,
            "deck_id": self.deck_id,
            "user_id": self.user_id,
            "stats": stats,
        }

        if include_cards:
            session_dict["cards"] = [s.to_dict() for s in self.session_cards]

        return session_dict
