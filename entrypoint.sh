#!/bin/sh

# Миграции БД
python manage.py migrate

# Запускаем джанго-сервер
python manage.py runserver 0.0.0.0:8000
