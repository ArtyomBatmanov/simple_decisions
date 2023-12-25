import stripe
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.detail import DetailView
from .models import Item, Order
from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentSuccessView(TemplateView):
    template_name = "myapp/payment_successful.html"


class PaymentErrorView(TemplateView):
    template_name = "myapp/payment_error.html"


class ItemPageView(TemplateView):
    template_name = "myapp/item.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        product = Item.objects.get(pk=pk)
        context = super(ItemPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class ItemsListView(TemplateView):
    template_name = "myapp/items-list.html"

    def get_context_data(self, **kwargs):
        products = Item.objects.all()
        context = super(ItemsListView, self).get_context_data(**kwargs)
        context.update({
            "items": products,
        })
        return context


class OrdersListView(ListView):
    template_name = "myapp/orders_list.html"
    context_object_name = 'orders'
    queryset = Order.objects.all()


class BuyItemView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(id=item_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency,
                        'unit_amount': int(item.price * 100),
                        'product_data': {
                            'name': item.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": item.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/payment_successful/',
            cancel_url=YOUR_DOMAIN + '/payment_error/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class OrderDetailView(DetailView):
    model = Order
    template_name = 'myapp/order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # order = self.object
        # total_price = order.items.aggregate(sum_price=Sum('price'))['sum_price'] or Decimal('0.00')
        # total_price += order.taxes.aggregate(sum_tax=Sum('amount'))['sum_tax'] or Decimal('0.00')
        # total_price -= order.discounts.aggregate(sum_discount=Sum('amount'))['sum_discount'] or Decimal('0.00')
        #
        # # Применяем скидку и налог в процентах
        # total_price *= (1 + order.tax / 100)
        # total_price *= (1 - order.discount / 100)
        #
        # context['total_price'] = total_price

        pk = self.kwargs.get("pk")
        order = Order.objects.get(pk=pk)
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context.update({
            "order": order,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })

        return context


class OrderPaymentView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order = Order.objects.get(pk=pk)
        order.update_total_price()
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': order.currency,
                    'product_data': {
                        'name': f'Order {order.id}',
                    },
                    'unit_amount': int(order.total_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/payment_successful/',
            cancel_url=YOUR_DOMAIN + '/payment_error/',
        )

        # Сохраняем id сессии в заказе
        order.payment_session_id = session.id
        order.save()

        # Возвращаем ID платежной сессии
        return JsonResponse({'session_id': session.id})






