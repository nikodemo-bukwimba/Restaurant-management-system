from django.urls import path
from . import views
from .views import waiter_expenses, waiter_history

app_name = 'orders'  
app_name = 'expenses'

urlpatterns = [
    path('waiter/expenses/', waiter_expenses, name='waiter_expenses'),
    path('waiter-history/', waiter_history, name='waiter_history'),
    path('waiter-history/<int:waiter_id>/', views.waiter_history, name='waiter_history_with_id'),
    path('orders/update_payment_method/<int:order_id>/', views.update_payment_method, name='update_payment_method'),
    path('menu_item_list/', views.menu_item_list, name='menu_item_list'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('user-orders/', views.user_orders, name='user_orders'),
    path('<slug:category_slug>/', views.menu_item_list, name='menu_item_list_by_category'),
    path('<int:id>/<slug:slug>/', views.menu_item_detail, name='menu_item_detail'), 
]
