from domain.deps.deps_crud import get_crud_account
from domain.deps.deps_repo import get_user_repo
from domain.entities.entities import User
from domain.schemas.schemas import AccountModel
from domain.util.util import verify_jwt


class BankService:
    def create_account(self, acc: AccountModel, token: str):
        acc_crud = get_crud_account()
        u = User()
        if not verify_jwt(token, get_user_repo(), u):
            return {"Message": "Invalid token!"}
        if acc.user_id != u.uuid:
            return {"Message": "Invalid user ID!"}
        accounts_list = acc_crud.read_by_user_id(acc.user_id)
        for i in accounts_list:
            if i.currency_tag == acc.currency_tag:
                return {"Message": "Already exists!"}
        account_id = acc_crud.create(0, acc.currency_tag, acc.user_id)
        return {"Message": "Success", "AccountID": account_id}
