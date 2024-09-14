from django.db import models
from django.conf import settings
from users.models import Waiter, Manager, CEO, Shift
from orders.models import MenuItem

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('phone', 'Phone'),
    ], default='cash')
    sender_name = models.CharField(max_length=100, blank=True, null=True)
    manager_confirmed = models.BooleanField(default=False)
    assigned_waiter = models.ForeignKey(Waiter, null=True, blank=True, on_delete=models.SET_NULL)
    shift = models.ForeignKey(Shift, null=True, blank=True, on_delete=models.SET_NULL) 
    reported = models.BooleanField(default=False)

    def get_total_cost(self):
        return self.total_cost

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
