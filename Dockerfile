# temp stage
FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install -y build-essential libpq-dev python3-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
