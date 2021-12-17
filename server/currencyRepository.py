from sqlalchemy.orm.session import Session
from models import CurrencyDB
class CurrencyRepository:
    __currencies: dict[str, CurrencyDB] = {}
    def __init__(self, session: Session):
        self.session = session
    def CreateCurrency(self, currency_tag: str, name: str, cost: float):
        c = CurrencyDB(tag=currency_tag, name=name, cost=cost)
        self.__currencies[currency_tag] = c
    def GetCurrency(self, currency_tag: str) -> CurrencyDB:
        try:
            return self.__currencies[currency_tag]
        except:
            return CurrencyDB()
    def GetCurrencies(self):
        return self.__currencies
    def Convert(self, first_tag: str, second_tag: str, amount: float):
        return self.__currencies[second_tag].cost * amount / self.__currencies[first_tag].cost
    def UpdateCurrency(self, currency_tag: str, amount: float):
        self.__currencies[currency_tag].cost = amount
    def DeleteCurrency(self, currency_tag: str):
        try:
            self.session.delete(self.__currencies[currency_tag])
            del self.__currencies[currency_tag]
        except:
            return
    def Upload(self):
        for i in self.session.query(CurrencyDB).all():
            self.__currencies[i.tag] = i
            self.session.add(i)