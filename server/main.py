from fastapi import FastAPI
from auth import auth_router
from bank import bank_router
from db_interface import Main
from requests import get
from fastapi_utils.tasks import repeat_every
app = FastAPI()
@app.on_event("shutdown")
def shutdown_event():
    Main.Close()
def startup():
    from models import CurrencyDB
    session = Main.GetSession()
    rub = get("https://free.currconv.com/api/v7/convert?q=USD_RUB&compact=ultra&apiKey=739681f9901ab24c75b2").json()
    eur = get("https://free.currconv.com/api/v7/convert?q=USD_EUR&compact=ultra&apiKey=739681f9901ab24c75b2").json()
    session.merge(CurrencyDB(
        tag="RUB",
        name="Рубль",
        cost=rub["USD_RUB"]
    ))
    session.merge(CurrencyDB(
        tag="EUR",
        name="Евро",
        cost=eur["USD_EUR"]
    ))
    session.merge(CurrencyDB(
        tag="USD",
        name="Доллар",
        cost=1
    ))
    print("IM WORKING!")
    session.commit()
startup()
@app.on_event('startup')
@repeat_every(seconds=60)
def Repeater():
    print("COMMITING, DON'T MOVE...")
    Main.GetSession().commit()
app.include_router(auth_router)
app.include_router(bank_router)