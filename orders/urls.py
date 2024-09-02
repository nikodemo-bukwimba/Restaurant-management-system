from django.urls import path
from . import views
from .views import custom_login, home

app_name = 'orders'

urlpatterns = [
    path('login/', custom_login, name='login'),
    path('', home, name='home'),
    path('', views.menu_item_list, name='menu_item_list'),
    path('user-orders/', views.user_orders, name='user_orders'),
    path('<slug:category_slug>/', views.menu_item_list, name='menu_item_list_by_category'),
    path('<int:id>/<slug:slug>/', views.menu_item_detail, name='menu_item_detail'),
]

