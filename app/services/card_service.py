from app.models.cards_models.card_answer_qcm import AnswerQcm
from app.models.cards_models.card_gapfill import Gapfill
from app.models.cards_models.card_base import Card
from app.models.cards_models.card_image import Image
from app.models.cards_models.card_qa import Qa
from app.models.cards_models.card_qcm import Qcm

from app.models import db
from app.services.deck_service import get_deck

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


# region POST


def factorized_create_card(
    dto: Gapfill | Image | Qa | Qcm,
) -> Gapfill | Image | Qa | Qcm | None:
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


def create_card_Qcm(dto: QcmCreateDTO) -> Qcm:
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


def create_card_Qa(dto: QaCreateDTO) -> Qa:
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


def create_card_Gapfill(dto: GapfillCreateDTO) -> Gapfill:
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


def create_card_Image(dto: ImageCreateDTO) -> Image:
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
# todo verifier
def factorized_patch_card(
    card_id: int,
    card_type: str,
    dto: QcmPatchDTO | QaPatchDTO | ImagePatchDTO | GapfillPatchDTO,
) -> Gapfill | Image | Qa | Qcm | None:
    """Receive a dto and create a card by checking is "card_type", returning the propre type of card
    in the case of a Qcm card, create severals answerQcm instances and update everything
    """
    # fetch the card to get it's type

    # check the type
    if card_type == "qcm":
        return patch_card_Qcm(card_id, dto)

    elif card_type == "qa":
        return patch_card_Qa(card_id, dto)

    elif card_type == "image":
        return patch_card_Image(card_id, dto)

    elif card_type == "gapfill":
        return patch_card_Gapfill(card_id, dto)

    return None


# todo a verifier
#!!Le patch ici permet égalkement de créer de nouvelles réponses
def patch_card_Qcm(card_id: int, dto: QcmPatchDTO):
    """Patch an existing QCM card and its answers"""
    # 1. Récupérer la carte existante
    card_update = db.session.get(Qcm, card_id)
    if not card_update:
        return None

    # 2. Mettre à jour la question si présente
    if dto.question:
        card_update.question = dto.question

    # 3. Mettre à jour ou ajouter les réponses
    if dto.answers is not None:
        for a in dto.answers:
            answer_id = a.get("id")
            if answer_id:
                # Mise à jour d'une réponse existante
                existing = db.session.get(AnswerQcm, answer_id)
                if existing and existing.qcm_id == card_id:
                    if "answer" in a:
                        existing.answer = a["answer"]
                    if "valid" in a:
                        existing.valid = a["valid"]
            else:
                # Création d'une nouvelle réponse
                if "answer" in a and "valid" in a:
                    new_answer = AnswerQcm(
                        answer=a["answer"], valid=a["valid"], qcm_id=card_id
                    )
                    db.session.add(new_answer)

    # 4. Commit final
    db.session.commit()
    return card_update


def patch_card_Qa(card_id: int, dto: QaPatchDTO):
    """Patch an existing QA card"""
    card_update = db.session.get(Qa, card_id)

    if not card_update:
        return None

    if dto.question:
        card_update.question = dto.question
    if dto.answer:
        card_update.answer = dto.answer

    db.session.commit()
    return card_update


def patch_card_Image(card_id: int, dto: ImagePatchDTO):
    """Patch an existing Image card"""
    card_update = db.session.get(Image, card_id)

    if not card_update:
        return None

    if dto.question:
        card_update.question = dto.question
    if dto.answer:
        card_update.answer = dto.answer
    if dto.text_alt:
        card_update.text_alt = dto.text_alt
    if dto.url:
        card_update.url = dto.url

    db.session.commit()
    return card_update


def patch_card_Gapfill(card_id: int, dto: GapfillPatchDTO):
    """Patch an existing Gapfill card"""
    card_update = db.session.get(Image, card_id)

    if not card_update:
        return None

    if dto.text1:
        card_update = dto.text1
    if dto.text2:
        card_update = dto.text2
    if dto.answer:
        card_update = dto.answer

    db.session.commit()
    return card_update


# endregion

# region DELETE

# endregion
