from werkzeug.security import safe_str_cmp
from models.user import UserModel
from typing import Union


def authenicate(username: str, password: str) -> Union[UserModel, None]:
    """
    Function is called when user calls /auth endpoint
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(password, user.password):
        return user


def identity(payload):
    """
    Called when user is authenticated already.
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


