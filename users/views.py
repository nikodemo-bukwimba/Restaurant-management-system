# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Waiter, Manager, CEO
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Check if user is associated with one of the custom roles
                if Waiter.objects.filter(user=user).exists():
                    return redirect('orders:menu_item_list')
                elif Manager.objects.filter(user=user).exists():
                    return redirect('users:manager_dashboard')
                elif CEO.objects.filter(user=user).exists():
                    return redirect('users:ceo_dashboard')
                else:
                    form.add_error(None, 'User does not have an appropriate role.')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def ceo_dashboard(request):
    waiters = Waiter.objects.all()
    menu_items = MenuItem.objects.all()
    expenses = Expense.objects.all()
    orders = Order.objects.all()
    sales = Sales.objects.all()
    context = {
        'waiters': waiters,
        'menu_items': menu_items,
        'expenses': expenses,
        'orders': orders,
        'sales': sales,
    }
    return render(request, 'ceo_dashboard.html', context)

@login_required
def manager_dashboard(request):
    waiters_managed = Waiter.objects.filter(manager__user=request.user)
    orders = Order.objects.filter(waiter__manager__user=request.user)
    sales = Sales.objects.filter(waiter_sales__manager__user=request.user)
    context = {
        'waiters_managed': waiters_managed,
        'total_orders': orders.count(),
        'total_sales': sum(sale.total_sales for sale in sales),
    }
    return render(request, 'manager_dashboard.html', context)

@login_required
def waiter_dashboard(request):
    orders = Order.objects.filter(waiter__user=request.user)
    sales = Sales.objects.filter(waiter_sales__user=request.user)
    context = {
        'orders': orders,
        'sales': sales,
    }
    return render(request, 'orders/menu_item_list.html', context)
