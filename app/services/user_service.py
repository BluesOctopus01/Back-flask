from app.models.user_models.user import User


# region GET


def fetch_all_users() -> list[User]:
    """Return a list of all users"""
    # todo rajouter une pagination
    return User.query.all()


# endregion


# region POST
# end region


# region PATCH
# endregion


# region DELETE
# endregion
