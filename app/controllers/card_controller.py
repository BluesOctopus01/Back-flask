from app.models.cards_models.card_answer_qcm import AnswerQcm
from app.models.cards_models.card_gapfill import Gapfill
from app.models.cards_models.card_base import Card
from app.models.cards_models.card_image import Image
from app.models.cards_models.card_qa import Qa
from app.models.cards_models.card_qcm import Qcm

from app.DTO.card_dto import (
    QaCreateDTO,
    QcmCreateDTO,
    ImageCreateDTO,
    GapfillCreateDTO,
    QaPatchDTO,
    QcmPatchDTO,
    ImagePatchDTO,
    GapfillPatchDTO,
)
from app.services.card_service import (
    factorized_create_card,
    get_cards_deck,
    get_all_cards,
    get_card_by_id,
    factorized_patch_card,
)
from app.services.deck_service import get_deck_search
from app.services.deck_service import is_owner
from flask import jsonify, request


# region POST
def create_card_controller(user_id, deck_id, data):
    """EndPoint : POST /users/deck/:id/cards"""

    if not is_owner(user_id, deck_id):
        return jsonify({"message": "Unauthorized"}), 401

    card_type = data.get("card_type")

    if card_type not in ["qcm", "qa", "image", "gapfill"]:
        return jsonify({"message": "Invalid card_type"}), 400
    data["deck_id"] = deck_id

    if card_type == "qcm":
        dto, err = QcmCreateDTO.from_json(data)

    if card_type == "qa":
        dto, err = QaCreateDTO.from_json(data)

    if card_type == "image":
        dto, err = ImageCreateDTO.from_json(data)

    if card_type == "gapfill":
        dto, err = GapfillCreateDTO.from_json(data)
    if err:
        return jsonify(err), 400

    card = factorized_create_card(dto)
    if not card:
        return jsonify({"message": "unkown error"}), 500

    response = card.to_dict()
    return jsonify(response), 201


# endregion


# region GET
def get_card_deck_controller(user_id, deck_id, data_access):
    """EndPoint : GET /users/deck/:id/cards/"""
    # todo filtre type de cartes ect

    deck, err = get_deck_search(user_id, deck_id, data_access)

    if err:
        return jsonify(err), 403

    try:
        cards = get_cards_deck(deck_id)
        cards_dict = [card.to_dict() for card in cards]
        return jsonify(cards_dict), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch cards", "details": str(e)}), 500


def get_all_cards_controller():
    """EndPoint : GET /users/deck/cards/"""
    cards = get_all_cards()
    cards_dict = [card.to_dict() for card in cards]
    return jsonify(cards_dict), 200


def get_card_by_id_controller(user_id, deck_id, card_id, data_access):
    """EndPoint : GET /users/deck/:id/cards/:id/"""
    #!!!todo verifier quand on fait un get qu'on ne doivent pas tout le temps mettre le mot de passe
    deck, err = get_deck_search(user_id, deck_id, data_access)
    if err:
        return jsonify(err), 403

    card = get_card_by_id(deck_id, card_id)
    if not card:
        return jsonify({"message": "card not found"}), 404

    if card.deck_id != deck_id:
        return jsonify({"error": "Card does not belong to this deck"}), 400

    cards_dict = card.to_dict()
    return jsonify(cards_dict), 200


# endregion


# region UPDATE
# todo continuer
def patch_card_controller(user_id, deck_id, card_id, data):

    if not is_owner(user_id, deck_id):
        return jsonify({"message": "Unauthorized"}), 401

    card = get_card_by_id(card_id)
    if not card:
        return jsonify({"message": "Card not found"}), 404
    card_type = card.card_type

    if card_type == "qcm":
        dto, err = QcmPatchDTO.from_json(data)

    if card_type == "qa":
        dto, err = QaPatchDTO.from_json(data)

    if card_type == "image":
        dto, err = ImagePatchDTO.from_json(data)

    if card_type == "gapfill":
        dto, err = GapfillPatchDTO.from_json(data)
    if err:
        return jsonify(err), 400
    card = factorized_patch_card(card_type, dto)
    if not card:
        return jsonify({"message": "unkown error"}), 500

    response = card.to_dict()
    return jsonify(response), 201


# endregion

# region DELETE

# endregion
