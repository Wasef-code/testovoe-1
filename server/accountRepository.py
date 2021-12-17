from datetime import datetime

from sqlalchemy.orm.session import Session
from currencyRepository import CurrencyRepository
from models import AccountDB
from transactionRepository import TransactionRepository
from state import generate_id
class AccountRepository:
    __accounts: dict[str, AccountDB] = {}
    def __init__(self, session: Session):
        self.session = session
    def CreateAccount(self, user_id: str, currency_tag: str) -> int:
        i = generate_id()
        while i in self.__accounts.keys():
            i = generate_id()
        self.__accounts[i] = AccountDB(id=i, amount=0.0, user_id=user_id, currency_tag=currency_tag)
        self.session.add(self.__accounts[i])
        self.session.commit()
        return i
    def GetAccount(self, account_id: str) -> AccountDB:
        try:
            return self.__accounts[account_id]
        except KeyError:
            return AccountDB()
    def GetUserAccounts(self, user_id: str) -> list[AccountDB]:
        l: list[AccountDB] = []
        for i in self.__accounts:
            if self.__accounts[i].user_id == user_id:
                l.append(self.__accounts[i])
        return l
    def DeleteAccount(self, account_id: str):
        try:
            del self.__accounts[account_id]
            self.session.delete(self.__accounts[account_id])
            self.session.commit()
        except:
            return
    def Transfer(self, first_id: str, second_id: str, amount: float, cur_repo: CurrencyRepository, trans_repo: TransactionRepository) -> bool:
        charge = False
        try:
            if first_id == "-1":
                second = self.__accounts[second_id]
                second.amount += amount
                trans_repo.CreateTransaction(amount, datetime.now(), second.currency_tag, account_to_id=second_id)
                return True
            elif second_id == "-1":
                first = self.__accounts[first_id]
                if first.amount <= amount:
                    return False
                first.amount -= amount
                trans_repo.CreateTransaction(amount, datetime.now(), first.currency_tag, account_from_id=first_id)
                return True
            first, second = self.__accounts[first_id], self.__accounts[second_id]
            if first.amount <= amount:
                print("NOT ENOUGH")
                return False
            first.amount -= amount
            charge = True
            second.amount += cur_repo.Convert(first.currency_tag, second.currency_tag, amount)
            trans_repo.CreateTransaction(amount, datetime.now(), first.currency_tag, first_id, second_id)
            return True
        except KeyError:
            print("KEY ERROR")
            print(self.__accounts)
            if charge:
                first.amount += amount
            return False
    def Upload(self):
        for i in self.session.query(AccountDB).all():
            self.__accounts[i.id] = i
            self.session.add(i)