# oda/admin.py
from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'get_total_cost', 'sender_name', 'manager_confirmed')
    list_filter = ('created', 'updated', 'payment_method', 'manager_confirmed')
    search_fields = ('user__username', 'sender_name')
    readonly_fields = ('created', 'updated')
    
    # Optionally customize the form layout in the admin interface
    fields = ('user', 'created', 'updated', 'payment_method', 'sender_name', 'manager_confirmed', 'get_total_cost')
    # If you don't want some fields to be editable
    # readonly_fields = ('created', 'updated', 'get_total_cost')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'price', 'quantity', 'get_cost')  # Add get_cost to display
    list_filter = ('order', 'menu_item')
    search_fields = ('order__id', 'menu_item__name')
