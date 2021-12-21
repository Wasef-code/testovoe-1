from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    email: str
    phone_number: str
    password: str
    name: str
    last_name: str
    surname: str

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    email: Optional[str]
    phone_number: Optional[str]
    password: str


class ResetUser(BaseModel):
    uuid: str
    token: str
    email: Optional[list[str]]
    phone_number: Optional[list[str]]
    name: Optional[str]
    last_name: Optional[str]
    surname: Optional[str]
    password: Optional[list[str]]


class RestoreUser(BaseModel):
    email: list[str]
    password: list[str]


class Currency(BaseModel):
    tag: str
    name: str
    cost: float

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    amount: float
    currency_tag: str
    account_from_id: str
    account_to_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionRequest(BaseModel):
    token: str
    account_from_id: str
    account_to_id: str
    amount: float


class Account(BaseModel):
    currency_tag: str
    user_id: str

    class Config:
        orm_mode = True
