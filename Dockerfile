FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install wget -y

COPY . /app

RUN /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
