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
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

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

def user_orders(request):
    today = timezone.now().date()
    
    # Get the waiter object linked to the current user
    waiter = Waiter.objects.get(user=request.user)
    
    # Fetch all orders for today for the logged-in user (waiter)
    orders = Order.objects.filter(user=request.user, created__date=today).order_by('-created')
    
    # Calculate total sales for today's orders
    total_sales = sum(order.get_total_cost() for order in orders)
    
    # Calculate total phone payments (since phone payments go directly to the company)
    total_phone_payments = sum(order.get_total_cost() for order in orders if order.payment_method == 'phone')
    
    # Calculate total expenses for today for this waiter
    total_expenses = Expense.objects.filter(waiter=waiter, date=today).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # Calculate the amount to submit (total sales - total expenses - total phone payments)
    amount_to_submit = total_sales - total_expenses - total_phone_payments
    
    return render(request, 'orders/user_orders.html', {
        'orders': orders,
        'total_sales': total_sales,
        'total_phone_payments': total_phone_payments,
        'total_expenses': total_expenses,
        'amount_to_submit': amount_to_submit,
    })


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
        order.payment_method = payment_method
        order.save()
        return redirect('orders:user_orders')  # or any other view
    return redirect('orders:user_orders')  # Handle GET requests if needed
