from domain.interfaces.db_interface import DbInterface
from domain.interfaces.mail_interface import MailInterface
from fastapi import HTTPException
from domain.globals.state import SECRET_KEY
cache: dict[type, object] = {}


def get_db() -> DbInterface:
    url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/maindb'
    db_interface = cache.get(DbInterface)
    if db_interface is None:
        db_interface = DbInterface(url)
        db_interface.init_tables()
        cache[DbInterface] = db_interface
    return db_interface


def create_session():
    return get_db().create_session()


def get_mail():
    mail_interface = cache.get(MailInterface)
    if mail_interface is None:
        mail_interface = MailInterface()
        if not mail_interface.login():
            raise HTTPException(500, "SMTP setup failed")
        cache[MailInterface] = mail_interface
    return mail_interface


def get_secret_key():
    return SECRET_KEY
