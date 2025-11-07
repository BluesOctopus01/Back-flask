from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Tuple, Dict
import re
from app.utils.verify_utils import VerifyUtils


@dataclass
class CardCreateDTO:
    """Model to create a Base card"""

    # champ de base
    card_type: str
    question: str
    deck_id: int

    VALID_CARD_TYPE = {"qcm", "qa", "image", "gapfill"}

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["CardCreateDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a CardCreateDTO"""
        if not data:
            return None, {"error": "No data provided"}

        card_type = (data.get("card_type") or "").strip()
        question = (data.get("question") or "").strip()
        deck_id = data.get("deck_id")

        required_fields = {
            "card_type": card_type,
            "question": question,
            "deck_id": deck_id,
        }
        for field, value in required_fields.items():
            if not value:
                return None, {"error": f"Missing field: {field}"}

        if card_type not in CardCreateDTO.VALID_CARD_TYPE:
            return None, {"error": f"Invalid card_type: {card_type}"}

        return CardCreateDTO(card_type, question, deck_id), None


@dataclass
class QaCreateDTO(CardCreateDTO):
    """Model to create a Question Answer type of card"""

    answer: str

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["QaCreateDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a QaCreateDTO"""
        # Verifie les données a travers le DTO de base puis passe au type
        base_dto, error = CardCreateDTO.from_json(data)
        if error:
            return None, error

        answer = (data.get("answer") or "").strip()

        if not answer:
            return None, {"error": "Missing field: answer"}

        return (
            QaCreateDTO(
                card_type=base_dto.card_type,
                question=base_dto.question,
                deck_id=base_dto.deck_id,
                answer=answer,
            ),
            None,
        )


@dataclass
class GapfillCreateDTO(CardCreateDTO):
    """Model to create a gap fill type of card"""

    text1: str
    text2: str
    answer: str

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["GapfillCreateDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a GapfillCreateDTO"""
        # Verifie les données a travers le DTO de base puis passe au type
        base_dto, error = CardCreateDTO.from_json(data)
        if error:
            return None, error

        text1 = (data.get("text1") or "").strip().capitalize()
        text2 = (data.get("text2") or "").strip()
        answer = (data.get("answer") or "").strip()

        required_fields = {
            "text1": text1,
            "text2": text2,
            "answer": answer,
        }
        for field, value in required_fields.items():
            if not value:
                return None, {"error": f"Missing field: {field}"}
        return (
            GapfillCreateDTO(
                card_type=base_dto.card_type,
                question=base_dto.question,
                deck_id=base_dto.deck_id,
                text1=text1,
                text2=text2,
                answer=answer,
            ),
            None,
        )


@dataclass
class ImageCreateDTO(CardCreateDTO):
    text_alt: str
    url: str
    answer: str

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["ImageCreateDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a ImageCreateDTO"""
        # Verifie les données a travers le DTO de base puis passe au type
        base_dto, error = CardCreateDTO.from_json(data)
        if error:
            return None, error

        text_alt = (data.get("text_alt") or "").strip()
        url = (data.get("url") or "").strip()
        answer = (data.get("answer") or "").strip()

        required_fields = {
            "text_alt": text_alt,
            "url": url,
            "answer": answer,
        }
        for field, value in required_fields.items():
            if not value:
                return None, {"error": f"Missing field: {field}"}
        return (
            ImageCreateDTO(
                card_type=base_dto.card_type,
                question=base_dto.question,
                deck_id=base_dto.deck_id,
                text_alt=text_alt,
                url=url,
                answer=answer,
            ),
            None,
        )


@dataclass
class QcmCreateDTO(CardCreateDTO):
    """Validate and parse a JSON dict into a QcmCreateDTO, send back answers to create them"""

    answer: list[Dict[str, object]]

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["QcmCreateDTO"], Optional[Dict]]:
        """Validate and parse a JSON dict into a QcmCreateDTO"""
        # Verifie les données a travers le DTO de base puis passe au type
        base_dto, error = CardCreateDTO.from_json(data)
        if error:
            return None, error

        answers = data.get("answer")
        # Verification si il y a bien une instance de réponses
        if not isinstance(answers, list) or not answers:
            return None, {"error": "Answer must be a non-empty list"}
        #!! Compliquer
        # TODO a relire
        # i = index, a = dictionnaire a cette position
        for i, a in enumerate(answers):
            if not isinstance(a, dict):
                # on verifie que c'est bien un dico
                return None, {"error": f"Answer at index {i} must be a dictionary"}
            # on verifie qu'on a bien answer et valid
            if "answer" not in a or "valid" not in a:
                return None, {"error": f"Missing keys in answer at index {i}"}
            # on verifie le type
            if not isinstance(a["answer"], str):
                return None, {"error": f"'answer' must be a string at index {i}"}
            if not isinstance(a["valid"], bool):
                return None, {"error": f"'valid' must be a boolean at index {i}"}

            a["answer"] = a["answer"].strip()
            if not a["answer"]:
                return None, {"error": f"Answer at index {i} cannot be empty"}

            # { } crée un set CE QUI FILTRE LES DOUBLONS AUTOMATIQUEMENT
            unique_answers = {a["answer"] for a in answers}

            if len(unique_answers) < 4:
                return None, {"error": "There must be at least 4 different answers"}
            if not any(a["valid"] for a in answers):
                return None, {"error": "There must be at least one correct answer"}

        return (
            QcmCreateDTO(
                card_type=base_dto.card_type,
                question=base_dto.question,
                deck_id=base_dto.deck_id,
                answer=answers,
            ),
            None,
        )


# {
#   "card_type": "qcm",
#   "question": "Quels langages sont compilés ?",
#   "deck_id": 1,
#   "answers": [
#     1{"answer": "Python", "valid": false},
#     2{"answer": "C++", "valid": true},
#     3{"answer": "Java", "valid": true},
#     4{"answer": "HTML", "valid": false}
#   ]
# }
