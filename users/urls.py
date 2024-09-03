# urls.py
from django.urls import path
from .views import user_login, ceo_dashboard, manager_dashboard, waiter_dashboard
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_login, name='login'),
    path('ceo-dashboard/', views.ceo_dashboard, name='ceo_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('waiter-dashboard/', views.waiter_dashboard, name='waiter_dashboard'),
    # Other URL patterns
]
