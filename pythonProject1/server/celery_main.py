from celery import Celery
from celery.utils.log import get_task_logger
from requests import get
from domain.services.crud_currency import CrudCurrency
celery_app = Celery(__name__, broker='amqp://admin:password@rabbit:5672//')
celery_app.config_from_object(__name__)
logger = get_task_logger(__name__)


@celery_app.task()
def x():
    c = CrudCurrency()
    for i in c.read_multi():
        response = get(f"https://free.currconv.com/api/v7/convert?q=USD_{i.tag}&\
                         compact=ultra&apiKey=739681f9901ab24c75b2")
        x = response.json()
        if x is {}:
            continue
        c.update(i.uuid, amount=x[f"USD_{i.tag}"])


celery_app.conf.beat_schedule = {
    'upload': {
        'task': 'celery_main.x',
        'schedule': 60 * 60 * 24,
    }
}
