from app.models.session_models.session import Session

from flask import jsonify, request
from app.utils.jwt_utils import generate_token

from app.services.session_service import *
from app.services.deck_service import get_deck_search
from app.services.session_service import (
    fetch_session_by_id,
    is_owner_session,
    fetch_session_by_user_id,
)


# region POST
def create_session_controller(user_id, deck_id, data_access):

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
def join_session_controller(user_id, session_id):
    session = fetch_session_by_id(session_id)
    if not session:
        return jsonify({"message": "Session not found"}), 404

    own_session = is_owner_session(user_id, session)
    if not own_session:
        return jsonify({"message": "Unauthorized"}), 401

    response_session = session.to_dict()

    return jsonify(response_session), 200


# endregion


# region UPDATE
def update_session_controller():
    session = fetch_session_by_id()


# endregion


# region DELETE
def end_session_controller():
    pass


# endregion
