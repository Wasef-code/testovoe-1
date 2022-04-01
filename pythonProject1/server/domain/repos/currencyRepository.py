from domain.entities.entities import Currency
from .base_repository import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    def __init__(self):
        super().__init__(Currency)

    def convert(self, first: Currency, second: Currency,
                amount: float) -> float:
        return (first.cost * amount / second.cost)

    def get_by_tag(self, tag: str):
        for i in self.__internal:
            if self.__internal[i].tag == tag:
                return self.__internal[i]
        return None
