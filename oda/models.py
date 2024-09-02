from django.db import models
from django.conf import settings
from users.models import Waiter, Manager, CEO
from orders.models import MenuItem

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user who placed the order
    waiter = models.ForeignKey(Waiter, null=True, blank=True, on_delete=models.SET_NULL)  # Waiter assigned to this order
    manager = models.ForeignKey(Manager, null=True, blank=True, on_delete=models.SET_NULL)  # Manager who placed the order
    ceo = models.ForeignKey(CEO, null=True, blank=True, on_delete=models.SET_NULL)  # CEO who placed the order
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
