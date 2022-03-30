from domain.repos.base_repository import BaseRepository
from domain.entities.entities import Account


class AccountRepository(BaseRepository[Account]):
    def __init__(self):
        super().__init__(Account)


# DON'T UNCOMMENT IT, MUST BE REWORKED INTO ACCOUNT REPOSITORY!
'''    def transfer(self, first_id: str, second_id: str, amount: float,
                 cur_repo: CurrencyRepository,
                 trans_repo: TransactionRepository) -> bool:
        charge = False
        try:
            if first_id == "-1":
                second = self.__accounts[second_id]
                second.amount += amount
                trans_repo.create_transaction(amount, datetime.now(),
                                              second.currency_tag,
                                              account_to_id=second_id)
                return True
            elif second_id == "-1":
                first = self.__accounts[first_id]
                if first.amount <= amount:
                    return False
                first.amount -= amount
                trans_repo.create_transaction(amount, datetime.now(),
                                              first.currency_tag,
                                              account_from_id=first_id)
                return True
            first, second = self.__accounts[first_id],\
                self.__accounts[second_id]
            if first.amount <= amount:
                print("NOT ENOUGH")
                return False
            first.amount -= amount
            charge = True
            second.amount += cur_repo.convert(first.currency_tag,
                                              second.currency_tag, amount)
            trans_repo.create_transaction(amount, datetime.now(),
                                          first.currency_tag, first_id,
                                          second_id)
            return True
        except KeyError:
            print("KEY ERROR")
            print(self.__accounts)
            if charge:
                first.amount += amount
            return False
'''
