FROM python:3.8-alpine

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .
ENV PYTHONPATH /app

ENTRYPOINT /app/bin/airport_exporter
