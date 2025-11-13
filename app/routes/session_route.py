from flask import Blueprint, request

from app.utils.jwt_utils import jwt_required, admin_required

from app.controllers.session_controller import (
    create_session_controller,
    end_session_controller,
    join_session_controller,
    join_session_by_id_controller,
    all_sessions_by_user_controller,
    admin_all_sessions,
    update_session_controller,
)

session_bp = Blueprint("session_bp", __name__, url_prefix="/sessions/")


# TODO piocher des cartes aléatoire, crée la session, la finir, la quiter, reaccédé


# region POST
@session_bp.route("/decks/<int:deck_id>", methods=["POST"])
@jwt_required
def create_session(user_id, role, deck_id):
    access_key = request.args.get("access_key")
    data_access = {"access_key": access_key} if access_key else {}
    return create_session_controller(user_id, deck_id, data_access)


# endregion


# region GET
@session_bp.route("/", methods=["GET"])
@jwt_required
def join_session_active(user_id, role):
    return join_session_controller(user_id)


@session_bp.route("/<int:session_id>", methods=["GET"])
@jwt_required
def join_session_by_id(user_id, role, session_id):
    return join_session_by_id_controller(user_id, session_id)


@session_bp.route("/user/history", methods=["GET"])
@jwt_required
def history_session(user_id, role):
    return all_sessions_by_user_controller(user_id)


@session_bp.route("/admin", methods=["GET"])
@admin_required
def get_all_sessions():
    return admin_all_sessions()


# endregion


# region UPDATE
@session_bp.route("/<int:session_id>", methods=["PATCH"])
@jwt_required
def pause_session(user_id, role, session_id):
    data = request.get_json()
    return update_session_controller(user_id, session_id, data)


# endregion


# region DELETE
@session_bp.route("/<int:session_id>", methods=["DELETE"])
@jwt_required
def end_session(user_id, role_id, session_id):
    return end_session_controller(user_id, session_id)
    # endregion
