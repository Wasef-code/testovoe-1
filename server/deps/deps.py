from interfaces.db_interface import Main
from interfaces.mail_interface import MailInterface as Mail
from globals.state import SECRET_KEY
__mail = Mail()


def get_db():
    return Main


def get_mail():
    return __mail

def get_secret_key():
    return SECRET_KEY