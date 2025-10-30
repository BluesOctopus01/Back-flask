from app.models.user_models.user import User
from app.services.user_service import (
    fetch_all_users,
    create_user,
    authenticate_user,
    fetch_a_user,
    put_user,
    check_password_service,
    patch_password_user,
    deactivate_user,
)
from app.DTO.user_dto import (
    UserCreateDTO,
    UserPatchDTO,
    UserUpdateDTO,
    UserPasswordUpdateDTO,
)
from flask import jsonify, request
from app.models import db
from app.utils.jwt_utils import generate_token


def check_user_active(user: User):
    """Utilitary : Verifiy if the account is active or not"""
    if not user.is_active:
        return jsonify({"message": "This account is inactive"}), 403
    return None


# region GET
def get_user_controller(id: int):
    """EndPoint : GET /users/profiles/<id>"""

    user = fetch_a_user(id)

    if not user:
        return jsonify({"message": "user not found"}), 404

    check_user_active(user)

    user_public = user.to_public_dict()
    return jsonify(user_public), 200


def get_users_controller():
    """EndPoint : GET /users/admin/"""
    try:
        users = fetch_all_users()
        users_dict = [user.to_dict() for user in users]
        return jsonify(users_dict), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500


# endregion
# region POST


def post_user_controller(data):
    """EndPoint : POST /users/"""
    dto, err = UserCreateDTO.from_json(data)
    if err:
        return jsonify(err), 400
    new_user = create_user(
        dto.username,
        dto.first_name,
        dto.last_name,
        dto.password,
        dto.email,
        dto.gender,
        dto.phone_number,
        dto.birthdate,
        dto.country,
        dto.address,
        dto.user_bio,
        dto.image,
    )

    response_data = new_user.to_dict()
    return jsonify(response_data), 201


def login_user_controller(data):
    """EndPoint : POST /users/login/"""
    if not data.get("password") or not data.get("email"):
        return jsonify({"error": "Email and password are needed"}), 400

    user = authenticate_user(data["email"], data["password"])

    if not user:
        return jsonify({"error": "Invalid credentials"}), 404

    check_user_active(user)

    # TODO gérer la logique niveau front et crée une route réactivé niveau back
    response_data = user.to_dict()
    token = generate_token(user.id, user.role)
    response_data["token"] = token
    return jsonify(response_data), 200


# endregion


# region UPDATE
def update_user_controller(user_id, data):
    """EndPoint : PUT /users/update"""
    dto, err = UserUpdateDTO.from_json(data)
    if err:
        return jsonify(err), 400
    updated_user = put_user(
        user_id,
        dto.username,
        dto.first_name,
        dto.last_name,
        dto.email,
        dto.gender,
        dto.phone_number,
        dto.birthdate,
        dto.country,
        dto.address,
        dto.user_bio,
        dto.image,
    )
    if not updated_user:
        return jsonify({"message": "user not found"}), 404

    response_data = updated_user.to_dict()
    return jsonify(response_data), 200


def update_user_psw_controller(user_id, data):
    result = check_password_service(user_id, data["old_password"])
    if not result:
        return jsonify({"message": "invalid credentials"}), 400
    dto, err = UserPasswordUpdateDTO.from_json(data)
    if err:
        return jsonify(err), 400
    updated_user = patch_password_user(user_id, dto.new_password)
    if not updated_user:
        return jsonify({"error": "Error hashing password"}), 400
    response_data = updated_user.to_dict()
    return jsonify(response_data), 200


# endregion


# region DELETE
def soft_delete_user_controller(user_id):
    user = deactivate_user(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404
    response = user.to_dict()
    return jsonify(response), 200


# endregion
