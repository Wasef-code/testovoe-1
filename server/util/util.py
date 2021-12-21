from typing import Any
import jwt
from models.models import UserDB
from deps.deps import get_secret_key
from datetime import datetime, timedelta
from repos.userRepository import UserRepository


def create_jwt(user: UserDB) -> str:
    return jwt.encode({
        "uuid": user.uuid,
        "email": user.email.__str__(),
        "phone_number": user.phone_number,
        "password": user.password,
        "exp": datetime.now() + timedelta(days=1)
    }, get_secret_key(), "HS256")


def verify_jwt(token: str, user_repo: UserRepository, user_to: UserDB = None) -> bool:
    try:
        x: dict[str, Any] = jwt.decode(token, get_secret_key(), \
            algorithms=["HS256"])
        user = user_repo.get_user(x["uuid"])
        if user is None:
            return False
        if not (user.email == x["email"] and user.phone_number == x["phone_number"]):
            return False
        if not user.password == x["password"]:
            return False
        if user_to is not None:
            user_to.uuid = user.uuid
            user_to.email = user.email
            user_to.phone_number = user.phone_number
            user_to.is_admin = user.is_admin
            user_to.password = user.password
            user_to.name = user.name
            user_to.last_name = user.last_name
            user_to.surname = user.surname
        print(f"Got an user {user.uuid}")
        return True
    except jwt.ExpiredSignatureError:
        return False


def refresh_jwt(original_token: str, user_repo: UserRepository) -> str:
    u = UserDB()
    if not verify_jwt(original_token, user_repo, user_to=u):
        return ""
    return create_jwt(user_repo.get_user(u.uuid))