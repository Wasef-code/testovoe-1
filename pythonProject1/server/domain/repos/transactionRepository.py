from domain.entities.entities import Account, Transaction
from domain.repos.base_repository import BaseRepository
from domain.util.Conditioner import Conditioner


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    def get_by_account(self, account: Account) -> list[Transaction]:
        transactions_list = []
        internal = self.get_internal()
        for i in self:
            obj = internal[i]
            if Conditioner.AnyEqual(obj.account_from_id, obj.account_to_id,
                                    account.uuid):
                transactions_list.append(obj)
        return transactions_list
