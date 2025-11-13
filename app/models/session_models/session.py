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

    def to_dict(self) -> dict:
        """Return a JSON-compatible dictionary respresenting the Session"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "status": self.status,
        }
