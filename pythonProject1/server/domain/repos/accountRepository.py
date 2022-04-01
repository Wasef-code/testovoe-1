from domain.repos.base_repository import BaseRepository
from domain.entities.entities import Account


class AccountRepository(BaseRepository[Account]):
    def __init__(self):
        super().__init__(Account)
