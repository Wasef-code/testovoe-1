from typing import Type
from domain.services.auth_service import AuthService
cache: dict[Type, object] = {}


def get_auth_service() -> AuthService:
    auth_service = cache.get(AuthService)
    if auth_service is None:
        auth_service = AuthService()
        cache[AuthService] = auth_service
    return auth_service
