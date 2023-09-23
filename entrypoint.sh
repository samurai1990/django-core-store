#!/bin/bash


python manage.py migrate && \
python manage.py createadminuser && \

if [[ $1 = "debug" ]]; then
    tail -F targetio.log
elif [[ $1 = "stage" ]]; then
    gunicorn store_io.wsgi:application --bind 0.0.0.0:8000
fi
