from app.models.session_models.session import Session
from app.models.session_models.session_card import SessionCardStat
from app.models import db
from datetime import datetime, timezone
from app.models.cards_models.card_base import Card
from app.models.deck import Deck

# permet d'importer l'aléatoire dans la querry
from sqlalchemy.sql.expression import func


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


def create_session_stat(deck: Deck, user_id: int, session: Session) -> None:
    """Create a second table, stat session who bears the cards"""

    for card in deck.cards:
        stat = SessionCardStat(user_id=user_id, card_id=card.id, session_id=session.id)
        db.session.add(stat)

    db.session.commit()


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


def fetch_all_sessions_user(user_id: int) -> list[Session] | None:
    """fetch all NON ACTIVE sessions by own user_id and return a list of Sessions"""
    sessions = Session.query.filter(
        Session.user_id == user_id, Session.status != Session.ACTIVE
    )
    if not sessions:
        return sessions
    return None


def admin_fetch_sessions() -> list[Session]:
    """fetch all sessions and return them as a list"""
    return Session.query.all()


def draw_card(session_id: int, user_id: int) -> Card | Session:
    """Draw a random card, in the validated = False pool, return a card"""
    card_stat: SessionCardStat = (
        SessionCardStat.query.filter_by(
            session_id=session_id, user_id=user_id, validated=False
        )
        .order_by(func.random())
        .first()
    )
    if not card_stat:
        session = fetch_session_by_id(session_id)
        session_stat = succeed_finish_session(session)
        return session_stat
    card: Card = card_stat.card
    return card


# endregion


# region UPDATE
def pause_session(session: Session) -> Session | None:
    """Restart a session if ACTIVE, return a session or none"""
    if session.status == "ACTIVE":
        session.status = "PAUSE"
        db.session.commit()
        return session
    return None


def restart_session(session: Session) -> Session | None:
    """Restart a session if PAUSE, return a session or none"""
    if session.status == "PAUSE":
        session.status = "ACTIVE"
        db.session.commit()
        return session
    return None


def succeed_finish_session(session: Session) -> Session:
    """FINISHED a session if every condition are completed return True or false"""
    session.status = "FINISHED"
    if session:
        session.status = "FINISHED"
        session.ended_at = datetime.now(timezone.utc)
        db.session.commit()
        return session


# TODO a terme jouer avec des validations automatiques
def validate_answer(
    session_id: int, user_id: int, card_id: int, data: dict
) -> SessionCardStat | None:
    """Update the SessionCardStat card Validation, to true or keep it false and increment, return the card"""
    stat: SessionCardStat = SessionCardStat.query.filter_by(
        session_id=session_id, user_id=user_id, card_id=card_id
    ).first()

    if data["validation"] not in ["True", "False"]:
        return None

    stat.attempt_count += 1

    if data["validation"] == "True":
        stat.validated = True
        stat.correct_count += 1
    if data["validation"] == "False":
        stat.failed_count += 1

    db.session.commit()
    return stat


# endregion


# region DELETE
def end_session(session: Session) -> bool:
    """Transform status into CANCEL, return True if succeed, and False"""
    if session:
        session.status = "CANCEL"
        session.ended_at = datetime.now(timezone.utc)
        db.session.commit()
        return True
    return False


# endregion


# Todo draw cards/ shuffle / validate card /etc
# 🔹 Cycle de jeu

#     Création de session

#         Tu crées une Session.

#         Tu insères toutes les cartes du deck dans SessionCardStat avec validated = FALSE.

#     Répondre à une carte

#         L’utilisateur envoie sa réponse via une route (ex. PATCH /sessions/<id>/cards/<id>/answer).

#         Tu compares avec la bonne réponse.

#         Tu mets à jour les stats :

#             attempt_count += 1

#             Si correct → correct_count += 1, validated = TRUE (la carte sort du pool).

#             Si incorrect → failed_count += 1, validated = FALSE (elle reste dans le pool).

#     Pool actif

#         Les cartes encore en jeu sont celles avec validated = FALSE.

#         Tu peux récupérer la prochaine carte avec :
#         sql
# Fin de session

#     Quand toutes les cartes sont validated = TRUE, la session est terminée.

#     Tu peux mettre à jour session.status = FINISHED et session_ended_at = now().

# POST /sessions/decks/:deck_id → création

# GET /sessions/:id/draw-card → pioche

# PATCH /sessions/:id/cards/:card_id/answer → réponse

# PATCH /sessions/:id/end → fin

# PATCH /sessions/:id → pause/restart
