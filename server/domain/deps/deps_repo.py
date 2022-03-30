from domain.deps.deps_interfaces import create_session
from domain.entities.entities import Account, Currency, User
from domain.repos.accountRepository import AccountRepository
from domain.repos.currencyRepository import CurrencyRepository
from domain.repos.userRepository import UserRepository
from domain.repos.transactionRepository import TransactionRepository
cache: dict[type, object] = {}


def get_account_repo() -> AccountRepository:
    account_repo = cache.get(AccountRepository)
    if account_repo is None:
        with create_session() as session, session.begin():
            account_repo = AccountRepository()
            account_repo.from_list(session.query(Account).all())
            cache[AccountRepository] = account_repo
    return account_repo


def get_user_repo() -> UserRepository:
    user_repo = cache.get(UserRepository)
    if user_repo is None:
        with create_session() as session, session.begin():
            user_repo = UserRepository()
            user_repo.from_list(session.query(User).all())
            cache[UserRepository] = user_repo
    return user_repo


def get_currency_repo() -> CurrencyRepository:
    account_repo = cache.get(CurrencyRepository)
    if account_repo is None:
        with create_session() as session, session.begin():
            account_repo = CurrencyRepository()
            account_repo.from_list(session.query(Currency).all())
            cache[CurrencyRepository] = account_repo
    return account_repo


def get_transaction_repo() -> TransactionRepository:
    transaction_repo = cache.get(TransactionRepository)
    if transaction_repo is None:
        with create_session() as session, session.begin():
            transaction_repo = TransactionRepository()
            transaction_repo.from_list(session.query(Account).all())
            cache[TransactionRepository] = transaction_repo
    return transaction_repo
