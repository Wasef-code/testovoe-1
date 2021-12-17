from fastapi import APIRouter, Body
from models import Account, Currency, TransactionRequest, UserDB
from repos import account_repo, user_repo, currency_repo, transaction_repo as trans_repo
from util import VerifyJWT
bank_router = APIRouter()
@bank_router.post("/account/create")
def CreateAccount(acc: Account, token: str = Body(...)):
    u = UserDB()
    if not VerifyJWT(token, user_repo, u):
        return {"Message": "Invalid token!"}
    if acc.user_id != u.uuid:
        return {"Message": "Invalid user ID!"}
    l = account_repo.GetUserAccounts(acc.user_id)
    for i in l:
        if i.currency_tag == acc.currency_tag:
            return {"Message": "Account with that currency already exists!"}
    i = account_repo.CreateAccount(acc.user_id, acc.currency_tag)
    return {"Message": "Success", "AccountID": i}
@bank_router.delete("/account/delete/{acc_id}")
def CloseAccount(acc_id: str):
    account_repo.DeleteAccount(acc_id)
@bank_router.post("/account/transfer/")
def Transfer(request: TransactionRequest):
    u = UserDB()
    if not VerifyJWT(request.token, user_repo, u):
        return {"Message": "Incorrect token!"}
    x = account_repo.GetAccount(request.account_from_id).user_id
    if x != u.uuid:
        return {"Message": "You're not owner of this account!", "Owner": x, "You": u.uuid}
    if not account_repo.Transfer(request.account_from_id, request.account_to_id, request.amount, currency_repo, trans_repo):
        return {"Message": "Some error occured during transfer! Don't worry, everything restored as before."}
    return {"Message": "Success"}
@bank_router.post("/account/{acc_id}")
def GetAccount(acc_id: str, token: str = Body(...)):
    u = UserDB()
    if not VerifyJWT(token, user_repo, u):
        return {"Message": "Incorrect token!"}
    acc = account_repo.GetAccount(acc_id)
    if acc.id == "":
        return {"Message": "No account like that exist!"}
    if acc.user_id != u.uuid:
        return {"Message": "You can't see others' account state!"}
    return acc
@bank_router.post("/account")
def GetUserAccounts(user_id: str = Body(...), token: str = Body(...)):
    u = UserDB()
    if not VerifyJWT(token, user_repo, u):
        return {"Message": "Incorrect token!"}
    return account_repo.GetUserAccounts(user_id)
@bank_router.post("/account/deposit/{acc_id}")
def Deposit(acc_id: str, token: str = Body(...), amount: float = Body(...)):
    if not VerifyJWT(token, user_repo):
        return {"Message": "Incorrect token!"}
    acc = account_repo.GetAccount(acc_id)
    if not account_repo.Transfer("-1", acc_id, amount, currency_repo, trans_repo):
        return {"Message": "Some error occured during transfer! Don't worry, everything restored as before."}
    return {"Message": "Success"}
@bank_router.post("/account/withdraw/{acc_id}")
def Withdraw(acc_id: str, token: str = Body(...), amount: float = Body(...)):
    u = UserDB()
    if not VerifyJWT(token, user_repo, u):
        return {"Message": "Incorrect token!"}
    if account_repo.GetAccount(acc_id).user_id != u.uuid:
        return {"Message": "You can't withdraw from this account!"}
    if account_repo.Transfer(acc_id, "-1", amount, currency_repo, trans_repo):
        return {"Message": "Some error occured during transfer! Don't worry, everything restored as before."}
    return {"Message": "Success"}
@bank_router.post("/account/transactions/{acc_id}")
def GetAccountTransactions(acc_id: str, token: str = Body(...)):
    if acc_id == "":
        return {"Message": "Invalid acc ID!"}
    u = UserDB()
    if not VerifyJWT(token, user_repo, u):
        return {"Message": "Incorrect token!"}
    if account_repo.GetAccount(acc_id).user_id != u.uuid:
        return {"Message": "You can't watch others' account transactions!"}
    l = trans_repo.GetAccountTransactions(acc_id)
    return l
@bank_router.post("/currency/create")
def CreateCurrency(cur: Currency, token: str = Body(...)):
    if not VerifyJWT(token, user_repo):
        return {"Message": "Invalid token!"}
    currency_repo.CreateCurrency(cur.tag, cur.name, cur.cost)
    return {"Message": "Success"}