from domain.entities.entities import Account, Transaction
from domain.repos.base_repository import BaseRepository
from domain.util.Conditioner import Conditioner


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    def get_by_account_id(self, account: Account) -> list[Transaction]:
        transactions_list = []
        for i in self.__internal:
            obj = self.__internal[i]
            if Conditioner.AnyEqual(obj.account_from_id, obj.account_to_id,
                                    account.uuid):
                transactions_list.append(obj)
        return transactions_list
