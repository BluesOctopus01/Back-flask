from flask import Blueprint, request
from app.utils.jwt_utils import jwt_required, admin_required
from app.controllers.card_controller import (
    create_card_controller,
    get_card_deck_controller,
    get_all_cards_controller,
    get_card_by_id_controller,
    patch_card_controller,
    delete_card_controller,
    delete_card_admin_controller,
)
from app.routes.deck_route import deck_bp

card_bp = Blueprint("card_bp", __name__, url_prefix="/users/decks/cards")


# todo possibilité d'automatiser avec un middleware pour éviter de rappeler la route a chaque fois
# region POST
@deck_bp.route("/<int:deck_id>/cards", methods=["POST"])
@jwt_required
def create_card(user_id, role, deck_id):
    data = request.get_json()
    return create_card_controller(user_id, deck_id, data)


# endregion


# region GET
@deck_bp.route("/<int:deck_id>/cards", methods=["GET"])
@jwt_required
def get_card_deck(user_id, role, deck_id):
    access_key = request.args.get("access_key")
    data_access = {"access_key": access_key} if access_key else {}
    return get_card_deck_controller(user_id, deck_id, data_access)


@card_bp.route("/", methods=["GET"])
@admin_required
def get_all_cards():
    return get_all_cards_controller()


@deck_bp.route("/<int:deck_id>/cards/<int:card_id>", methods=["GET"])
@jwt_required
def get_a_card(user_id, role, deck_id, card_id):
    access_key = request.args.get("access_key")
    data_access = {"access_key": access_key} if access_key else {}
    return get_card_by_id_controller(user_id, deck_id, card_id, data_access)


# endregion


# region UPDATE
# todo continuer
@deck_bp.route("/<int:deck_id>/cards/<int:card_id>", methods=["PATCH"])
@jwt_required
def update_a_card(user_id, role, deck_id, card_id):
    data = request.get_json()

    return patch_card_controller(user_id, deck_id, card_id, data)


# endregion


# region DELETE
# todo continuer
@deck_bp.route("/<int:deck_id>/cards/<int:card_id>", methods=["DELETE"])
@jwt_required
def delete_card(user_id, role, deck_id, card_id):
    return delete_card_controller(user_id, deck_id, card_id)


@deck_bp.route("/<int:deck_id>/cards/<int:card_id>", methods=["DELETE"])
@admin_required
def delete_card_admin(card_id):
    return delete_card_admin_controller(card_id)


# endregion
