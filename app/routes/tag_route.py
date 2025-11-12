from flask import Blueprint, request
from app.utils.jwt_utils import jwt_required, admin_required
from app.controllers.tag_controller import (
    create_tag_controller,
    get_all_tags_controller,
    get_tag_id_controller,
    patch_tag_controller,
    delete_tag_controller,
)


tag_bp = Blueprint("tag_bp", __name__, url_prefix="/tags")


# region POST
@tag_bp.route("/", methods=["POST"])
@admin_required
def create_tag():
    data = request.get_json()
    return create_tag_controller(data)


# endregion


# region GET
@tag_bp.route("/", methods=["GET"])
def get_tags():
    return get_all_tags_controller()


@tag_bp.route("/<int:tag_id>", methods=["GET"])
def get_tag_id(tag_id):
    return get_tag_id_controller(tag_id)


# endregion


# region UPDATE
@admin_required
@tag_bp.route("/<int:tag_id>", methods=["PATCH"])
def update_tag(tag_id):
    data = request.get_json()
    return patch_tag_controller(tag_id, data)


# endregion


# region DELETE
@admin_required
@tag_bp.route("/<int:tag_id>", methods=["DELETE"])
def delete_tag(tag_id):
    return delete_tag_controller(tag_id)


# endregion
