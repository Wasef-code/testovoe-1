from celery import Celery
from celery.utils.log import get_task_logger
from requests import get    
from currencyRepository import CurrencyRepository
from db_interface import DbInterface
celery_app = Celery(__name__, broker='amqp://admin:password@rabbit:5672//')
celery_app.config_from_object(__name__)
logger = get_task_logger(__name__)
@celery_app.task()
def X():
    interface = DbInterface('postgresql+psycopg2://postgres:postgres@localhost:5432/maindb')
    conn = interface.GetSession()
    c = CurrencyRepository(conn)
    c.Upload()
    l = []
    for i in c.GetCurrencies():
        response = get(f"https://free.currconv.com/api/v7/convert?q=USD_{i}&compact=ultra&apiKey=739681f9901ab24c75b2")
        x = response.json()
        if x == {}:
            continue
        c.UpdateCurrency(i, x[f"USD_{i}"])
    interface.Close()
celery_app.conf.beat_schedule = {
    'upload': {
        'task': 'celery_main.X',
        'schedule': 60 * 60 * 24,
    }
}