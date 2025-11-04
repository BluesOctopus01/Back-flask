from app.models.deck import Deck
from app.services.deck_service import (
    post_deck,
    get_deck_user,
    get_deck,
    get_deck_search,
    patch_deck_user,
)
from app.services.user_service import fetch_a_user
from app.DTO.deck_dto import DeckCreateDTO, DeckPatchDTO
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


def get_deck_controller(user_id, deck_id, data_access):
    deck, err = get_deck_search(user_id, deck_id, data_access)
    if err:
        error_message = err.get("error")
        # back up si il ne rentre dans aucune conditions
        status = 400

        if error_message == "Deck not found":
            status = 404
        if error_message == "Invalid credentials":
            status = 403
        if error_message == "Unauthorized":
            status = 401

        return jsonify(err), status

    deck_response = deck.to_dict()
    return jsonify(deck_response), 200


def update_deck_controller(user_id, deck_id, data):
    creator = fetch_a_user(user_id)
    if not creator:
        return jsonify({"message": "user not found"}), 404

    deck = get_deck(deck_id)
    if not deck:
        return jsonify({"message": "deck not found"}), 404

    if deck.creator_id != user_id:
        return jsonify({"message": "Unauthorized"}), 401

    dto, err = DeckPatchDTO.from_json(data)
    if err:
        return jsonify(err), 400
    updated_deck = patch_deck_user(
        deck_id, dto.name, dto.bio, dto.access, dto.image, dto.access_key
    )
    if not updated_deck:
        return jsonify({"error": "Unknown error"}), 501

    response_data = deck.to_dict()
    return jsonify(response_data), 200


def delete_deck_controller():
    pass
