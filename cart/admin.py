from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item_name', 'quantity', 'price', 'total_price', 'added_on')
    list_filter = ('user', 'added_on')
    search_fields = ('user__username', 'item_name')
    ordering = ('-added_on',)
