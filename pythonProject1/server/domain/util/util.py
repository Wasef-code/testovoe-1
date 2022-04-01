from typing import Any
from uuid import UUID
import jwt
from domain.deps.deps_repo import get_user_repo
from domain.entities.entities import User
from domain.deps.deps_interfaces import get_secret_key
from datetime import datetime, timedelta

SPECIAL_SYMBOLS = "!./|\\$#@%_+=*"


def phone_validator(stroka: str) -> bool:
    x = len(stroka)
    return (8 <= x <= 18 and stroka[0] == "+")


def password_validator(stroka: str) -> bool:
    counters = {"digits": 0, "lower_case": 0, "upper_case": 0, "specials": 0}
    for i in stroka:
        if i.isnumeric():
            counters["digits"] += 1
        elif i.isupper():
            counters["upper_case"] += 1
        elif i.islower():
            counters["lower_case"] += 1
        elif i in SPECIAL_SYMBOLS:
            counters["specials"] += 1
    x = len(stroka)
    return (8 <= x < 32 and len(tuple(filter(lambda x: counters[x] > 1,
            counters))) == len(counters.values()))


def create_jwt(user: User) -> str:
    return jwt.encode({
        "uuid": str(user.uuid),
        "email": user.email.__str__(),
        "phone_number": user.phone_number,
        "password": user.password,
        "exp": datetime.now() + timedelta(days=1)
    }, get_secret_key(), "HS256")


def verify_jwt(token: str, user_to: User = None) -> bool:
    try:
        x: dict[str, Any] = jwt.decode(token, get_secret_key(),
                                       algorithms=["HS256"])
        user: User = get_user_repo().get(x["uuid"])
        if user is None:
            print("DEBUG: NONE USER")
            return False
        if not (user.email == x["email"] and user.phone_number ==
                x["phone_number"]):
            print("DEBUG: INCORRECT DATA")
            return False
        if not user.password == x["password"]:
            print("DEBUG: INCORRECT PASSWORD")
            return False
        if user_to is not None:
            user_to.uuid = UUID(user.uuid)
            user_to.email = user.email
            user_to.phone_number = user.phone_number
            user_to.admin = user.admin
            user_to.password = user.password
            user_to.name = user.name
            user_to.last_name = user.last_name
            user_to.surname = user.surname
            user_to.activated = user.activated
        return True
    except jwt.ExpiredSignatureError:
        print("DEBUG: EXPIRED TOKEN")
        return False


def refresh_jwt(original_token: str) -> str:
    u = User()
    if not verify_jwt(original_token, user_to=u):
        return ""
    return create_jwt(get_user_repo().get(u.uuid))
