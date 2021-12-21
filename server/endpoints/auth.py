from fastapi import APIRouter
from models.models import UserDB
from schemas.schemas import LoginUser, ResetUser, RestoreUser, User
from hashlib import sha256
from util.util import create_jwt, verify_jwt, refresh_jwt
from fastapi import Body
from deps.deps import get_db, get_mail
from deps.deps_repo import get_user_repo
auth_router = APIRouter()
SPECIAL_SYMBOLS = "!./|\\$#@%_+=*"
temp: dict[str, int] = {}
mail = get_mail()
SESSION = get_db().get_session()


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
            counters))) == len(counters))


@auth_router.post("/register")
def register(register_user: User):
    user_repository = get_user_repo()
    if not phone_validator(register_user.phone_number):
        return {"Message": "Invalid phone number"}
    if not password_validator(register_user.password):
        return {"Message": "Password doesn't match requirements"}
    if user_repository.check_email_is_busy(register_user.email) or \
            user_repository.check_phone_is_busy(register_user.phone_number):
        return {"Message": "User with this email/phone exists!"}
    uzver = UserDB(uuid="", email=register_user.email, phone_number=register_user.phone_number,
                password="", name=register_user.name, last_name=register_user.last_name, surname=register_user.surname)
    uzver.password = sha256(register_user.password.encode('utf-8')).hexdigest()
    key = user_repository.create_user(uzver)
    temp[key] = mail.send_code(uzver.email)
    return {"Message": "Verify your email!", "Identifier": key}


@auth_router.post("/verify")
def verify(code: int = Body(...), identifier: str = Body(...)):
    if temp[identifier] != code:
        return {"Message": "Wrong code!"}
    temp.pop(identifier)
    get_user_repo().final_add(identifier)
    return {"Message": "Verified successfully!"}


@auth_router.post("/login")
def login(login_user: LoginUser):
    if login_user.phone_number is None and login_user.email is None:
        return {"Message": "No identifiers present"}
    is_phone = login_user.email == ""
    user = get_user_repo().get_user_by_phone(login_user.phone_number) if is_phone \
        else get_user_repo().get_user_by_email(login_user.email)
    if user.uuid == "":
        return {"Message": "No user with that email/phone!"}
    if sha256(login_user.password.encode('utf-8')).hexdigest() == user.password:
        return {"Message": "Success", "Token": create_jwt(user)}
    return {"Message": "Incorrect email/phone/password!"}


@auth_router.post("/reset")
def reset(reset_user: ResetUser):
    u = UserDB()
    user_repository = get_user_repo()
    if not verify_jwt(reset_user.token, user_repository, u):
        return {"Message": "Invalid JWT token!"}
    u = user_repository.get_user(u.uuid)
    if reset_user.phone_number is None and reset_user.email is None and \
        (reset_user.name is None and reset_user.last_name is None and
            reset_user.surname is None):
        return {"Message": "No data provided!"}
    if not (reset_user.phone_number is None or reset_user.phone_number == []) \
        and reset_user.phone_number[0] == u.phone_number:
        u.phone_number = reset_user.phone_number[1]
    if not (reset_user.email is None or reset_user.email == []) and reset_user.email[0] == u.email:
        u.email = reset_user.email[1]
    if not (reset_user.password is None or reset_user.password == []) and \
        sha256(reset_user.password[0].encode('utf-8')).hexdigest() \
            == u.password:
        u.password = sha256(reset_user.password[1].encode('utf-8')).hexdigest()
    if not (reset_user.name is None and reset_user.last_name is None and reset_user.surname is None):
        u.name = reset_user.name
        u.last_name = reset_user.last_name
        u.surname = reset_user.surname
    get_db().get_session().commit()
    return {"Message": "Data has been updated successfully!"}


@auth_router.post("/restore")
def restore(restore_user: RestoreUser):
    u = get_user_repo().get_user_by_email(restore_user.email[0])
    if u is None:
        return {"Message": "Invalid data!"}
    if u.password != sha256(restore_user.password[0].encode('utf-8')).hexdigest():
        return {"Message": "Incorrect password!"}
    if len(restore_user.password) > 1:
        u.password = sha256(restore_user.password[1].encode('utf-8')).hexdigest()
    if len(restore_user.email) > 1:
        u.email = restore_user.email[1]
    get_db().get_session().commit()
    return {"Message": "Data updated successfully!"}


@auth_router.post("/refresh")
def refresh(token: str):
    return refresh_jwt(token, get_user_repo())