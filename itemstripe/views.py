from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import stripe
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .forms import OrderForm

from .stripe_utils import create_checkout_session, create_payment_intent
from .models import Item, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY_USD

class BuyItemView(View):
    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        if item.currency == 'usd':
            stripe.api_key = settings.STRIPE_SECRET_KEY_USD
        else:
            stripe.api_key = settings.STRIPE_SECRET_KEY_EUR
            
        payment_intent = create_payment_intent(
            amount=int(item.price * 100),
            currency=item.currency,
        )
        return JsonResponse({'client_secret': payment_intent.client_secret})
    
class ItemDetailView(View):
    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        return render(request, 'item_detail.html', {'item': item, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})

class OrderBuyView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        total_amount = order.get_total_price()
        first_item = order.items.first()
        if not first_item:
            return HttpResponseBadRequest("Order does not contain any items.")

        currency = first_item.item.currency


        discounts = []
        if order.discount:
            discounts.append({
                'coupon': order.discount.code,
            })

        tax_rates = []
        if order.tax:
            tax_rates.append(order.tax.stripe_id)


        line_items = [{
            'price_data': {
                'currency': currency,
                'unit_amount': int(total_amount * 100),
                'product_data': {
                    'name': 'Order Payment',
                },
            },
            'quantity': 1,
            "tax_rates": tax_rates
        }]

        success_url = request.build_absolute_uri(reverse('success'))
        cancel_url = request.build_absolute_uri(reverse('cancel'))
        

        session = create_checkout_session(line_items, success_url, cancel_url, discounts=discounts)
        return JsonResponse({'session_id': session.id})

class AddInOrderView(View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        order_id = request.session.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            if order.items.exists() and order.items.first().item.currency != item.currency:
                    return HttpResponseBadRequest("Все товары в заказе должны быть в одной валюте.")
            
        except Order.DoesNotExist:
            order = Order.objects.create()
            request.session['order_id'] = order.id
        
        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        if not created:
            order_item.quantity += 1
            order_item.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))

class OrderSummaryView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = OrderForm(initial={'tax': order.tax, 'discount': order.discount})
        return render(request, 'order_summary.html', {'order': order,'form': form, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})
    
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = OrderForm(request.POST)
        if form.is_valid():
            order.tax = form.cleaned_data['tax']
            order.discount = form.cleaned_data['discount']
            order.save()
            return redirect('order_summary', order_id=order.id)
        return render(request, 'order_summary.html', {'order': order, 'form': form, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})

class HomePageView(View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'index.html', {'items': items})

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"   