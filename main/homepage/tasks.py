import requests
from celery import chain, shared_task
from .models import Currency


@shared_task
def parse_private():
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    currency = response.json()
    return currency


@shared_task
def save_currency_to_model(currency):
    instance = Currency()
    instance.content = currency
    instance.save()

@shared_task
def common_task():
    chain(
        parse_private.s()
        |
        save_currency_to_model.s()
    )()
