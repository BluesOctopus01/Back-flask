from app.services.user_service import fetch_all_users, create_user, authenticate_user
from app.DTO.user_dto import UserCreateDTO
from flask import jsonify, request
from app.models import db
from app.utils.jwt_utils import generate_token


# region GET
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

    db.session.add(new_user)
    db.session.commit()
    response_data = new_user.to_dict()
    return jsonify(response_data), 201


def login_user_controller(data):
    """EndPoint : POST /users/login/"""
    if not data.get("password") or not data.get("email"):
        return jsonify({"error": "Email and password are needed"}), 400

    user = authenticate_user(data["email"], data["password"])

    if not user:
        return jsonify({"error": "Invalid credentials"}), 404

    if not user.is_active:
        return (
            jsonify({"message": "Your account is deactivated. Please reactivate it"}),
            403,
        )
        # TODO gérer la logique niveau front et crée une route réactivé niveau back
    response_data = user.to_dict()
    token = generate_token(user.id, user.role)
    response_data["token"] = token
    return jsonify(response_data), 200


# endregion
