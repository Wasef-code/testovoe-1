from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.sql.sqltypes import Boolean
from db_interface import Main
BaseDB = Main.base
class User(BaseModel):
    email: str
    phone_number: str
    password: str
    name: str
    last_name: str
    surname: str
    class Config:
        orm_mode = True
class UserDB(BaseDB):
    __tablename__ = "users"
    uuid: Column = Column(String, primary_key=True)
    is_admin: Column = Column(Boolean, default=False)
    email: Column = Column(String)
    phone_number: Column = Column(String)
    password: Column = Column(String)
    name: Column = Column(String)
    last_name: Column = Column(String)
    surname: Column = Column(String)
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
class CurrencyDB(BaseDB):
    __tablename__ = "currencies"
    tag: Column = Column(String, primary_key=True)
    name: Column = Column(String)
    cost: Column = Column(Float)
class Transaction(BaseModel):
    amount: float
    currency_tag: str
    account_from_id: str
    account_to_id: str
    created_at: datetime
    class Config:
        orm_mode = True
class TransactionDB(BaseDB):
    __tablename__ = "transactions"
    id: Column = Column(String, primary_key=True)
    amount: Column = Column(Float)
    currency_tag: Column = Column(String)
    account_from_id: Column = Column(String)
    account_to_id: Column = Column(String)
    created_at: Column = Column(DateTime)
class Account(BaseModel):
    currency_tag: str
    user_id: str
    class Config:
        orm_mode = True
class AccountDB(BaseDB):
    __tablename__ = "accounts"
    id: Column = Column(String, primary_key=True)
    amount: Column = Column(Float)
    currency_tag: Column = Column(String)
    user_id: Column = Column(String)
class TransactionRequest(BaseModel):
    token: str
    account_from_id: str
    account_to_id: str
    amount: float
BaseDB.metadata.create_all(Main.GetEngine())