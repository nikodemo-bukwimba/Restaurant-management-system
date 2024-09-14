from django.contrib import admin
from .models import Order, OrderItem
from users.models import Waiter

# Custom admin form for Order
from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'created': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
            'updated': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
        }

def mark_as_confirmed(modeladmin, request, queryset):
    queryset.update(manager_confirmed=True)
mark_as_confirmed.short_description = "Mark selected orders as confirmed"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'get_total_cost', 'payment_method', 'sender_name', 'manager_confirmed', 'assigned_waiter', 'shift', 'reported')
    list_filter = ('created', 'updated', 'payment_method', 'manager_confirmed', 'assigned_waiter', 'shift')
    search_fields = ('user__username', 'sender_name', 'assigned_waiter__name')
    readonly_fields = ('created', 'updated')
    fields = ('user', 'created', 'updated', 'total_cost', 'payment_method', 'sender_name', 'manager_confirmed', 'assigned_waiter', 'shift', 'reported')
    form = OrderForm
    actions = [mark_as_confirmed]

    def get_total_cost(self, obj):
        return obj.get_total_cost()
    get_total_cost.admin_order_field = 'total_cost'
    get_total_cost.short_description = 'Total Cost'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'price', 'quantity', 'get_cost')
    list_filter = ('order', 'menu_item')
    search_fields = ('order__id', 'menu_item__name')

    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.admin_order_field = 'price'
    get_cost.short_description = 'Cost'
