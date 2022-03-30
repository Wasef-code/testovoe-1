from domain.entities.entities import Currency
from .base_repository import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    def __init__(self):
        super().__init__(Currency)


# TODO: TRANSFER CURRENCY CONVERT LOGIC INTO CRUD LAYER
