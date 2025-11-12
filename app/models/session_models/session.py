from app.models import db
from datetime import datetime, timezone


class Session(db.Model):
    """Represent a session"""

    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = db.Column(
        db.DateTime,
        default=None,
    )
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
