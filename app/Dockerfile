FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
