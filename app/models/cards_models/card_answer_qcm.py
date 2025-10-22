from app.models import db


class AnswerQcm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    valid = db.Column(db.Boolean, default=False)

    qcm_id = db.Column(db.Integer, db.ForeignKey("qcm.id"), nullable=False)
