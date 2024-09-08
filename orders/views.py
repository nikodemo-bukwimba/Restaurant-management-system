from django.shortcuts import render, get_object_or_404
from .models import MenuCategory, MenuItem
from orders.models import MenuItem
from cart.forms import CartAddMenuItemForm
from oda.models import Order
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import Expense, Waiter  
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models.functions import ExtractMonth, ExtractYear
from users.models import Shift
from oda.models import Order
from .models import Expense

def menu_item_list(request, category_slug=None):
    category = None
    categories = MenuCategory.objects.all()
    menu_items = MenuItem.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(MenuCategory, slug=category_slug)
        menu_items = menu_items.filter(category=category)

    return render(request, 'orders/menu_item_list.html', {
        'category': category,
        'categories': categories,
        'menu_items': menu_items
    })

def menu_item_detail(request, id, slug):
    menu_item = get_object_or_404(MenuItem, id=id, slug=slug, available=True)
    cart_menu_item_form = CartAddMenuItemForm()
    
    return render(request, 'orders/menu_item_detail.html',  {'menu_item': menu_item, 'cart_menu_item_form': cart_menu_item_form})


@login_required
def user_orders(request):
    today = timezone.now().date()

    try:
        waiter = Waiter.objects.get(user=request.user)
    except Waiter.DoesNotExist:
        return render(request, '404.html', {'message': 'Waiter not found.'})

    shift = Shift.objects.filter(waiter=waiter, completed=False).last()

    if shift:
        # Fetch orders created by the waiter directly (user matches, assigned_waiter is null)
        orders_created_by_waiter = Order.objects.filter(user=request.user, shift=shift, assigned_waiter__isnull=True)

        # Fetch orders assigned to the waiter
        orders_assigned_to_waiter = Order.objects.filter(assigned_waiter=waiter, shift=shift)

        # Combine both querysets
        orders = orders_created_by_waiter | orders_assigned_to_waiter
        orders = orders.order_by('-created')
    else:
        orders = Order.objects.none()

    total_sales = sum(order.get_total_cost() for order in orders)
    total_phone_payments = sum(order.get_total_cost() for order in orders if order.payment_method == 'phone')

    total_expenses = Expense.objects.filter(waiter=waiter, date=today).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    amount_to_submit = total_sales - total_expenses - total_phone_payments
    has_phone_payments = orders.filter(payment_method='phone').exists()

    context = {
        'orders': orders,
        'total_sales': total_sales,
        'total_phone_payments': total_phone_payments,
        'total_expenses': total_expenses,
        'amount_to_submit': amount_to_submit,
        'has_phone_payments': has_phone_payments,
        'shift': shift,
    }

    return render(request, 'orders/user_orders.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.waiter = request.user.waiter  # Link expense to the logged-in waiter
            expense.save()
            # Optionally update the waiter's total sales here
            return redirect('orders:menu_item_list')  # Redirect to a relevant page
    else:
        form = ExpenseForm()
    return render(request, 'orders/add_expense.html', {'form': form})

@login_required
def waiter_expenses(request):
    # Retrieve the Waiter instance associated with the current user
    try:
        waiter = Waiter.objects.get(user=request.user)
    except Waiter.DoesNotExist:
        # Handle the case where the Waiter instance does not exist
        return render(request, 'orders/waiter_expenses.html', {'expenses': [], 'total_expenses': 0})

    # Fetch expenses related to the waiter
    expenses = Expense.objects.filter(waiter=waiter)
    
    # Calculate total expenses
    total_expenses = expenses.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
    }
    return render(request, 'orders/waiter_expenses.html', context)

