from sqlalchemy.orm.session import Session
from models.models import UserDB
from globals.state import generate_id


class UserRepository:
    __users: dict[str, UserDB] = {}
    __temp: dict[str, UserDB] = {}

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserDB) -> str:
        key = generate_id()
        while key in self.__users.keys():
            key = generate_id()
        user.uuid = key
        self.__temp[key] = user
        return key

    def final_add(self, key: str):
        try:
            self.__users[key] = self.__temp[key]
            self.__temp.pop(key)
            self.session.add(self.__users[key])
            self.session.commit()
        except KeyError:
            return

    def get_user(self, uuid: str) -> UserDB:
        try:
            return self.__users[uuid]
        except KeyError:
            return UserDB()

    def get_user_by_email(self, email: str) -> UserDB:
        for i in self.__users:
            if self.__users[i].email == email:
                return self.__users[i]
        return UserDB()

    def get_user_by_phone(self, phone: str) -> UserDB:
        for i in self.__users:
            if self.__users[i].phone_number == phone:
                return self.__users[i]
        return UserDB()

    def check_email_is_busy(self, email: str) -> bool:
        e = self.get_user_by_email(email)
        return not (e.uuid == "" or e.uuid is None)

    def check_phone_is_busy(self, phone_number: str) -> bool:
        e = self.get_user_by_phone(phone_number)
        return not (e.uuid == "" or e.uuid is None)

    def upload(self):
        for i in self.session.query(UserDB).all():
            self.__users[i.uuid] = i
            self.session.add(i)
