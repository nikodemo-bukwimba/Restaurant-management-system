from django.contrib import admin
from .models import Waiter, Manager, CEO

@admin.register(Waiter)
class WaiterAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']

@admin.register(CEO)
class CEOAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
