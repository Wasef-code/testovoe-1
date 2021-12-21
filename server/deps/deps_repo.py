from repos.repos import transaction_repo, user_repo, currency_repo, account_repo


def get_account_repo():
    return account_repo


def get_user_repo():
    return user_repo


def get_currency_repo():
    return currency_repo


def get_transaction_repo():
    return transaction_repo