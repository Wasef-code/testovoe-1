from uuid import UUID
from domain.entities.entities import Account, Transaction
from domain.services.crud_base import CrudBase
from domain.repos.accountRepository import AccountRepository
from domain.deps.deps_repo import get_account_repo, get_currency_repo,\
    get_transaction_repo
from datetime import datetime


class CrudAccount(CrudBase[Account, AccountRepository]):
    temp: dict[str, int] = {}

    def __init__(self):
        super().__init__(Account, AccountRepository, get_account_repo)

    def read_by_user_id(self, user_id: UUID) -> list[Account]:
        result = []
        for i in self.repo_object.get_all():
            if i.user_id == user_id:
                result.append(i)
        return result

    def transfer(self, first_id: UUID, second_id: UUID, amount: float) -> bool:
        charge = False
        try:
            trans_repo = get_transaction_repo()
            acc_repo = get_account_repo()
            cur_repo = get_currency_repo()
            if first_id == "-1":
                second = acc_repo.get(second_id)
                second.amount += amount
                transaction = Transaction("", amount, second.currency_tag,
                                          -1, second_id, datetime.now())
                trans_repo.add(transaction)
                return True
            elif second_id == "-1":
                first = acc_repo.get(first_id)
                if first.amount <= amount:
                    return False
                first.amount -= amount
                transaction = Transaction("", amount, first.currency_tag,
                                          first_id, -1, datetime.now())
                trans_repo.add(transaction)
                return True
            first, second = acc_repo.get(first_id), acc_repo.get(second_id)
            if first.amount <= amount:
                return False
            first.amount -= amount
            charge = True
            second.amount += cur_repo.convert(cur_repo.get(first.currency_tag),
                                              cur_repo.get(second.
                                                           currency_tag),
                                              amount)
            trans_repo.add(Transaction(amount, first.currency_tag, first_id,
                                       second_id, datetime.now()))
            return True
        except AttributeError:
            if charge:
                first.amount += amount
            return False
