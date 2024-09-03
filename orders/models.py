from django.db import models
from django.urls import reverse
from users.models import Waiter 


class MenuCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'menu category'
        verbose_name_plural = 'menu categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('orders:menu_item_list_by_category', args=[self.slug])

class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='menu_items/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    customer_price = models.DecimalField(max_digits=20, decimal_places=2)
    staff_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('orders:menu_item_detail', args=[self.id, self.slug])

class Expense(models.Model):
    waiter = models.ForeignKey('users.Waiter', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Expense by {self.waiter.name} on {self.date}"
        return f"{self.amount} - {self.description}"

