FROM python:3.11

WORKDIR /opt/telegram_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE 'core.settings'

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .