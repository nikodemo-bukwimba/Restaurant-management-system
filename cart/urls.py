from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:menu_item_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:menu_item_id>/', views.cart_remove, name='cart_remove'),
    # path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
]
