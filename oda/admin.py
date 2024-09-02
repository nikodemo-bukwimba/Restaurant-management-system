# oda/admin.py
from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'get_total_cost')  # Add get_total_cost to display
    list_filter = ('created', 'updated')
    search_fields = ('user__username',)
    readonly_fields = ('created', 'updated')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'price', 'quantity', 'get_cost')  # Add get_cost to display
    list_filter = ('order', 'menu_item')
    search_fields = ('order__id', 'menu_item__name')
