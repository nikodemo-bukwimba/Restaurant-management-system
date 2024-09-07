# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Waiter, Manager, CEO
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from oda.models import Order, Waiter, Manager, CEO
from orders.models import Expense
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import  Shift
from django.utils import timezone
from django.db import models
from decimal import Decimal

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
def manager_dashboard(request):
    try:
        manager = Manager.objects.get(user=request.user)
    except Manager.DoesNotExist:
        return render(request, 'users/manager_dashboard.html', {'error': 'Manager profile not found.'})

    waiters_managed = Waiter.objects.filter(manager=manager)
    orders = Order.objects.filter(user__in=waiters_managed.values_list('user', flat=True))
    total_sales = orders.aggregate(total_sales=Sum('total_cost'))['total_sales'] or 0

    context = {
        'waiters_managed': waiters_managed,
        'total_orders': orders.count(),
        'total_sales': total_sales,
        'is_manager': True,
        'is_ceo': False,
    }
    return render(request, 'users/manager_dashboard.html', context)


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
        'is_ceo': True,  # Pass this to help display the dashboard link
        'is_manager': False,
    }
    return render(request, 'ceo_dashboard.html', context)

@login_required
def waiter_dashboard(request):
    orders = Order.objects.filter(waiter__user=request.user)
    sales = Sales.objects.filter(waiter_sales__user=request.user)
    context = {
        'orders': orders,
        'sales': sales,
    }
    return render(request, 'orders/menu_item_list.html', context)

@login_required
def waiter_detail_and_accept(request, waiter_id):
    waiter = get_object_or_404(Waiter, id=waiter_id)
    today = timezone.now().date()
    shift = Shift.objects.filter(waiter=waiter, completed=False).last()

    if request.method == 'POST':
        if 'accept_sales' in request.POST and shift:
            # End the current shift
            shift.completed = True
            shift.end_time = timezone.now()
            shift.save()

            # Create a new shift
            new_shift = Shift(waiter=waiter, start_time=timezone.now())
            new_shift.save()

            return redirect('users:manager_dashboard')  # Redirect after accepting sales

    if shift:
        # Include orders where the waiter is either the assigned waiter or the order creator (user)
        orders = Order.objects.filter(
            shift=shift
        ).filter(
            models.Q(assigned_waiter=waiter) | models.Q(user=waiter.user)
        )
    else:
        orders = Order.objects.none()  # No active shift

    # Calculate financial details for this shift
    total_sales = sum(order.get_total_cost() for order in orders)
    total_phone_payments = sum(order.get_total_cost() for order in orders if order.payment_method == 'phone')
    total_expenses = Expense.objects.filter(waiter=waiter, date=today).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    amount_to_submit = total_sales - total_expenses - total_phone_payments
    has_phone_payments = orders.filter(payment_method='phone').exists()

    return render(request, 'users/waiter_detail_and_accept.html', {
        'waiter': waiter,
        'orders': orders,
        'shift': shift,
        'total_sales': total_sales,
        'total_phone_payments': total_phone_payments,
        'total_expenses': total_expenses,
        'amount_to_submit': amount_to_submit,
        'has_phone_payments': has_phone_payments,
    })

