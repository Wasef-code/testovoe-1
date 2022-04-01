from fastapi import APIRouter, Body
from domain.deps.deps_service import get_bank_service
from domain.entities.entities import User
from domain.schemas.schemas import AccountModel, CurrencyModel,\
    TransactionRequestModel
from domain.deps.deps_repo import get_user_repo
from domain.deps.deps_crud import get_crud_account, get_crud_currency,\
    get_crud_transaction, get_crud_user
from domain.util.util import verify_jwt
bank_router = APIRouter()
bank_service = get_bank_service()
account_crud = get_crud_account()


@bank_router.post("/account/create")
def create_account(acc: AccountModel, token: str = Body(...)):
    return bank_service.create_account(acc, token)


@bank_router.delete("/account/delete/{acc_id}")
def close_account(acc_id: str, token: str = Body(...)):
    return bank_service.close_account(acc_id, token)


@bank_router.post("/account/transfer/")
def transfer(request: TransactionRequestModel):
    return bank_service.transfer(request)


@bank_router.post("/account/{acc_id}")
def get_account(acc_id: str, token: str = Body(...)):
    u = User()
    if not verify_jwt(token, get_user_repo(), u):
        return {"Message": "Incorrect token!"}
    return account_crud.read(acc_id)


@bank_router.post("/account")
def get_user_accounts(user_id: str = Body(...), token: str = Body(...)):
    user = User()
    if not verify_jwt(token, get_user_repo(), user):
        return {"Message": "Incorrect token!"}
    return account_crud.read_by_user_id(user_id)


@bank_router.post("/account/deposit/{acc_id}")
def deposit(acc_id: str, token: str = Body(...), amount: float = Body(...)):
    return bank_service.transfer(TransactionRequestModel(token, "-1",
                                                         acc_id, amount))


@bank_router.post("/account/withdraw/{acc_id}")
def withdraw(acc_id: str, token: str = Body(...), amount: float = Body(...)):
    return bank_service.transfer(TransactionRequestModel(token, acc_id,
                                                         "-1", amount))


@bank_router.post("/account/transactions/{acc_id}")
def get_account_transactions(acc_id: str, token: str = Body(...)):
    user = User()
    if not verify_jwt(token, user):
        return {"Message": "Incorrect token!"}
    account = account_crud.read(acc_id)
    if account.user_id != user.uuid:
        return {"Message": "Not owned"}
    return get_crud_transaction().get_by_account_id(account)


@bank_router.post("/currency/create")
def create_currency(cur: CurrencyModel, token: str = Body(...)):
    u = User()
    if not verify_jwt(token, user_to=u):
        return {"Message": "Invalid token!"}
    u = get_crud_user().read(u.uuid)
    if not u.admin:
        return {"Message": "No permissions"}
    currency_crud = get_crud_currency()
    ident = currency_crud.create(**cur.dict())
    return {"Message": "Success", "CurrencyID": ident}
