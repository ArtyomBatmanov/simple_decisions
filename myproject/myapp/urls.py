from django.urls import path
from .views import (
    BuyItemView,
    ItemPageView,
    PaymentSuccessView,
    PaymentErrorView,
    ItemsListView,
    OrderDetailView,
    OrderPaymentView,
    OrdersListView,
)

urlpatterns = [
    path('payment_error/', PaymentErrorView.as_view(), name='cancel'),
    path('payment_successful/', PaymentSuccessView.as_view(), name='success'),
    path('', ItemsListView.as_view(), name='home-page'),
    path('item/<int:pk>', ItemPageView.as_view(), name='item'),
    path('buy/<int:pk>/', BuyItemView.as_view(), name='create-checkout-session'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('myapp/payment/<int:pk>/', OrderPaymentView.as_view(), name='order-payment'),
    path('orders/', OrdersListView.as_view(), name='orders-list'),

]