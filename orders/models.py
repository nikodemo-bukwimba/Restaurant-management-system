from django.db import models
from django.urls import reverse
from users.models import Waiter,Report
from django.utils.text import slugify
from users.models import Shift

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
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Keep only this slug field
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

from django.utils import timezone
class Expense(models.Model):
    waiter = models.ForeignKey('users.Waiter', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    shift = models.ForeignKey(Shift, null=True, blank=True, on_delete=models.SET_NULL)
    reports = models.ManyToManyField(Report, related_name='expenses', blank=True)
    time = models.TimeField(default=timezone.now)
    reported = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} - {self.description}"
