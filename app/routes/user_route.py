from flask import Blueprint, request, jsonify

from app.utils.jwt_utils import jwt_required, admin_required, generate_token

from app.controllers.user_controller import get_users_controller, post_user_controller

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")
admin_bp = Blueprint("admin_bp", __name__, url_prefix="/users/admin")


# region USER ROUTE
@user_bp.route("/", methods=["POST"])
def register_user():
    data = request.get_json()
    user = post_user_controller(data)


# endregion


# region ADMIN ROUTE
@admin_bp.route("/", methods=["GET"])
@admin_required
def get_all_users():
    return get_users_controller()


# endregion
