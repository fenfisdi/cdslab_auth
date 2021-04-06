FROM python:3.8-slim-buster

EXPOSE 5000

ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

COPY requirements.txt .

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

WORKDIR ${APP_HOME}

COPY . .

ENTRYPOINT uvicorn main:app --host 0.0.0-0 --port 5000 --reload