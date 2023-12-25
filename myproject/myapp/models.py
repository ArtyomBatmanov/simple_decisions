from django.db import models
from decimal import Decimal
from django.db.models import Sum



class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)
    currency = models.CharField(max_length=3, default='RUB')


    def __str__(self):
        return self.name

    def get_str_to_dollars(self):
        return f"{self.price:.2f}"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    currency = models.CharField(max_length=3)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    def update_total_price(self):
        total_price = self.items.aggregate(sum_price=Sum('price'))['sum_price'] or Decimal('0.00')
        discount_amount = total_price * (self.discount / 100)
        total_price -= discount_amount
        tax_amount = total_price * (self.tax / 100)
        total_price += tax_amount

        self.total_price = total_price
        self.save()

class Discount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discounts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Tax(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='taxes')
    amount = models.DecimalField(max_digits=10, decimal_places=2)




# class Discount(models.Model):
#     order = models.ForeignKey(Order, related_name='discounts', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#
# class Tax(models.Model):
#     order = models.ForeignKey(Order, related_name='taxes', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)