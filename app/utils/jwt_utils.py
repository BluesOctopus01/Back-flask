import jwt
import datetime
from flask import current_app
from functools import wraps
from flask import request, jsonify
from app.models import User


# Generer un token JWT


# token :
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 .
# eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0 .
# KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30
def generate_token(user_id, role):
    payload = {
        # Id de l'utilisateur
        "user_id": user_id,
        # role de l'utilisateur
        "role": role,
        # Date d'expiration du token
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=1),
        # heure limite du token : 66432
        # heure actuelle : 55432
        # date d'emission du token
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token


# Decoder un token JWT
def decode_token(token):
    try:
        payload = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        user_id = payload["user_id"]
        role = payload["role"]

        user = User.query.get(user_id)

        if user:
            return user_id, role
        else:
            return None
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# Decorateur Pour  les routes
def jwt_required(f):
    # wraps permet de conserver les informations de la fonction d'origine
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Recuperer le token depuis le headers de la requete
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split(" ")

            # Verification des valeurs du header
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
                print(f"Token found: {token}")

        # Si le token est absent on renvoie une erreur 401 ( unauthorized )
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        # Decoder le token
        decoded = decode_token(token)
        # si le token est invalide ou expiré
        if not decoded:
            return jsonify({"error": "Token is invalid or expired!"}), 401

        user_id, role = decoded
        return f(user_id=user_id, role=role, *args, **kwargs)

    return decorated


# Decorateur Pour  les routes admin
def admin_required(f):
    # wraps permet de conserver les paramètres de la fonction d'origine
    @wraps(f)
    def decoratedRole(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        result = decode_token(token)

        if not result:
            return jsonify({"error": "Token is invalid or expired!"}), 401

        user_id, role = result

        if role != "admin":
            return jsonify({"error": "Admin access required!"}), 403

        return f(*args, **kwargs)

    return decoratedRole
