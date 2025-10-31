from app.models.deck import Deck
from app.services.deck_service import post_deck, get_deck_user, get_deck, is_owner_deck
from app.services.user_service import fetch_a_user
from app.DTO.deck_dto import DeckCreateDTO
from flask import jsonify, request


def create_deck_controller(user_id, data):
    creator = fetch_a_user(user_id)
    if not creator:
        return jsonify({"message": "user not found"}), 404
    data["creator_id"] = user_id
    dto, err = DeckCreateDTO.from_json(data)
    if err:
        return jsonify(err), 400
    new_deck = post_deck(
        dto.name, dto.bio, dto.access, dto.image, dto.access_key, dto.creator_id
    )
    response_data = new_deck.to_dict()
    return jsonify(response_data), 201


def get_user_decks_controller(user_id):
    creator = fetch_a_user(user_id)
    if not creator:
        return jsonify({"message": "user not found"}), 404

    decks = get_deck_user(user_id)
    if not decks:
        return jsonify({"message": "decks not found"}), 404
    decks_dict = [deck.to_dict() for deck in decks]
    return jsonify(decks_dict), 200


# todo retravailler ca pour une meilleure logique métier
# def get_deck_controller(user_id, deck_id, data):
#     deck = get_deck(deck_id, user_id)
#     if not deck:
#         return jsonify({"message": "deck not found"}), 404
#     owner = is_owner_deck(user_id, deck_id)
#     if not owner:
#         pass


def update_deck_controller():
    pass


def delete_deck_controller():
    pass
