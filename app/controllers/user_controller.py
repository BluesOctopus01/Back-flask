from app.services.user_service import fetch_all_users
from app.utils.jwt_utils import admin_required, jwt_required
from flask import jsonify, request


def get_users_controller():
    """EndPoint : GET /users/admin"""
    try:
        users = fetch_all_users()
        users_dict = [user.to_dict() for user in users]
        return jsonify(users_dict), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500
