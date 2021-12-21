from sqlalchemy.orm.session import Session
from models.models import CurrencyDB


class CurrencyRepository:
    __currencies: dict[str, CurrencyDB] = {}

    def __init__(self, session: Session):
        self.session = session

    def create_currency(self, currency_tag: str, name: str, cost: float):
        c = CurrencyDB(tag=currency_tag, name=name, cost=cost)
        self.__currencies[currency_tag] = c

    def get_currency(self, currency_tag: str) -> CurrencyDB:
        try:
            return self.__currencies[currency_tag]
        except KeyError:
            return CurrencyDB()

    def get_currencies(self):
        return self.__currencies

    def convert(self, first_tag: str, second_tag: str, amount: float):
        return self.__currencies[second_tag].cost * amount / self.__currencies[first_tag].cost

    def update_currency(self, currency_tag: str, amount: float):
        self.__currencies[currency_tag].cost = amount

    def delete_currency(self, currency_tag: str):
        try:
            self.session.delete(self.__currencies[currency_tag])
            del self.__currencies[currency_tag]
        except KeyError:
            return

    def upload(self):
        for i in self.session.query(CurrencyDB).all():
            self.__currencies[i.tag] = i
            self.session.add(i)
