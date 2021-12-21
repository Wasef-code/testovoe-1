from .userRepository import UserRepository
from .currencyRepository import CurrencyRepository
from .accountRepository import AccountRepository
from .transactionRepository import TransactionRepository
from deps.deps import get_db
SESSION = get_db().get_session()
user_repo = UserRepository(SESSION)
user_repo.upload()
currency_repo = CurrencyRepository(SESSION)
currency_repo.upload()
account_repo = AccountRepository(SESSION)
account_repo.upload()
transaction_repo = TransactionRepository(SESSION)
transaction_repo.upload()
