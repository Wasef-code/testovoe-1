from uuid import UUID
from random import randint
SECRET_KEY = '049de71b99848929230a58fac583786f493da59477e715f3b8ec84485c7fbef3'
__SECRET_ARRAY: str = "0123456789ABCDEFGJKLMNOPQRSTUVWXYZ"


def generate_id() -> str:
    spisok = [__SECRET_ARRAY[randint(0, len(__SECRET_ARRAY) - 1)] for i in range(16)]
    return UUID(bytes="".join(spisok).encode('utf-8')).__str__()
