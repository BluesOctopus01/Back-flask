from app.models.cards_models.card_answer_qcm import AnswerQcm
from app.models.cards_models.card_gapfill import Gapfill
from app.models.cards_models.card_base import Card
from app.models.cards_models.card_image import Image
from app.models.cards_models.card_qa import Qa
from app.models.cards_models.card_qcm import Qcm

from app.models import db
from app.services.deck_service import get_deck

import random

used_cards_by_deck: dict[int, list[int]] = {}

# region POST


def factorized_create_card(dto) -> Gapfill | Image | Qa | Qcm | None:
    """Receive a dto and create a card by checking is "card_type", returning the propre type of card
    in the case of a Qcm card, create severals answerQcm instances"""
    # check the type
    if dto.card_type == "qcm":
        return create_card_Qcm(dto)

    elif dto.card_type == "qa":
        return create_card_Qa(dto)

    elif dto.card_type == "image":
        return create_card_Image(dto)

    elif dto.card_type == "gapfill":
        return create_card_Gapfill(dto)

    return None


def create_card_Qcm(dto) -> Qcm:
    """Return a card Question Answer and create Answers"""
    new_card = Qcm(
        card_type=dto.card_type,
        question=dto.question,
        deck_id=dto.deck_id,
    )
    db.session.add(new_card)
    db.session.flush()

    for a in dto.answers:
        new_answer = AnswerQcm(answer=a["answer"], valid=a["valid"], qcm_id=new_card.id)
        db.session.add(new_answer)

    db.session.commit()
    return new_card


def create_card_Qa(dto) -> Qa:
    """Return a card Question Answer"""
    new_card = Qa(
        card_type=dto.card_type,
        question=dto.question,
        deck_id=dto.deck_id,
        answer=dto.answer,
    )

    db.session.add(new_card)
    db.session.commit()
    return new_card


def create_card_Gapfill(dto) -> Gapfill:
    """Return a card Gapfill"""
    new_card = Gapfill(
        card_type=dto.card_type,
        question=dto.question,
        deck_id=dto.deck_id,
        text1=dto.text1,
        text2=dto.text2,
        answer=dto.answer,
    )

    db.session.add(new_card)
    db.session.commit()
    return new_card


def create_card_Image(dto) -> Image:
    """Return a card Image"""
    new_card = Image(
        card_type=dto.card_type,
        question=dto.question,
        deck_id=dto.deck_id,
        text_alt=dto.text_alt,
        url=dto.url,
        answer=dto.answer,
    )

    db.session.add(new_card)
    db.session.commit()
    return new_card


# endregion
# region GET


def get_cards_deck(deck_id: int) -> list[Card]:
    """Return a list of cards in a deck"""
    deck = get_deck(deck_id)
    if not deck:
        return None
    return deck.cards


def get_all_cards() -> list[Card]:
    """Return a list of all cards"""
    cards = Card.query.all()
    return cards


def get_card_by_id(deck_id: int, card_id: int) -> Card | None:
    """Return a card"""
    card = Card.query.filter_by(id=card_id, deck_id=deck_id).first()
    if not card:
        return None
    return card


# endregion


# region UPDATE
def patch_card():
    pass


# endregion

# region DELETE

# endregion
