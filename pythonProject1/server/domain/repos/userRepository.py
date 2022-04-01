from domain.entities.entities import User
from domain.repos.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str) -> User | None:
        internal = self.get_internal()
        for i in internal:
            if internal[i].email == email:
                return internal[i]
        return None

    def get_user_by_phone(self, phone: str) -> User | None:
        internal = self.get_internal()
        for i in internal:
            if internal[i].phone_number == phone:
                return internal[i]
        return None

    def check_email_is_busy(self, email: str) -> bool:
        e = self.get_user_by_email(email)
        return e is not None

    def check_phone_is_busy(self, phone_number: str) -> bool:
        e = self.get_user_by_phone(phone_number)
        return e is not None


# TODO: TRANSFER CONFIRMATION AND USER-CREATION LOGIC INTO USER CRUD!
