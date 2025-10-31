from flask import Blueprint, request
from app.utils.jwt_utils import jwt_required, admin_required
from app.controllers.deck_controller import (
    create_deck_controller,
    get_deck_controller,
    delete_deck_controller,
    update_deck_controller,
    get_user_decks_controller,
)

deck_bp = Blueprint("deck_bp", __name__, url_prefix="/users/decks")


@deck_bp.route("/create", methods=["POST"])
@jwt_required
def create_deck(user_id, role):
    data = request.get_json()
    return create_deck_controller(user_id, data)


@deck_bp.route("/", methods=["GET"])
@jwt_required
def get_decks(user_id, role):
    return get_user_decks_controller(user_id)


@deck_bp.route("/<deck_id: int>", methods=["GET"])
@jwt_required
def get_deck(user_id, role, deck_id):
    data = request.get_json()
    return get_deck_controller(user_id, deck_id, data)
    # verifier si le deck appartient a l'user
    # si non, verifier l'accessibilité du deck
    # si protected, verifier le mot de passer pour le voir
    # verifier si l'user est admin, .


# todo get admin


@deck_bp.route("/<deck_id>", methods=["PUT"])
@jwt_required
def update_deck(user_id, role, deck_id):
    data = request.get_json()
    return update_deck_controller(user_id, deck_id, data)


@deck_bp.route("/<deck_id>", methods=["DELETE"])
@jwt_required
def delete_deck(user_id, role, deck_id):
    return delete_deck_controller(user_id, deck_id)
