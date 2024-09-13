from django.contrib import admin
from .models import Waiter, Manager, CEO, Shift

@admin.register(Waiter)
class WaiterAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']

@admin.register(CEO)
class CEOAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['waiter', 'start_time', 'end_time', 'completed']
    list_filter = ['completed', 'start_time']
    search_fields = ['waiter__name']

from .models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ['manager', 'created_at']  # Removed report_type, start_time, end_time
    list_filter = ['created_at']  # Removed report_type from filters

admin.site.register(Report, ReportAdmin)
