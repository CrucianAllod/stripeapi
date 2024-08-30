import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY_USD

def create_tax_rate(display_name, description, percentage, inclusive, jurisdiction):
    tax_rate = stripe.TaxRate.create(
        display_name=display_name,
        description=description,
        percentage=percentage,
        inclusive=inclusive,
        jurisdiction=jurisdiction,
    )
    return tax_rate

def create_stripe_coupon(code, amount):
    if 'EUR' in code:
        coupon = stripe.Coupon.create(
            duration="once",
            id=code,
            amount_off=int(amount * 100), 
            currency="eur"
        )
        return coupon
    else:
        coupon = stripe.Coupon.create(
            duration="once",
            id=code,
            amount_off=int(amount * 100), 
            currency="usd"
        )
        return coupon


def create_checkout_session(line_items, success_url, cancel_url, discounts=None):
    session_data = {
        'line_items': line_items,
        'mode': 'payment',
        'success_url': success_url,
        'cancel_url': cancel_url,
    }

    if discounts:
        session_data['discounts'] = discounts

    session = stripe.checkout.Session.create(**session_data)
    return session

def create_payment_intent(amount, currency, payment_method_types=['card'], discounts=None, tax_rates=None):
    intent_data = {
        'amount': amount,
        'currency': currency,
        'payment_method_types': payment_method_types,
    }

    if discounts:
        intent_data['discounts'] = discounts

    if tax_rates:
        intent_data['tax_rates'] = tax_rates

    payment_intent = stripe.PaymentIntent.create(**intent_data)
    return payment_intent
