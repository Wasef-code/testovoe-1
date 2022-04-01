from typing import Type
from domain.services.auth_service import AuthService
from domain.services.bank_service import BankService
cache: dict[Type, object] = {}


def get_auth_service() -> AuthService:
    auth_service = cache.get(AuthService)
    if auth_service is None:
        auth_service = AuthService()
        cache[AuthService] = auth_service
    return auth_service


def get_bank_service() -> BankService:
    bank_service = cache.get(BankService)
    if bank_service is None:
        bank_service = BankService()
        cache[BankService] = bank_service
    return bank_service
