from fastapi import APIRouter
from domain.deps.deps_service import get_auth_service
from domain.schemas.schemas import LoginUserModel, ResetUserModel,\
    RestoreUserModel, UserModel
from fastapi import Body
auth_router = APIRouter()
auth_service = get_auth_service()


@auth_router.post("/register")
def register(register_user: UserModel):
    return auth_service.create(register_user)


@auth_router.post("/verify")
def verify(code: int = Body(...), identifier: str = Body(...)):
    return auth_service.confirm(identifier, code)


@auth_router.post("/login")
def login(login_user: LoginUserModel):
    return auth_service.login(login_user)


@auth_router.post("/reset")
def reset(reset_user: ResetUserModel):
    return auth_service.reset(reset_user)


@auth_router.post("/restore")
def restore(restore_user: RestoreUserModel):
    return auth_service.restore(restore_user)


@auth_router.post("/refresh")
def refresh(token: str):
    return auth_service.refresh_token(token)
