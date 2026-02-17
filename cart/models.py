from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)  # Or link to Product if you have one
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(default=timezone.now)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.item_name} ({self.quantity})"
