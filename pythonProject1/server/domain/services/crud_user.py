from domain.entities.entities import User
from domain.services.crud_base import CrudBase
from domain.repos.userRepository import UserRepository
from domain.deps.deps_repo import get_user_repo


class CrudUser(CrudBase[User, UserRepository]):
    temp: dict[str, int] = {}

    def __init__(self):
        super().__init__(User, UserRepository, get_user_repo)
