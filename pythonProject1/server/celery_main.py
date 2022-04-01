from celery import Celery
from celery.utils.log import get_task_logger
from requests import get
from domain.deps.deps_repo import CurrencyRepository
from domain.deps.deps_interfaces import get_db
from domain.entities.entities import Currency
celery_app = Celery(__name__, broker='amqp://admin:password@rabbit:5672//')
celery_app.config_from_object(__name__)
logger = get_task_logger(__name__)


@celery_app.task()
def x():
    with get_db().create_session() as conn, conn.begin():
        c = CurrencyRepository(conn.query(Currency).all())
        for i in c.get_currencies():
            response = get(f"https://free.currconv.com/api/v7/convert?q=USD_{i}&\
                            compact=ultra&apiKey=739681f9901ab24c75b2")
            x = response.json()
            if x == {}:
                continue
            c.update_currency(i, x[f"USD_{i}"])
            conn.merge()


celery_app.conf.beat_schedule = {
    'upload': {
        'task': 'celery_main.x',
        'schedule': 60 * 60 * 24,
    }
}
