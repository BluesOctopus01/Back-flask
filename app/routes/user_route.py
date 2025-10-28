from flask import Blueprint, request, jsonify

from app.utils.jwt_utils import jwt_required, admin_required, generate_token

from app.controllers.user_controller import (
    post_user_controller,
    get_users_controller,
    login_user_controller,
    get_user_controller,
    update_user_controller,
)

user_bp = Blueprint("user_bp", __name__, url_prefix="/users/")


# region POST
@user_bp.route("/register", methods=["POST"])
def register_user_route():
    data = request.get_json()
    return post_user_controller(data)


@user_bp.route("/login", methods=["POST"])
def login_user_route():
    data = request.get_json()
    return login_user_controller(data)


# endregion


# region GET
@user_bp.route("/profiles/<id>", methods=["GET"])
def get_user_route(id):
    return get_user_controller(id)


@user_bp.route("/admin", methods=["GET"])
@admin_required
def get_all_users_route():
    return get_users_controller()


# endregion


# region UPDATE
@jwt_required
@user_bp.route("/update", methods=["PUT"])
def update_user_profile(user_id, role):
    data = request.get_json()
    return update_user_controller(user_id, data)


@jwt_required
@user_bp.route("/update_password", methods=["PATCH"])
def update_user_psw(id):
    # TODO
    pass


# endregion


# region DELETE


@user_bp.route("/delete", methods=["PATCH"])
@jwt_required
def soft_delete_user_self():
    # TODO
    pass


@user_bp.route("delete/<id>", methods=["PATCH"])
@admin_required
def soft_delete_user(id):
    # TODO
    pass


# endregion
