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
)
from app.services.card_service import factorized_create_card
from app.services.deck_service import is_owner
from flask import jsonify, request


# region POST
def create_card_controller(user_id, deck_id, data):

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

# endregion

# region UPDATE

# endregion

# region DELETE

# endregion
