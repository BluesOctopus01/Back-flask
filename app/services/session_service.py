from app.models.session_models.session import Session
from app.models import db


def is_owner_session(user_id: int, session: Session) -> bool:
    """Return True if user created the session"""
    if session.user_id == user_id:
        return True
    return False


# region POST
def create_session(user_id: int, deck_id: int) -> Session:
    """Create a session and return a session"""
    new_session = Session(user_id=user_id, deck_id=deck_id)

    db.session.add(new_session)
    db.session.commit()

    return new_session


# endregion


# region GET
def fetch_session_by_id(session_id: int) -> Session | None:
    """fetch a session and return it or None"""
    session: Session = Session.query.filter_by(id=session_id).first()
    if not session:
        return None
    return session


def fetch_session_by_user_id(user_id: int) -> Session | None:
    """fetch a session by user_id and return it or None"""
    session_active: Session = Session.query.filter_by(
        user_id=user_id, status=Session.ACTIVE
    ).first()

    if not session_active:
        return None

    return session_active


def fetch_all_sessions_user():
    """fetch all sessions by own user_id and return a list of Sessions"""


def admin_fetch_sessions():
    """fetch all sessions and return them as a list"""


# endregion

# region UPDATE
# endregion


# region DELETE
def end_session():
    pass


# endregion
