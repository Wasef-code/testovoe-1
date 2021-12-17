from sqlalchemy import Column, Float, String
from db_interface import Main
BaseDB = Main.base
class CurrencyDB(BaseDB):
    __tablename__ = "currencies"
    tag: Column = Column(String, primary_key=True)
    name: Column = Column(String)
    cost: Column = Column(Float)
BaseDB.metadata.create_all(Main.GetEngine())