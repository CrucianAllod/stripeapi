from django.db import models
from decimal import Decimal

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=(('usd', 'USD'), ('eur', 'EUR')), default='usd')
    

    def __str__(self):
        return self.name
    
class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_coupon_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.code

class Tax(models.Model):
    name = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=255, unique=True, null=True) 
    percentage = models.FloatField(default=10.0)
    inclusive = models.BooleanField(default=False)
    jurisdiction = models.CharField(max_length=255, default='RU')

    def __str__(self):
        return self.name
    
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)

    def get_total_price(self):
        total = sum(item.get_total_price() for item in self.items.all())
        if self.discount:
            total -= self.discount.amount
        if self.tax:
            total *= (Decimal('1') + Decimal(str(self.tax.percentage)) / Decimal('100'))
        return total
    
    def __str__(self):
        return f"Order #{self.id} - Total: {self.get_total_price()}"    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.item.price * self.quantity    
