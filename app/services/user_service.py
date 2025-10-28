from datetime import datetime, timezone
from app.models.user_models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db


# region GET
def fetch_a_user(id: int) -> User:
    """Return a single user with his id with only his public informations"""
    user = User.query.filter_by(id=id).first()
    if not user:
        return None
    return user


def fetch_all_users() -> list[User]:
    """Return a list of all users"""
    # todo rajouter une pagination
    return User.query.all()


# endregion


# region POST
def create_user(
    username: str,
    first_name: str,
    last_name: str,
    password: str,
    email: str,
    gender: str,
    phone_number: str,
    birth_date: str,
    country: str,
    address: str,
    user_bio: str,
    image: str,
) -> User:
    """Return a created user"""
    hashed_password = generate_password_hash(password)

    is_first_user = User.query.count() == 0
    role = "admin" if is_first_user else "user"
    new_user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
        email=email,
        gender=gender,
        phone_number=phone_number,
        birth_date=birth_date,
        country=country,
        address=address,
        user_bio=user_bio,
        image=image,
        role=role,
    )
    return new_user


def authenticate_user(email: str, password: str) -> User | None:
    """Return an existing user or None if not found"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return None

    if check_password_hash(user.password, password):
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()
        return user

    return None


# todo premier user = admin / changer mot de passe premiere co si c'est le cas
# endregion


# region PATCH
# endregion


# region DELETE
# endregion
