from django import forms
from .models import Tax, Discount

class OrderForm(forms.Form):
    tax = forms.ModelChoiceField(queryset=Tax.objects.all(), required=False)
    discount = forms.ModelChoiceField(queryset=Discount.objects.all(), required=False)
