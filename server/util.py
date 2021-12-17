import jwt
from models import UserDB
from state import SECRET_KEY
from datetime import datetime, timedelta
from typing import Any
from userRepository import UserRepository
def CreateJWT(user: UserDB) -> str:
    return jwt.encode({
        "uuid": user.uuid,
        "email": user.email.__str__(),
        "phone_number": user.phone_number,
        "password": user.password,
        "exp": datetime.now() + timedelta(days=1)
    }, SECRET_KEY, "HS256")
def VerifyJWT(token: str, user_repo: UserRepository, user_to: UserDB=None) -> bool:
    try:
        x: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = user_repo.GetUser(x["uuid"])
        if user is None:
            return False
        if not (user.email == x["email"] and user.phone_number == x["phone_number"]):
            return False
        if not user.password == x["password"]:
            return False
        if not user_to is None:
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
def RefreshJWT(original_token: str, user_repo: UserRepository, uuid: str) -> str:
    if not VerifyJWT(original_token, user_repo):
        return ""
    return CreateJWT(user_repo.GetUser(uuid))
def GetUserFromJWT(token: str, user_repo: UserRepository) -> UserDB:
    user = UserDB()
    if not VerifyJWT(token, user_repo, user_to=user):
        return None
    return user
def UpdateCurrencyRates():
    pass # TODO: Implement currency rate update