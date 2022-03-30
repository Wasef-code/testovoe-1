from fastapi import FastAPI
from endpoints.auth import auth_router
from endpoints.bank import bank_router
from domain.deps.deps_interfaces import get_db
from requests import get
from sqlalchemy.exc import SQLAlchemyError
Main = get_db()
app = FastAPI()
# TODO: MAKE CRUD LAYER AND TRANSFER ALL LOGIC FROM ENDPOINTS TO IT


@app.on_event("shutdown")
def shutdown_event():
    pass


def startup():
    from domain.entities.entities import CurrencyDB
    with get_db().create_session() as session, session.begin():
        try:
            rub = get("https://free.currconv.com/api/v7/convert?q=RUB_USD&compact=\
                    ultra&apiKey=739681f9901ab24c75b2").json()
            eur = get("https://free.currconv.com/api/v7/convert?q=EUR_USD&compact=\
                    ultra&apiKey=739681f9901ab24c75b2").json()
            session.merge(CurrencyDB(
                tag="RUB",
                name="Рубль",
                cost=rub["RUB_USD"]
            ))
            session.merge(CurrencyDB(
                tag="EUR",
                name="Евро",
                cost=eur["EUR_USD"]
            ))
            session.merge(CurrencyDB(
                tag="USD",
                name="Доллар",
                cost=1
            ))
        except SQLAlchemyError:
            return


startup()
app.include_router(auth_router)
app.include_router(bank_router)
