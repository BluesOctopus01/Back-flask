from app.models.deck import Deck
from app.services.deck_service import (
    post_deck,
    get_deck_user,
    get_deck,
    get_deck_search,
    patch_deck_user,
    delete_deck_service,
    get_decks,
    delete_deck_admin,
)
from app.services.user_service import fetch_a_user
from app.DTO.deck_dto import DeckCreateDTO, DeckPatchDTO
from flask import jsonify, request


# region POST


def create_deck_controller(user_id, data):

    creator = fetch_a_user(user_id)
    if not creator:
        return jsonify({"message": "user not found"}), 404
    data["creator_id"] = user_id
    tags = data.get("tags", [])

    dto, err = DeckCreateDTO.from_json(data)
    if err:
        return jsonify(err), 400
    new_deck = post_deck(
        dto.name, dto.bio, dto.access, dto.image, dto.access_key, dto.creator_id, tags
    )
    response_data = new_deck.to_dict()
    return jsonify(response_data), 201


# endregion


# region GET


def get_user_decks_controller(user_id):
    """EndPoint : GET /users/decks"""
    creator = fetch_a_user(user_id)
    if not creator:
        return jsonify({"message": "user not found"}), 404

    decks = get_deck_user(user_id)
    if not decks:
        return jsonify({"message": "decks not found"}), 404
    decks_dict = [deck.to_dict() for deck in decks]
    return jsonify(decks_dict), 200


def get_deck_controller(user_id, deck_id, data_access):
    """EndPoint : GET /users/decks/int:id"""
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


def get_all_decks_controller():
    """EndPoint : GET /users/decks/admin"""
    try:
        decks = get_decks()
        decks_dict = [deck.to_dict() for deck in decks]
        return jsonify(decks_dict), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch decks", "details": str(e)}), 500


# endregion


# region UPDATE
def update_deck_controller(user_id, deck_id, data):
    """EndPoint : PATCH /users/decks/int:id"""
    creator = fetch_a_user(user_id)
    add_tags = data.get("add_tags", [])
    remove_tags = data.get("remove_tags", [])
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
        deck_id,
        dto.name,
        dto.bio,
        dto.access,
        dto.image,
        dto.access_key,
        add_tags,
        remove_tags,
    )
    if not updated_deck:
        return jsonify({"error": "Unknown error"}), 501

    response_data = updated_deck.to_dict()
    return jsonify(response_data), 200


# endregion


# region DELETE
def delete_deck_controller(user_id, deck_id):
    """EndPoint : DELETE /users/decks/int:id"""
    creator = fetch_a_user(user_id)
    if not creator:
        return jsonify({"message": "user not found"}), 404

    deck = get_deck(deck_id)
    if not deck:
        return jsonify({"message": "deck not found"}), 404

    if deck.creator_id != user_id:
        return jsonify({"message": "Unauthorized"}), 401

    deck_delete = delete_deck_service(deck_id)
    if not deck_delete:
        return jsonify({"message": "unexpected error"}), 500
    return jsonify({"message": "deck deleted successfully"}), 200


def delete_deck_admin_controller(deck_id):
    """EndPoint : DELETE /users/decks/int:id"""
    deck = delete_deck_admin(deck_id)
    if not deck:
        return jsonify({"message": "deck not found"}), 404
    return jsonify({"message": "deck deleted successfully"}), 200


# endregion
