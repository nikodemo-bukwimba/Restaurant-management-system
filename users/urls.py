from django.urls import path
from .views import user_login, ceo_dashboard, manager_dashboard, waiter_dashboard, waiter_detail_and_accept
from orders import views as orders_views

app_name = 'users'

urlpatterns = [
    path('', user_login, name='login'),
    path('waiter-history/', orders_views.waiter_history, name='waiter_history'),
    path('waiter/<int:waiter_id>/', waiter_detail_and_accept, name='waiter_detail_and_accept'),
    # path('order/<int:order_id>/confirm/', confirm_order_payment, name='confirm_order_payment'),
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('ceo-dashboard/', ceo_dashboard, name='ceo_dashboard'),
    path('waiter-dashboard/', waiter_dashboard, name='waiter_dashboard'),
    # Other URL patterns
]
