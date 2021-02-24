# Urmart practice

## Env requirement

- Python 3.7
- Django 3.1.7

## Init database

    python manage.py migrate
    python manage.py loaddata dump.json


## Start

    python manage.py runserver


## Test data

        {
            "customer_id": "398d9c25"
            "customer_name": "jennifer lopez",
            "vip": true
        },
        {
            "customer_id": "7f584d2d"
            "customer_name": "cardi b",
            "vip": false
        },
            "customer_id": "ad68c1fb"
            "customer_name": "shirley",
            "vip"": false
        }