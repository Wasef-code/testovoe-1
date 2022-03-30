from domain.entities.entities import Account
from domain.services.crud_base import CrudBase
from domain.repos.accountRepository import AccountRepository
from domain.deps.deps_repo import get_account_repo


class CrudAccount(CrudBase[Account, AccountRepository, get_account_repo]):
    temp: dict[str, int] = {}

    def __init__(self):
        super().__init__(Account, AccountRepository, get_account_repo)

    def read_by_user_id(self, user_id: str) -> list[Account]:
        result = []
        for i in self.repo_object.get_all():
            if i.user_id == user_id:
                result.append(i)
        return result