def update_payment_method(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        sender_name = request.POST.get('sender_name', '')  # Default to empty if not provided
        
        if payment_method not in ['cash', 'credit_card', 'phone']:
            return HttpResponseBadRequest("Invalid payment method")

        # Update payment method and sender name
        order.payment_method = payment_method
        if payment_method == 'phone':
            order.sender_name = sender_name
        else:
            order.sender_name = ''
        order.save()

        # Redirect to the orders page or another page
        return redirect('orders:user_orders')  # Adjust the redirect as needed
    
    # Handle the case where the request method is not POST
    return HttpResponseBadRequest("Invalid request method")

@login_required
def waiter_history(request, waiter_id=None):
    if waiter_id:
        try:
            waiter = Waiter.objects.get(id=waiter_id)
        except Waiter.DoesNotExist:
            return render(request, 'orders/waiter_history.html', {'error': 'Waiter not found.'})
    else:
        try:
            waiter = request.user.waiter
        except AttributeError:
            if request.user.is_manager:
                waiter = None
            else:
                return render(request, 'orders/waiter_history.html', {'error': 'No waiter profile found for this user.'})

    # Aggregate orders by month and year
    if waiter:
        aggregated_orders = (
            Order.objects.filter(
                Q(user=waiter.user) | Q(assigned_waiter=waiter)
            )
            .annotate(month=ExtractMonth('created'), year=ExtractYear('created'))
            .values('month', 'year')
            .annotate(total_cost=Sum('total_cost'))
            .order_by('year', 'month')
        )
        
        orders_details = (
            Order.objects.filter(
                Q(user=waiter.user) | Q(assigned_waiter=waiter)
            )
            .prefetch_related('items__menu_item')  # Efficiently fetch related items
            .values('created', 'id', 'total_cost', 'payment_method')
            .order_by('created')
        )

        aggregated_expenses = (
            Expense.objects.filter(waiter=waiter)
            .annotate(month=ExtractMonth('date'), year=ExtractYear('date'))
            .values('month', 'year')
            .annotate(total_amount=Sum('amount'))
            .order_by('year', 'month')
        )

        expenses_details = (
            Expense.objects.filter(waiter=waiter)
            .values('date', 'amount', 'description')
            .order_by('date')
        )

    else:
        aggregated_orders = (
            Order.objects.filter(
                Q(assigned_waiter__isnull=False)
            )
            .annotate(month=ExtractMonth('created'), year=ExtractYear('created'))
            .values('month', 'year')
            .annotate(total_cost=Sum('total_cost'))
            .order_by('year', 'month')
        )

        orders_details = (
            Order.objects.filter(
                Q(assigned_waiter__isnull=False)
            )
            .prefetch_related('items__menu_item')  # Efficiently fetch related items
            .values('created', 'id', 'total_cost', 'payment_method')
            .order_by('created')
        )

        aggregated_expenses = (
            Expense.objects.all()
            .annotate(month=ExtractMonth('date'), year=ExtractYear('date'))
            .values('month', 'year')
            .annotate(total_amount=Sum('amount'))
            .order_by('year', 'month')
        )

        expenses_details = (
            Expense.objects.all()
            .values('date', 'amount', 'description')
            .order_by('date')
        )

    paginator_orders = Paginator(orders_details, 10)
    page_number_orders = request.GET.get('page_orders')
    page_obj_orders = paginator_orders.get_page(page_number_orders)

    paginator_expenses = Paginator(expenses_details, 10)
    page_number_expenses = request.GET.get('page_expenses')
    page_obj_expenses = paginator_expenses.get_page(page_number_expenses)

    trend_data = []
    previous_total = None

    for order in aggregated_orders:
        current_total = order['total_cost']
        if previous_total is not None:
            change = (current_total - previous_total) / previous_total * 100
            trend_data.append({
                'month': order['month'],
                'year': order['year'],
                'total_cost': current_total,
                'change': change
            })
        else:
            trend_data.append({
                'month': order['month'],
                'year': order['year'],
                'total_cost': current_total,
                'change': None
            })
        previous_total = current_total

    context = {
        'aggregated_orders': aggregated_orders,
        'aggregated_expenses': aggregated_expenses,
        'page_obj_orders': page_obj_orders,
        'page_obj_expenses': page_obj_expenses,
        'trend_data': trend_data,
    }

    return render(request, 'orders/waiter_history.html', context)

