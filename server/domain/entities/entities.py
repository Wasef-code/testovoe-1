from sqlalchemy import Column, Float, String, DateTime, ForeignKey, Boolean
from domain.entities.base_class import Base


class User(Base):
    __tablename__ = "users"
    admin: Column = Column(Boolean, default=False)
    email: Column = Column(String)
    phone_number: Column = Column(String)
    password: Column = Column(String)
    name: Column = Column(String)
    last_name: Column = Column(String)
    surname: Column = Column(String)
    activated = Column(Boolean, default=False)


class Currency(Base):
    __tablename__ = "currencies"
    tag: Column = Column(String, primary_key=True)
    name: Column = Column(String)
    cost: Column = Column(Float)


class Account(Base):
    __tablename__ = "accounts"
    amount: Column = Column(Float)
    currency_tag: Column = Column(String, ForeignKey(Currency.tag))
    user_id: Column = Column(String, ForeignKey(User.uuid))


class Transaction(Base):
    __tablename__ = "transactions"
    amount: Column = Column(Float)
    currency_tag: Column = Column(String, ForeignKey(Currency.tag))
    account_from_id: Column = Column(String, ForeignKey(Account.uuid))
    account_to_id: Column = Column(String, ForeignKey(Account.uuid))
    created_at: Column = Column(DateTime)


# TODO: CHECK WHY UUID ISN'T HIGHLIGHTNING ANYMORE
