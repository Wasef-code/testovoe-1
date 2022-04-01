FROM python:3
ADD . /backend/
WORKDIR /backend
RUN set -xe \
    && apt-get update -q -y \
    && apt-get install python3-pip postgresql-client -q -y
RUN pip install -r backend_requirements.txt
EXPOSE 8000