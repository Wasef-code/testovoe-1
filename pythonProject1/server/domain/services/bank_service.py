from domain.deps.deps_crud import get_crud_account
from domain.entities.entities import User
from domain.schemas.schemas import AccountModel, TransactionRequestModel
from domain.util.util import verify_jwt


class BankService:
    def __init__(self):
        self.account_crud = get_crud_account()

    def create_account(self, acc: AccountModel, token: str):
        acc_crud = self.account_crud
        u = User()
        if not verify_jwt(token, u):
            return {"Message": "Invalid token!"}
        if acc.user_id != str(u.uuid):
            return {"Message": "Invalid user ID!"}
        accounts_list = acc_crud.read_by_user_id(acc.user_id)
        for i in accounts_list:
            if i.currency_tag == acc.currency_tag:
                return {"Message": "Already exists!"}
        account_id = acc_crud.create(**acc.dict())
        return {"Message": "Success", "AccountID": account_id}

    def close_account(self, acc_id: str, token: str):
        u = User()
        if not verify_jwt(token, u):
            return {"Message": "Incorrect token!"}
        if not self.account_crud.read(acc_id).user_id == u.uuid:
            return {"Message": "You're not owner of this account!"}
        self.account_crud.delete(acc_id)
        return {"Message": "Success"}

    def transfer(self, request: TransactionRequestModel):
        acc_crud = self.account_crud
        u = User()
        if not verify_jwt(request.token, u):
            return {"Message": "Incorrect token!"}
        x = acc_crud.read(request.account_from_id).user_id
        if x != u.uuid:
            return {"Message": "You're not owner of this account!", "Owner": x,
                    "You": u.uuid}
        if not acc_crud.transfer(request.account_from_id, request.
                                 account_to_id, request.amount):
            return {"Message": "Some error occured during transfer! Don't worry,\
                    everything restored as before."}
        return {"Message": "Success"}
