from fastapi import APIRouter, Body
from models.models import UserDB
from schemas.schemas import Account, Currency, TransactionRequest, User
from deps.deps_repo import get_account_repo, get_currency_repo, get_transaction_repo, get_user_repo
from util.util import verify_jwt
bank_router = APIRouter()


@bank_router.post("/account/create")
def create_account(acc: Account, token: str = Body(...)):
    acc_repo = get_account_repo()
    u = UserDB()
    if not verify_jwt(token, get_user_repo(), u):
        return {"Message": "Invalid token!"}
    if acc.user_id != u.uuid:
        return {"Message": "Invalid user ID!"}
    l = acc_repo.get_user_accounts(acc.user_id)
    for i in l:
        if i.currency_tag == acc.currency_tag:
            return {"Message": "Account with that currency already exists!"}
    i = acc_repo.create_account(acc.user_id, acc.currency_tag)
    return {"Message": "Success", "AccountID": i}


@bank_router.delete("/account/delete/{acc_id}")
def close_account(acc_id: str, token: str = Body(...)):
    u = UserDB()
    if not verify_jwt(token, get_user_repo(), u):
        return {"Message": "Incorrect token!"}
    if not get_account_repo().get_account(acc_id).user_id == u.uuid:
        return {"Message": "You're not owner of this account!"}
    get_account_repo().delete_account(acc_id)
    return {"Message": "Success"}


@bank_router.post("/account/transfer/")
def transfer(request: TransactionRequest):
    acc_repo = get_account_repo()
    u = UserDB()
    if not verify_jwt(request.token, get_user_repo(), u):
        return {"Message": "Incorrect token!"}
    x = acc_repo.get_account(request.account_from_id).user_id
    if x != u.uuid:
        return {"Message": "You're not owner of this account!", "Owner": x, "You": u.uuid}
    if not acc_repo.transfer(request.account_from_id, request.account_to_id, request.amount,
            get_currency_repo(), get_transaction_repo()):
        return {"Message": "Some error occured during transfer! Don't worry, everything restored as before."}
    return {"Message": "Success"}


@bank_router.post("/account/{acc_id}")
def get_account(acc_id: str, token: str = Body(...)):
    u = UserDB()
    if not verify_jwt(token, get_user_repo(), u):
        return {"Message": "Incorrect token!"}
    acc = get_account_repo().get_account(acc_id)
    if acc.id == "":
        return {"Message": "No account like that exist!"}
    if acc.user_id != u.uuid:
        return {"Message": "You can't see others' account state!"}
    return acc


@bank_router.post("/account")
def get_user_accounts(user_id: str = Body(...), token: str = Body(...)):
    u = UserDB()
    if not verify_jwt(token, get_user_repo(), u):
        return {"Message": "Incorrect token!"}
    return get_account_repo().get_user_accounts(user_id)


@bank_router.post("/account/deposit/{acc_id}")
def deposit(acc_id: str, token: str = Body(...), amount: float = Body(...)):
    acc_repo = get_account_repo()
    if not verify_jwt(token, get_user_repo()):
        return {"Message": "Incorrect token!"}
    if not acc_repo.transfer("-1", acc_id, amount, get_currency_repo(), get_transaction_repo()):
        return {"Message": "Some error occured during transfer! Don't worry, everything restored as before."}
    return {"Message": "Success"}


@bank_router.post("/account/withdraw/{acc_id}")
def withdraw(acc_id: str, token: str = Body(...), amount: float = Body(...)):
    acc_repo = get_account_repo()
    u = UserDB()
    if not verify_jwt(token, get_user_repo(), u):
        return {"Message": "Incorrect token!"}
    if acc_repo.get_account(acc_id).user_id != u.uuid:
        return {"Message": "You can't withdraw from this account!"}
    if acc_repo.transfer(acc_id, "-1", amount, get_currency_repo(), get_transaction_repo()):
        return {"Message": "Some error occured during transfer! Don't worry, everything restored as before."}
    return {"Message": "Success"}


@bank_router.post("/account/transactions/{acc_id}")
def get_account_transactions(acc_id: str, token: str = Body(...)):
    if acc_id == "":
        return {"Message": "Invalid acc ID!"}
    u = UserDB()
    if not verify_jwt(token, get_user_repo(), u):
        return {"Message": "Incorrect token!"}
    if get_account_repo().get_account(acc_id).user_id != u.uuid:
        return {"Message": "You can't watch others' account transactions!"}
    l = get_transaction_repo().get_account_transactions(acc_id)
    return l


@bank_router.post("/currency/create")
def create_currency(cur: Currency, token: str = Body(...)):
    if not verify_jwt(token, get_user_repo()):
        return {"Message": "Invalid token!"}
    get_currency_repo().create_currency(cur.tag, cur.name, cur.cost)
    return {"Message": "Success"}