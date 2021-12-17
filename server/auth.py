from fastapi import APIRouter
from models import LoginUser, ResetUser, RestoreUser, User, UserDB
from hashlib import sha256
from util import CreateJWT, VerifyJWT
from fastapi import Body
from repos import user_repo as user_repository, mail
from db_interface import SESSION
auth_router = APIRouter()
special_symbols = "!./|\\$#@%_+=*"
temp: dict[str, int] = {}
def PhoneValidator(stroka: str) -> bool:
    x = len(stroka)
    return (8 <= x <= 18 and stroka[0] == "+")
def PasswordValidator(stroka: str) -> bool:
    counters = {"digits": 0, "lower_case": 0, "upper_case": 0, "specials": 0}
    for i in stroka:
        if i.isnumeric():
            counters["digits"] += 1
        elif i.isupper():
            counters["upper_case"] += 1
        elif i.islower():
            counters["lower_case"] += 1
        elif i in special_symbols:
            counters["specials"] += 1
    x = len(stroka)
    return (8 <= x < 32 and len(tuple(filter(lambda x: counters[x] > 1, counters))) == len(counters))
@auth_router.post("/register")
def Register(register_user: User):
    if not PhoneValidator(register_user.phone_number):
        return {"Message": "Invalid phone number"}
    if not PasswordValidator(register_user.password):
        return {"Message": "Password doesn't match requirements"}
    if user_repository.CheckEmailIsBusy(register_user.email) or user_repository.CheckPhoneIsBusy(register_user.phone_number):
        return {"Message": "User with this email/phone exists!"}
    uzver = UserDB(uuid="", email=register_user.email, phone_number=register_user.phone_number, \
        password="", name=register_user.name, last_name=register_user.last_name, surname=register_user.surname)
    uzver.password = sha256(register_user.password.encode('utf-8')).hexdigest()
    key = user_repository.CreateUser(uzver)
    temp[key] = mail.SendCode(uzver.email)
    return {"Message": "Verify your email!", "Identifier": key}
@auth_router.post("/verify")
def Verify(code: int = Body(...), identifier: str = Body(...)):
    if temp[identifier] != code:
        return {"Message": "Wrong code!"}
    temp.pop(identifier)
    user_repository.FinalAdd(identifier)
    return {"Message": "Verified successfully!"}
@auth_router.post("/login")
def Login(login_user: LoginUser):
    if login_user.phone_number is None and login_user.email is None:
        return {"Message": "No identifiers present"}
    is_phone = login_user.email == ""
    user = user_repository.GetUserByPhone(login_user.phone_number) if is_phone else user_repository.GetUserByEmail(login_user.email)
    if user.uuid == "":
        return {"Message": "No user with that email/phone!"}
    if sha256(login_user.password.encode('utf-8')).hexdigest() == user.password:
            return {"Message": "Success", "Token": CreateJWT(user)}
    return {"Message": "Incorrect email/phone/password!"}
@auth_router.post("/reset")
def Reset(reset_user: ResetUser):
    u = UserDB()
    if not VerifyJWT(reset_user.token, user_repository, u):
        return {"Message": "Invalid JWT token!"}
    u = user_repository.GetUser(u.uuid)
    if reset_user.phone_number is None and reset_user.email is None and \
        (reset_user.name is None and reset_user.last_name is None and \
            reset_user.surname is None):
                return {"Message": "No data provided!"}
    if not (reset_user.phone_number is None or reset_user.phone_number == []) and reset_user.phone_number[0] == u.phone_number:
        u.phone_number = reset_user.phone_number[1]
    if not (reset_user.email is None or reset_user.email == []) and reset_user.email[0] == u.email:
        u.email = reset_user.email[1]
    if not (reset_user.password is None or reset_user.password == []) and sha256(reset_user.password[0].encode('utf-8')).hexdigest() \
            == u.password:
        u.password = sha256(reset_user.password[1].encode('utf-8')).hexdigest()
    if not (reset_user.name is None and reset_user.last_name is None and reset_user.surname is None):
        u.name = reset_user.name
        u.last_name = reset_user.last_name
        u.surname = reset_user.surname
    SESSION.commit()
    return {"Message": "Data has been updated successfully!"}
@auth_router.post("/restore")
def Restore(restore_user: RestoreUser):
    u = user_repository.GetUserByEmail(restore_user.email[0])
    if u is None:
        return {"Message": "Invalid data!"}
    if u.password != sha256(restore_user.password[0].encode('utf-8')).hexdigest():
        return {"Message": "Incorrect password!"}
    if len(restore_user.password) > 1:
        u.password = sha256(restore_user.password[1].encode('utf-8')).hexdigest()
    if len(restore_user.email) > 1:
        u.email = restore_user.email[1]
    SESSION.commit()
    return {"Message": "Data updated successfully!"}