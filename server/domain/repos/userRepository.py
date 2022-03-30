from domain.entities.entities import User
from domain.repos.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str) -> User | None:
        for i in self.__internal:
            if self.__internal[i].email == email:
                return self.__internal[i]
        return None

    def get_user_by_phone(self, phone: str) -> User | None:
        for i in self.__internal:
            if self.__internal[i].phone_number == phone:
                return self.__internal[i]
        return None

    def check_email_is_busy(self, email: str) -> bool:
        e = self.get_user_by_email(email)
        return e is None

    def check_phone_is_busy(self, phone_number: str) -> bool:
        e = self.get_user_by_phone(phone_number)
        return e is None


# TODO: TRANSFER CONFIRMATION AND USER-CREATION LOGIC INTO USER CRUD!
