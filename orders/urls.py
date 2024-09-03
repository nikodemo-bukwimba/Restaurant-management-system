from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('menu_item_list/', views.menu_item_list, name='menu_item_list'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('user-orders/', views.user_orders, name='user_orders'),
    path('<slug:category_slug>/', views.menu_item_list, name='menu_item_list_by_category'),
    path('<int:id>/<slug:slug>/', views.menu_item_detail, name='menu_item_detail'),
    
]

