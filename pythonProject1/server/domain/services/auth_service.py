from domain.entities.entities import User
from domain.deps.deps_interfaces import get_db, get_mail
from domain.deps.deps_repo import get_user_repo
from domain.schemas.schemas import LoginUserModel, ResetUserModel,\
    RestoreUserModel, UserModel
from domain.util.Conditioner import Conditioner
from domain.util.util import phone_validator, password_validator, refresh_jwt
from hashlib import sha256
from domain.util.util import create_jwt, verify_jwt


class AuthService:
    temp: dict[str, int] = {}

    def __init__(self):
        self.repo_object = get_user_repo()

    def create(self, model: UserModel):
        user_repository = self.repo_object
        if not phone_validator(model.phone_number):
            return {"Message": "Invalid phone number"}
        if not password_validator(model.password):
            return {"Message": "Password doesn't match requirements"}
        if Conditioner.Any(user_repository.check_email_is_busy(model.email),
                           user_repository.
                           check_phone_is_busy(model.phone_number)):
            return {"Message": "User with this email/phone exists!"}
        uzver = User(uuid=None, email=model.email,
                     phone_number=model.phone_number,
                     password="", name=model.name,
                     last_name=model.last_name,
                     surname=model.surname,
                     activated=False)
        uzver.password = sha256(model.password.encode('utf-8')).hexdigest()
        key = user_repository.add(uzver)
        self.temp[key] = get_mail().send_code(uzver.email)
        return {"Message": "Verify your email!", "Identifier": key}

    def confirm(self, identifier: str, code: int):
        pending_code = self.temp.get(identifier)
        if pending_code is None or pending_code != code:
            return {"Message": "Wrong code!"}
        user_object = self.repo_object.update(self.repo_object.get(identifier),
                                              {"activated": True})
        with get_db().create_session() as session, session.begin():
            session.add(user_object)
        self.temp.pop(identifier)
        return {"Message": "Verified successfully!"}

    def login(self, login_user: LoginUserModel):
        if Conditioner.AllEqual(None, login_user.phone_number,
                                login_user.email):
            return {"Message": "No identifiers present"}
        is_phone = login_user.email == ""
        user = self.repo_object.get_user_by_phone(login_user.phone_number) if \
            is_phone else self.repo_object.get_user_by_email(login_user.email)
        if user is None:
            return {"Message": "No user with that email/phone!"}
        if sha256(login_user.password.encode('utf-8')).hexdigest() ==\
                user.password:
            return {"Message": "Success", "Token": create_jwt(user),
                    "UUID": str(user.uuid)}
        return {"Message": "Incorrect email/phone/password!"}

    def reset(self, reset_user: ResetUserModel):
        u = User()
        user_repository = self.repo_object
        if not verify_jwt(reset_user.token, user_repository, u):
            return {"Message": "Invalid JWT token!"}
        u = user_repository.get(u.uuid)
        if Conditioner.AllEqual(None, reset_user.email, reset_user.
                                phone_number) and\
           Conditioner.AllEqual(None, reset_user.name, reset_user.last_name,
                                reset_user.surname):
            return {"Message": "No data provided!"}
        if not Conditioner.AllEqual(reset_user.phone_number, None, []) \
                and reset_user.phone_number[0] == u.phone_number:
            u.phone_number = reset_user.phone_number[1]
        if not Conditioner.AllEqual(reset_user.email, None, []) and\
                reset_user.email[0] == u.email:
            u.email = reset_user.email[1]
        if not Conditioner.AllEqual(reset_user.password, None, []) and \
            sha256(reset_user.password[0].encode('utf-8')).hexdigest() \
                == u.password:
            u.password = sha256(reset_user.password[1].encode('utf-8')).\
                                hexdigest()
        if not Conditioner.AllEqual(None, reset_user.name,
                                    reset_user.last_name, reset_user.surname):
            u.name = reset_user.name
            u.last_name = reset_user.last_name
            u.surname = reset_user.surname
        return {"Message": "Data has been updated successfully!"}

    def restore(self, restore_user: RestoreUserModel):
        u = self.repo_object.get_user_by_email(restore_user.email[0])
        if u is None:
            return {"Message": "Invalid data!"}
        if u.password != sha256(restore_user.password[0].
                                encode('utf-8')).hexdigest():
            return {"Message": "Incorrect password!"}
        if len(restore_user.password) > 1:
            u.password = sha256(restore_user.password[1]
                                .encode('utf-8')).hexdigest()
        if len(restore_user.email) > 1:
            u.email = restore_user.email[1]
        return {"Message": "Data updated successfully!"}

    def refresh_token(self, token: str):
        token = refresh_jwt(token, self.repo_object)
        if token == "":
            return {"Message": "Incorrect token!"}
        return {"Token": token}
