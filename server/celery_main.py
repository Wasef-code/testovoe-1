from celery import Celery
from celery.utils.log import get_task_logger
from requests import get    
from repos.currencyRepository import CurrencyRepository
from interfaces.db_interface import DbInterface
celery_app = Celery(__name__, broker='amqp://admin:password@rabbit:5672//')
celery_app.config_from_object(__name__)
logger = get_task_logger(__name__)


@celery_app.task()
def x():
    interface = DbInterface('postgresql+psycopg2://postgres:postgres@db/maindb')
    conn = interface.get_session()
    c = CurrencyRepository(conn)
    c.upload()
    for i in c.get_currencies():
        response = get(f"https://free.currconv.com/api/v7/convert?q=USD_{i}&compact=ultra&apiKey=739681f9901ab24c75b2")
        x = response.json()
        if x == {}:
            continue
        c.update_currency(i, x[f"USD_{i}"])
    interface.close()


celery_app.conf.beat_schedule = {
    'upload': {
        'task': 'celery_main.x',
        'schedule': 60 * 60 * 24,
    }
}