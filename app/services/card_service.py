from app.models.cards_models.card_answer_qcm import AnswerQcm
from app.models.cards_models.card_gapfill import Gapfill
from app.models.cards_models.card_base import Card
from app.models.cards_models.card_image import Image
from app.models.cards_models.card_qa import Qa
from app.models.cards_models.card_qcm import Qcm

from app.models import db


# region POST
# todo en dernier, le plus compliqué
def create_card_qcm(card_type: str, question: str, deck_id: int):
    pass


def create_card_Qa(dto) -> Qa:
    """Return a created Card"""
    new_card = Qa(
        card_type=dto.card_type,
        question=dto.question,
        deck_id=dto.deck_id,
        answer=dto.answer,
    )

    db.session.add(new_card)
    db.session.commit()
    return new_card


def create_card_Gapfill(
    card_type: str, question: str, deck_id: int, text1: str, text2: str, answer: str
):
    pass


def create_card_Image(
    card_type: str, question: str, deck_id: int, text_alt: str, url: str, answer: str
):
    pass


# endregion
# region GET

# endregion

# region UPDATE

# endregion

# region DELETE

# endregion
