from uuid import UUID
from domain.entities.entities import Transaction
from domain.services.crud_base import CrudBase
from domain.repos.transactionRepository import TransactionRepository
from domain.deps.deps_repo import get_account_repo, get_transaction_repo


class CrudTransaction(CrudBase[Transaction, TransactionRepository]):
    def __init__(self):
        super().__init__(Transaction, TransactionRepository,
                         get_transaction_repo)

    def get_by_account_id(self, acc_id: UUID):
        account = get_account_repo().get(acc_id)
        return self.repo_object.get_by_account(account)
