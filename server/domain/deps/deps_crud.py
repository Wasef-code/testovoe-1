from domain.services.crud_account import CrudAccount
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
