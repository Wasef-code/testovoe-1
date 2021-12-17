from sqlalchemy.orm.session import Session
from models import UserDB
from state import generate_id
class UserRepository:
    __users: dict[str, UserDB] = {}
    __temp: dict[str, UserDB] = {}
    def __init__(self, session: Session):
        self.session = session
    def CreateUser(self, user: UserDB) -> str:
        key = generate_id()
        while key in self.__users.keys():
            key = generate_id()
        user.uuid = key
        self.__temp[key] = user
        return key
    def FinalAdd(self, key: str):
        try:
            self.__users[key] = self.__temp[key]
            self.__temp.pop(key)
            self.session.add(self.__users[key])
            self.session.commit()
        except KeyError:
            return
    def GetUser(self, uuid: str) -> UserDB:
        try:
            return self.__users[uuid]
        except KeyError:
            return UserDB()
    def GetUserByEmail(self, email: str) -> UserDB:
        for i in self.__users:
            if self.__users[i].email == email:
                return self.__users[i]
        return UserDB()
    def GetUserByPhone(self, phone: str) -> UserDB:
        for i in self.__users:
            if self.__users[i].phone_number == phone:
                return self.__users[i]
        return UserDB()
    def CheckEmailIsBusy(self, email: str) -> bool:
        e = self.GetUserByEmail(email)
        return not (e.uuid == "" or e.uuid is None)
    def CheckPhoneIsBusy(self, phone_number: str) -> bool:
        e = self.GetUserByPhone(phone_number)
        return not (e.uuid == "" or e.uuid is None)
    def CheckPassword(self, password: str) -> bool:
        return False
    def Upload(self):
        for i in self.session.query(UserDB).all():
            self.__users[i.uuid] = i
            self.session.add(i)