from flask import Blueprint, request
from app.utils.jwt_utils import jwt_required, admin_required
from app.controllers.deck_controller import *

deck_bp = Blueprint("deck_bp", __name__, url_prefix="/users/<user_id>/decks")


@deck_bp.route("/", methods=["POST"])
@jwt_required
def create_deck(user_id, role):
    data = request.get_json()
    # return create_deck_controller(user_id, data)
    pass


@deck_bp.route("/", methods=["GET"])
@jwt_required
def get_decks(user_id, role):
    # return get_user_decks_controller(user_id)
    pass


@deck_bp.route("/<deck_id>", methods=["GET"])
@jwt_required
def get_deck(user_id, role, deck_id):
    # return get_deck_controller(user_id, deck_id)
    pass


@deck_bp.route("/<deck_id>", methods=["PUT"])
@jwt_required
def update_deck(user_id, role, deck_id):
    data = request.get_json()
    # return update_deck_controller(user_id, deck_id, data)
    pass


@deck_bp.route("/<deck_id>", methods=["DELETE"])
@jwt_required
def delete_deck(user_id, role, deck_id):
    # return delete_deck_controller(user_id, deck_id)
    pass
