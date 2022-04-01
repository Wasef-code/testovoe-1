FROM python:3
ADD . /celery
WORKDIR /celery
RUN set -xe \
    && apt-get update -q -y \
    && apt-get install python3-pip rabbitmq-server postgresql-client -q -y
RUN pip install -r celery_requirements.txt