from sqlalchemy.orm.session import Session
from models import TransactionDB
from datetime import datetime
from state import generate_id
class TransactionRepository:
    __transactions: dict[int, TransactionDB] = {}
    def __init__(self, session: Session):
        self.session = session
    def CreateTransaction(self, amount: float, created_at: datetime, currency_tag: str, account_from_id: str = "-1", account_to_id: str = "-1"):
        i = generate_id()
        while i in self.__transactions.keys():
            i = generate_id()
        self.__transactions[i] = TransactionDB(id=i, amount=amount, created_at=created_at, currency_tag=currency_tag, account_from_id=account_from_id,\
            account_to_id=account_to_id)
        self.session.add(self.__transactions[i])
        self.session.commit()
    def GetTransaction(self, tr_id: str) -> TransactionDB:
        try:
            return self.__transactions[tr_id]
        except KeyError:
            return TransactionDB()
    def GetAccountTransactions(self, account_id: str) -> list[TransactionDB]:
        l: list[TransactionDB] = []
        for i in self.__transactions:
            if self.__transactions[i].account_from_id == account_id or self.__transactions[i].account_to_id == account_id:
                l.append(self.__transactions[i])
        return l
    def DeleteTransaction(self, transaction_id: str):
        try:
            del self.__transactions[transaction_id]
            self.session.delete(self.__transactions[transaction_id])
            self.session.commit()
        except:
            return
    def Upload(self):
        for i in self.session.query(TransactionDB).all():
            self.__transactions[i.id] = i
            self.session.add(i)