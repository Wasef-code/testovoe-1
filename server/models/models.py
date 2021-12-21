from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.sql.sqltypes import Boolean
from interfaces.db_interface import Main
BaseDB = Main.base


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


class CurrencyDB(BaseDB):
    __tablename__ = "currencies"
    tag: Column = Column(String, primary_key=True)
    name: Column = Column(String)
    cost: Column = Column(Float)


class TransactionDB(BaseDB):
    __tablename__ = "transactions"
    id: Column = Column(String, primary_key=True)
    amount: Column = Column(Float)
    currency_tag: Column = Column(String)
    account_from_id: Column = Column(String)
    account_to_id: Column = Column(String)
    created_at: Column = Column(DateTime)


class AccountDB(BaseDB):
    __tablename__ = "accounts"
    id: Column = Column(String, primary_key=True)
    amount: Column = Column(Float)
    currency_tag: Column = Column(String)
    user_id: Column = Column(String)


BaseDB.metadata.create_all(Main.get_engine())