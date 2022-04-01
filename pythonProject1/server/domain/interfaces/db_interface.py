from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from domain.entities.entities import Base


class DbInterface:

    def __init__(self, url):
        self.__engine: Engine = create_engine(url)
        self.__sessionmaker = sessionmaker(self.__engine)

    def create_session(self) -> Session:
        return sessionmaker(self.__engine)()

    def init_tables(self):
        Base.metadata.create_all(self.__engine)
