from flask import Blueprint, request
from app.utils.jwt_utils import jwt_required, admin_required
from app.controllers.card_controller import create_card_controller
from app.routes.deck_route import deck_bp

card_bp = Blueprint("card_bp", __name__, url_prefix="/users/decks/cards")


# todo possibilité d'automatiser avec un middleware pour éviter de rappeler la route a chaque fois
# region POST
@deck_bp.route("/<int:deck_id>/cards", methods=["POST"])
@jwt_required
def create_card(user_id, role, deck_id):
    data = request.get_json()
    create_card_controller(user_id, deck_id, data)


# BESOIN
# user id
# deck id
# data composé de toutes les informations pour une carte

# QUESTION
# est ce que tout peux être contenu dans ma requete json ?

# endregion


# region GET
@card_bp.route("/", methods=["GET"])
def get_all_cards():
    pass


@card_bp.route("/<int:id>", methods=["GET"])
def get_card():
    pass


@card_bp.route("/draw", methods=["GET"])
def get_random_card():
    pass


# endregion

# region UPDATE

# endregion

# region DELETE

# endregion
