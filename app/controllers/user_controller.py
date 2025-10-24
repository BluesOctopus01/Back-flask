from app.services.user_service import fetch_all_users, create_user
from app.utils.jwt_utils import admin_required, jwt_required
from app.DTO.user_dto import UserCreateDTO
from flask import jsonify, request
from app.models import db
from app.utils.jwt_utils import generate_token


# def get_users_controller():
#     """EndPoint : GET /users/admin"""
#     try:
#         users = fetch_all_users()
#         users_dict = [user.to_dict() for user in users]
#         return jsonify(users_dict), 200
#     except Exception as e:
#         return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500


# region POST


def post_user_controller(data):
    """EndPoint : POST /users"""
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

    token = generate_token(new_user.id, new_user.role)

    response_data = new_user.to_dict()
    response_data["token"] = token
    return jsonify(response_data), 201


# endregion
