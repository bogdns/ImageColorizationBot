FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install wget -y

COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
