from app.models.session_models.session import Session

from flask import jsonify, request
from app.utils.jwt_utils import generate_token

from app.services.session_service import *
from app.services.deck_service import get_deck_search
from app.services.session_service import (
    fetch_session_by_id,
    is_owner_session,
    fetch_session_by_user_id,
    pause_session,
    restart_session,
    succeed_finish_session,
    end_session,
)


# region POST
def create_session_controller(user_id, deck_id, data_access):
    """EndPoint : GET /sessions/decks/:deck_id"""

    exisiting_session = fetch_session_by_user_id(user_id)
    if exisiting_session:
        return jsonify({"message": "A session is already active"}), 403

    deck, err = get_deck_search(user_id, deck_id, data_access)
    if err:
        error_message = err.get("error")
        # back up si il ne rentre dans aucune conditions
        status = 400

        if error_message == "Deck not found":
            status = 404
        if error_message == "Invalid credentials":
            status = 403
        if error_message == "Unauthorized":
            status = 401

        return jsonify(err), status

    session = create_session(user_id, deck_id)
    response_session = session.to_dict()

    return jsonify(response_session), 201


# endregion


# region GET
def join_session_controller(user_id):
    """EndPoint : GET /sessions/"""
    session = fetch_session_by_user_id(user_id)
    if not session:
        return jsonify({"message": "No current session active"}), 404
    response_session = session.to_dict()

    return jsonify(response_session), 200


def join_session_by_id_controller(user_id, session_id):
    """EndPoint : GET /sessions/:session_id"""
    session = fetch_session_by_id(session_id)
    if not session:
        return jsonify({"message": "Session not found"}), 404

    own_session = is_owner_session(user_id, session)
    if not own_session:
        return jsonify({"message": "Unauthorized"}), 401

    response_session = session.to_dict()

    return jsonify(response_session), 200


def all_sessions_by_user_controller(user_id):
    """EndPoint : GET /sessions/user/history"""
    sessions = fetch_all_sessions_user(user_id)
    if not sessions:
        return jsonify({"message": "No history"}), 404
    sessions_dict = [session.to_dict() for session in sessions]
    return jsonify(sessions_dict), 200


def admin_all_sessions():
    sessions = admin_fetch_sessions()
    sessions_dict = [session.to_dict() for session in sessions]
    return jsonify(sessions_dict), 200


# endregion


# region UPDATE
# TODO Pour bien faire, créer un dto
def update_session_controller(user_id, session_id, data):
    """PATCH /sessions/:session_id"""
    session = fetch_session_by_id(session_id)
    if not session:
        return jsonify({"message": "Session not found"}), 404

    if not is_owner_session(user_id, session):
        return jsonify({"message": "Unauthorized"}), 401

    action = data["action"] or ""
    if action not in ["PAUSE", "ACTIVE"]:
        return jsonify({"message": "Invalid action"}), 403

    if action == "PAUSE":
        session_action = pause_session(session)

    elif action == "ACTIVE":
        user_session = fetch_session_by_user_id(user_id)
        if user_session:
            return jsonify({"message": "An other session is already active"}), 403
        session_action = restart_session(session)

    if not session_action:
        return jsonify({"message": "Action not allowed"}), 400

    return jsonify(session_action.to_dict()), 200


# endregion


# region DELETE
def end_session_controller(user_id, session_id):
    """DELETE /sessions/:session_id"""
    session = fetch_session_by_id(session_id)
    if not session:
        return jsonify({"message": "Session not found"}), 404

    if not is_owner_session(user_id, session):
        return jsonify({"message": "Unauthorized"}), 401

    session_response = end_session(session)
    if not session_response:
        return jsonify({"message": "ERROR"}), 500
    return jsonify({"message": "Session terminated"}), 200
    # TODO continuer


# endregion
