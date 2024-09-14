from django.contrib import admin
from .models import MenuCategory, MenuItem

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'customer_price', 'staff_price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['customer_price', 'staff_price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    search_fields = ['name', 'description']

from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('waiter', 'amount', 'description', 'date', 'shift', 'reported')
    list_filter = ('waiter', 'date', 'shift', 'reported')
    search_fields = ('description',)