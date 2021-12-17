from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import close_all_sessions
class DbInterface:
    def __init__(self, url):
        self.__engine: Engine = create_engine(url)
        self.__session: Session = sessionmaker(self.__engine)()
        self.base = declarative_base()
    def OpenConn(self) -> Session:
        return sessionmaker(self.__engine)()
    def GetEngine(self) -> Engine:
        return self.__engine
    def GetSession(self) -> Session:
        return self.__session
    def Close(self):
        close_all_sessions()
Main = DbInterface('postgresql+psycopg2://postgres:postgres@db/maindb')
SESSION = Main.GetSession()