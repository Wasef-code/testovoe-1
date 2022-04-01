from domain.deps.deps_repo import get_currency_repo
from domain.entities.entities import Currency
from domain.services.crud_base import CrudBase
from domain.repos.currencyRepository import CurrencyRepository


class CrudCurrency(CrudBase[Currency, CurrencyRepository]):
    def __init__(self):
        super().__init__(Currency, CurrencyRepository, get_currency_repo)
