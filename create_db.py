import os
import sys
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stripeapi.settings')

import django
django.setup()

from itemstripe.stripe_utils import create_stripe_coupon, create_tax_rate
from itemstripe.models import Discount, Item, Tax


def create():
    items = [
        {'name': 'Item 1', 'description': 'Description for Item 1', 'price': 100.00, 'currency': 'usd'},
        {'name': 'Item 2', 'description': 'Description for Item 2', 'price': 200.00, 'currency': 'eur'},
        {'name': 'Item 3', 'description': 'Description for Item 3', 'price': 300.00, 'currency': 'usd'},
        {'name': 'Item 4', 'description': 'Description for Item 4', 'price': 400.00, 'currency': 'eur'},
        {'name': 'Item 5', 'description': 'Description for Item 5', 'price': 500.00, 'currency': 'usd'},
        {'name': 'Item 6', 'description': 'Description for Item 6', 'price': 600.00, 'currency': 'eur'},
    ]

    for item_data in items:
        Item.objects.create(**item_data)

    if not Tax.objects.exists():
        tax_rates = [
            {
                'display_name': 'Tax Name 1',
                'description': 'Tax Description 1',
                'percentage': 10.0,
                'inclusive': False,
                'jurisdiction': 'RU',
            },
        ]

        for tax_rate in tax_rates:
            stripe_tax_rate = create_tax_rate(**tax_rate)
            Tax.objects.create(
                name=tax_rate['display_name'],
                stripe_id=stripe_tax_rate.id,
                percentage=tax_rate['percentage'],
                inclusive=tax_rate['inclusive'],
                jurisdiction=tax_rate['jurisdiction'],
            )

    if not Discount.objects.exists():
        coupons = [
            {
                'code': 'DISCOUNT' + str(random.randint(1,1000)) + '_USD',
                'amount': 10.0,
            },
                        {
                'code': 'DISCOUNT' + str(random.randint(1,1000)) + '_EUR',
                'amount': 10.0,
            },
        ]

        for coupon in coupons:
            stripe_coupon = create_stripe_coupon(coupon['code'], coupon['amount'])
            Discount.objects.create(
                code=coupon['code'],
                amount=coupon['amount'],
                stripe_coupon_id=stripe_coupon.id,
            )


if __name__ == '__main__':
    create()
    print('Тестовые данные успешно добавлены в базу данных.')