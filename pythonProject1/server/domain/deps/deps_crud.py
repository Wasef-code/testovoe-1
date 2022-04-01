from domain.services.crud_account import CrudAccount
from domain.services.crud_currency import CrudCurrency
from domain.services.crud_transaction import CrudTransaction
from domain.services.crud_user import CrudUser
cache: dict[type, object] = {}


def get_crud_user() -> CrudUser:
    crud_user = cache.get(CrudUser)
    if crud_user is None:
        crud_user = CrudUser()
        cache[CrudUser] = crud_user
    return crud_user


def get_crud_account() -> CrudAccount:
    crud_account = cache.get(CrudAccount)
    if crud_account is None:
        crud_account = CrudAccount()
        cache[CrudAccount] = crud_account
    return crud_account


def get_crud_currency() -> CrudCurrency:
    crud_currency = cache.get(CrudCurrency)
    if crud_currency is None:
        crud_currency = CrudCurrency()
        cache[CrudCurrency] = crud_currency
    return crud_currency


def get_crud_transaction() -> CrudTransaction:
    crud_transaction = cache.get(CrudTransaction)
    if crud_transaction is None:
        crud_transaction = CrudTransaction()
        cache[CrudTransaction] = crud_transaction
    return crud_transaction
