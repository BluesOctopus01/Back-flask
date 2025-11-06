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
from app.services.card_service import (
    create_card_Gapfill,
    create_card_Image,
    create_card_Qa,
    create_card_qcm,
)
from app.services.deck_service import is_owner
from flask import jsonify, request


# region POST
def create_card_controller(user_id, deck_id, data):

    if not is_owner(user_id, deck_id):
        return jsonify({"message": "Unauthorized"}), 401

    data["deck_id"] = deck_id
    #todo centraliser toute la logique pour créer un service
    # todo en dernier, le plus compliqué
    if data["card_type"] == "qcm":
        dto, err = QaCreateDTO.from_json(data)
        card = create_card_qcm(dto)

    if data["card_type"] == "qa":
        dto, err = GapfillCreateDTO.from_json(data)
        card = create_card_Qa(dto)

    if data["card_type"] == "image":
        dto, err = GapfillCreateDTO.from_json(data)

    if data["card_type"] == "gapfill":
        dto, err = QcmCreateDTO.from_json(data)
    if err:
        return jsonify({err}), 400
    if dto:
        


# endregion

# region GET

# endregion

# region UPDATE

# endregion

# region DELETE

# endregion
