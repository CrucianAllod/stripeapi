from django.urls import path
from .views import (BuyItemView, CancelView, HomePageView, 
                    ItemDetailView, OrderBuyView, SuccessView,
                    AddInOrderView, OrderSummaryView)

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('buy/<int:item_id>/', BuyItemView.as_view(), name='buy'),
    path('item/<int:item_id>/', ItemDetailView.as_view(), name='item_detail'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('add_to_order/<int:item_id>/', AddInOrderView.as_view(), name='add_to_order'),
    path('order_buy/<int:order_id>/', OrderBuyView.as_view(), name='order_buy'),
    path('order_summary/<int:order_id>/', OrderSummaryView.as_view(), name='order_summary'),

] 