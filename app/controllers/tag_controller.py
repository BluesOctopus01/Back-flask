from app.models.tags import Tag, TagDeck
from app.models.deck import Deck

from app.DTO.tag_dto import TagCreateDTO, TagPatchDTO

from flask import jsonify, request
from app.utils.jwt_utils import generate_token

from app.services.tag_service import (
    create_tag,
    fetch_tag_by_id,
    fetch_all_tags,
    patch_tag,
    delete_tag,
)


# region POST
def create_tag_controller(data):
    """EndPoint : POST /tags/"""
    dto, err = TagCreateDTO.from_json(data)
    if err:
        return jsonify(err), 400
    new_tag = create_tag(dto.name, dto.description)

    response_data = new_tag.to_dict()
    return jsonify(response_data), 201


# endregion


# region GET
def get_all_tags_controller():
    """EndPoint : GET /tags/"""
    try:
        tags = fetch_all_tags()
        tags_dict = [tag.to_dict() for tag in tags]
        return jsonify(tags_dict), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch tags", "details": str(e)}), 500


def get_tag_id_controller(tag_id):
    """EndPoint : GET /tags/:tag_id"""
    tag = fetch_tag_by_id(tag_id)
    if not tag:
        return jsonify({"message": "tag not found"}), 404
    response_data = tag.to_dict()
    return jsonify(response_data), 200


# endregion


# region UPDATE
def patch_tag_controller(tag_id, data):
    """EndPoint : PATCH /tags/:tag_id"""
    dto, err = TagPatchDTO.from_json(data)
    if err:
        return jsonify(err), 403
    tag = patch_tag(tag_id, dto.name, dto.description)

    if not tag:
        return jsonify({"message": "tag not found"}), 404
    response_data = tag.to_dict()
    return jsonify(response_data), 200


# endregion


# region DELETE
def delete_tag_controller(tag_id):
    """EndPoint : DELETE /tags/:tag_id"""
    tag = delete_tag(tag_id)
    if not tag:
        return jsonify({"message": "tag not found"}), 404
    return jsonify({"message": "Tag deleted successfully"}), 200


# endregion
