FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install wget -y

COPY . /app

RUN wget https://huggingface.co/jessicanono/filparty_colorization/resolve/main/colorization_md1.pth -O /app/network/colorization_md1.pth

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
