from django.urls import path
from .views import (
    BuyItemView,
    ItemPageView,
    SuccessView,
    CancelView,
    ItemsListView,
    OrderDetailView,
    OrderPaymentView
)

urlpatterns = [
    path('payment_error/', CancelView.as_view(), name='cancel'),
    path('payment_successful/', SuccessView.as_view(), name='success'),
    path('', ItemsListView.as_view(), name='home-page'),
    path('item/<int:pk>', ItemPageView.as_view(), name='item'),
    path('buy/<int:pk>/', BuyItemView.as_view(), name='create-checkout-session'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('myapp/payment/<int:pk>/', OrderPaymentView.as_view(), name='order-payment')

]