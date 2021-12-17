from mail_interface import MailInterface
from userRepository import UserRepository
from currencyRepository import CurrencyRepository
from accountRepository import AccountRepository
from transactionRepository import TransactionRepository
from db_interface import SESSION
user_repo = UserRepository(SESSION)
user_repo.Upload()
currency_repo = CurrencyRepository(SESSION)
currency_repo.Upload()
account_repo = AccountRepository(SESSION)
account_repo.Upload()
transaction_repo = TransactionRepository(SESSION)
transaction_repo.Upload()
mail = MailInterface()