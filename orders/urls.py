from django.urls import path
from . import views
from .views import waiter_expenses, waiter_history
# from .views import generate_manager_report
from .views import add_menu_item
from .views import detailed_sales_report

app_name = 'orders'  
app_name = 'expenses'

urlpatterns = [
    path('generate_report/', views.generate_manager_report_view, name='generate_manager_report'),

    path('generate_report/', views.generate_manager_report, name='generate_manager_report'),
    path('save_report/', views.save_manager_report, name='save_manager_report'),
    path('download_report/', views.download_manager_report_pdf, name='download_manager_report_pdf'),
    # path('generate-report/<str:report_type>/', views.generate_manager_report, name='generate_manager_report'),
    # Menu item detail
    path('menu-item/<int:id>/<slug:slug>/', views.menu_item_detail, name='menu_item_detail'),
    
    # List all menu items
    path('menu-item-list/', views.menu_item_list, name='menu_item_list'),
    
    # List menu items by category slug
    path('category/<slug:category_slug>/', views.menu_item_list, name='menu_item_list_by_category'),
    
    # Manage waiters
    path('manage-waiters/', views.manage_waiters, name='manage_waiters'),
    
    # Detailed sales report
    path('detailed-sales-report/', views.detailed_sales_report, name='detailed_sales_report'),
    
    # Waiter expenses
    path('waiter/expenses/', views.waiter_expenses, name='waiter_expenses'),
    
    # Generate report
    # path('generate-report/<str:report_type>/', views.generate_manager_report, name='generate_manager_report'),
    
    # Download report as PDF
    # path('download-report/', views.download_manager_report_pdf, name='download_manager_report_pdf'),
    
    # Waiter history
    path('waiter-history/', views.waiter_history, name='waiter_history'),
    path('waiter-history/<int:waiter_id>/', views.waiter_history, name='waiter_history_with_id'),
    
    # Update payment method
    path('orders/update_payment_method/<int:order_id>/', views.update_payment_method, name='update_payment_method'),
    
    # Add expense
    path('add-expense/', views.add_expense, name='add_expense'),
    
    # User orders
    path('user-orders/', views.user_orders, name='user_orders'),
    
    # URL pattern for menu items by category ID (consider if needed)
    path('menu-items/<int:category_id>/', views.menu_item_list, name='menu_item_list_by_category_id'),

    path('add-menu-item/', views.add_menu_item, name='add_menu_item'),
    
    # The last URL pattern is redundant with the earlier category slug pattern
    # path('<slug:category_slug>/', views.menu_item_list, name='menu_item_list_by_category'),
]
