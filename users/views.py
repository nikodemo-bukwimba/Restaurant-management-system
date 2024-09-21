# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Waiter, Manager, CEO
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from oda.models import Order, Waiter, Manager, CEO,OrderItem
from orders.models import Expense
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import  Shift
from django.utils import timezone
from django.db import models
from decimal import Decimal
from orders.models import MenuItem
from django.http import HttpResponseBadRequest
from .forms import WaiterForm

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

    # Get all waiters managed by this manager
    waiters_managed = Waiter.objects.filter(manager=manager)

    # Get the active shifts for these waiters
    active_shifts = Shift.objects.filter(waiter__in=waiters_managed, completed=False)

    # Filter orders that belong to these waiters and are in the active shift
    orders = Order.objects.filter(shift__in=active_shifts)

    # Calculate total sales from the orders within the active shift
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

    # Example data for charts and tables (replace with actual calculations and queries)
    total_sales = orders.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    recent_orders = orders.order_by('-created')[:10]  # Fetch recent 10 orders
    top_waiters = (
        Waiter.objects
        .annotate(total_sales=Sum('order__total_cost'))
        .order_by('-total_sales')[:10]  # Top 5 waiters by sales
    )

    context = {
        'waiters': waiters,
        'menu_items': menu_items,
        'expenses': expenses,
        'orders': orders,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
        'top_waiters': top_waiters,
        'is_ceo': True,
        'is_manager': False,
    }
    return render(request, 'users/ceo_dashboard.html', context)

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
    now = timezone.now()

    # Get the active shift (shift with no end time)
    shift = Shift.objects.filter(waiter=waiter, end_time__isnull=True).last()

    if request.method == 'POST':
        if 'accept_sales' in request.POST and shift:
            shift.completed = True
            shift.end_time = now
            shift.save()

            # Create a new shift for the waiter
            new_shift = Shift(waiter=waiter, start_time=now)
            new_shift.save()

            return redirect('users:manager_dashboard')

        elif 'update_payment' in request.POST:
            order_id = request.POST.get('update_payment')
            try:
                order = Order.objects.get(id=order_id)
                payment_method = request.POST.get(f'payment_method_{order.id}')
                order.payment_method = payment_method

                if payment_method == 'phone':
                    sender_name = request.POST.get(f'sender_name_{order.id}', '')
                    order.sender_name = sender_name

                order.save()
            except Order.DoesNotExist:
                return HttpResponseBadRequest("Order not found.")

        elif 'confirm_order' in request.POST:
            order_id = request.POST.get('confirm_order')
            try:
                order = Order.objects.get(id=order_id)
                order.manager_confirmed = True
                order.save()
            except Order.DoesNotExist:
                return HttpResponseBadRequest("Order not found.")

    if shift:
        # Fetch orders created by the waiter directly (user matches, assigned_waiter is null)
        orders_created_by_waiter = Order.objects.filter(
            user=waiter.user, shift=shift, assigned_waiter__isnull=True
        )

        # Fetch orders assigned to the waiter
        orders_assigned_to_waiter = Order.objects.filter(
            assigned_waiter=waiter, shift=shift
        )

        # Combine both querysets
        orders = orders_created_by_waiter | orders_assigned_to_waiter
        orders = orders.order_by('-created')

        total_sales = sum(order.get_total_cost() for order in orders)
        total_phone_payments = sum(order.get_total_cost() for order in orders if order.payment_method == 'phone')

        # Total expenses for the active shift
        if shift.completed:
    # For completed shifts (simplified)
            total_expenses = Expense.objects.filter(waiter=waiter,shift=shift).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        else:
    # For ongoing shifts (simplified)
            total_expenses = Expense.objects.filter(waiter=waiter,shift=shift).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        amount_to_submit = total_sales - total_expenses - total_phone_payments
        has_phone_payments = orders.filter(payment_method='phone').exists()
    else:
        orders = Order.objects.none()
        total_sales = Decimal('0.00')
        total_phone_payments = Decimal('0.00')
        total_expenses = Decimal('0.00')
        amount_to_submit = Decimal('0.00')
        has_phone_payments = False

    context = {
        'waiter': waiter,
        'shift': shift,
        'orders': orders,
        'total_sales': total_sales,
        'total_phone_payments': total_phone_payments,
        'total_expenses': total_expenses,
        'amount_to_submit': amount_to_submit,
        'has_phone_payments': has_phone_payments,
    }

    return render(request, 'users/waiter_detail_and_accept.html', context)

def waiter_detail(request, id):
    waiter = get_object_or_404(Waiter, id=id)
    return render(request, 'users/waiter_detail.html', {'waiter': waiter})


def waiter_edit(request, id):
    waiter = get_object_or_404(Waiter, id=id)
    if request.method == 'POST':
        form = WaiterForm(request.POST, instance=waiter)
        if form.is_valid():
            form.save()
            return redirect('orders:manage_waiters')  # or any other URL you want to redirect to
    else:
        form = WaiterForm(instance=waiter)
    
    return render(request, 'users/waiter_edit.html', {'form': form, 'waiter': waiter})

