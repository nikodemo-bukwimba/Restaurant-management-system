from django.urls import path
from .views import user_login, ceo_dashboard, manager_dashboard, waiter_dashboard, waiter_detail_and_accept,load_more_orders
from orders import views as orders_views
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

app_name = 'users'

def root_redirect(request):
    return redirect('users:login')

urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('waiter/<int:id>/edit/', views.waiter_edit, name='waiter_edit'),
    path('waiter-history/', orders_views.waiter_history, name='waiter_history'),
    path('waiter/<int:waiter_id>/', waiter_detail_and_accept, name='waiter_detail_and_accept'),
    path('waiter/<int:id>/', views.waiter_detail, name='waiter_detail'),
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('ceo-dashboard/', ceo_dashboard, name='ceo_dashboard'),
    path('waiter-dashboard/', waiter_dashboard, name='waiter_dashboard'),
    path('load-more-orders/', load_more_orders, name='load_more_orders'),
    # Other URL patterns
]
