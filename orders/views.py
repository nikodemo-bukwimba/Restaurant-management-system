from django.shortcuts import render, get_object_or_404
from .models import MenuCategory, MenuItem
from orders.models import MenuItem
from cart.forms import CartAddMenuItemForm
from oda.models import Order
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .forms import ExpenseForm
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
from django.contrib import messages
from .forms import ExpenseForm , ExpenseFormForManager 
from users.models import Manager,Report
from .forms import MenuItemForm 
from io import BytesIO

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
    
    # Assuming your cart is stored in the session
    cart = request.session.get('cart', {})  # Adjust based on your cart implementation
    item_in_cart = menu_item.id in cart.get('items', [])  # Check if item ID is in cart items

    return render(request, 'orders/menu_item_detail.html', {
        'menu_item': menu_item,
        'cart_menu_item_form': cart_menu_item_form,
        'item_in_cart': item_in_cart,  # Pass this to the template
    })

@login_required
def user_orders(request):
    now = timezone.now()

    try:
        waiter = Waiter.objects.get(user=request.user)
    except Waiter.DoesNotExist:
        return render(request, '404.html', {'message': 'Waiter not found.'})

    # Get the active shift for the waiter
    shift = Shift.objects.filter(waiter=waiter, completed=False).last()

    if shift:
        # Fetch orders created by the waiter directly (user matches, assigned_waiter is null)
        orders_created_by_waiter = Order.objects.filter(user=request.user, shift=shift, assigned_waiter__isnull=True)

        # Fetch orders assigned to the waiter
        orders_assigned_to_waiter = Order.objects.filter(assigned_waiter=waiter, shift=shift)

        # Combine both querysets
        orders = orders_created_by_waiter | orders_assigned_to_waiter
        orders = orders.order_by('-created')

        # Calculate total sales and phone payments
        total_sales = sum(order.get_total_cost() for order in orders)
        total_phone_payments = sum(order.get_total_cost() for order in orders if order.payment_method == 'phone')

        # Filter expenses by the active shift
        if shift.completed:
    # For completed shifts (simplified)
            total_expenses = Expense.objects.filter(waiter=waiter,shift=shift).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        else:
    # For ongoing shifts (simplified)
            total_expenses = Expense.objects.filter(waiter=waiter,shift=shift).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        # Calculate the amount to submit
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
    else:
        # No active shift found
        context = {
            'orders': Order.objects.none(),
            'total_sales': Decimal('0.00'),
            'total_phone_payments': Decimal('0.00'),
            'total_expenses': Decimal('0.00'),
            'amount_to_submit': Decimal('0.00'),
            'has_phone_payments': False,
            'shift': None,
        }

    return render(request, 'orders/user_orders.html', context)


@login_required
def add_expense(request):
    try:
        # Check if the user is a manager
        manager = Manager.objects.get(user=request.user)
        is_manager = True
    except Manager.DoesNotExist:
        is_manager = False

    if is_manager:
        # Manager-specific logic
        if request.method == 'POST':
            form = ExpenseFormForManager(request.POST)
            if form.is_valid():
                expense = form.save(commit=False)
                waiter = form.cleaned_data.get('waiter')

                if waiter:  # If the waiter is assigned
                    # Fetch the latest active shift for the selected waiter
                    shift = Shift.objects.filter(waiter=waiter, end_time__isnull=True).last()

                    if not shift:
                        messages.error(request, "The selected waiter does not have an active shift.")
                        return redirect('orders:add_expense')

                    # Calculate total cash sales for the active shift
                    total_cash_sales = Order.objects.filter(
                        shift=shift,
                        payment_method='cash'
                    ).aggregate(
                        total_sales=Sum('total_cost')
                    )['total_sales'] or Decimal('0.00')

                    # Get total existing expenses for the current shift
                    existing_expenses = Expense.objects.filter(
                        waiter=waiter,
                        shift=shift,
                        date=expense.date
                    ).aggregate(
                        total_expenses=Sum('amount')
                    )['total_expenses'] or Decimal('0.00')

                    # Calculate the remaining cash available for expenses
                    remaining_cash = total_cash_sales - existing_expenses

                    if remaining_cash <= 0:
                        messages.error(request, "Hakuna pesa taslimu inayopatikana kwa matumizi zaidi!!.")
                        return redirect('orders:add_expense')

                    # Check if the new expense exceeds the remaining cash
                    if expense.amount > remaining_cash:
                        messages.error(request, f"Kiwango cha juu kinachoruhusiwa kwa matumizi ni Tsh.{remaining_cash}.")
                        return redirect('orders:add_expense')

                    # Save the expense and assign to the waiter and shift
                    expense.waiter = waiter
                    expense.shift = shift

                else:  # If no waiter is assigned, treat as manager's expense
                    expense.waiter = None  # No waiter assigned
                    expense.manager = manager  # Assign to the manager

                expense.save()
                messages.success(request, "Matumizi yamewekwa kikamilifu.")
                return redirect('orders:menu_item_list')
        else:
            form = ExpenseFormForManager()  # Form for managers with waiter selection
    else:
        # Waiter-specific logic
        try:
            waiter = request.user.waiter
        except Waiter.DoesNotExist:
            messages.error(request, "Wewe sio mhudumu. Tafadhali wasiliana na meneja wako.")
            return redirect('orders:menu_item_list')

        if request.method == 'POST':
            form = ExpenseForm(request.POST, manager=None)
            if form.is_valid():
                expense = form.save(commit=False)

                # Fetch the latest active shift for the current waiter
                shift = Shift.objects.filter(waiter=waiter, end_time__isnull=True).last()

                if not shift:
                    messages.error(request, "Huna zamu inayoendelea.")
                    return redirect('orders:add_expense')

                # Calculate total cash sales for the active shift
                total_cash_sales = Order.objects.filter(
                    shift=shift,
                    payment_method='cash'
                ).aggregate(
                    total_sales=Sum('total_cost')
                )['total_sales'] or Decimal('0.00')

                # Get total existing expenses for the current shift
                existing_expenses = Expense.objects.filter(
                    waiter=waiter,
                    shift=shift,
                    date=expense.date
                ).aggregate(
                    total_expenses=Sum('amount')
                )['total_expenses'] or Decimal('0.00')

                # Calculate remaining cash for expenses
                remaining_cash = total_cash_sales - existing_expenses

                if remaining_cash <= 0:
                    messages.error(request, "Huna mauzo ya pesa taslimu yaliyopo kwa matumizi zaidi.")
                    return redirect('orders:add_expense')

                # Ensure the expense doesn't exceed remaining cash
                if expense.amount > remaining_cash:
                    messages.error(request, f"Kiwango cha juu kinachoruhusiwa kwa matumizi ni Tsh.{remaining_cash}.")
                    return redirect('orders:add_expense')

                # Save the expense and assign to the waiter and shift
                expense.waiter = waiter
                expense.shift = shift
                expense.save()
                messages.success(request, "Matumizi yamefanyika kikamilifu.")
                return redirect('orders:menu_item_list')
        else:
            form = ExpenseForm(manager=None)  # Form for waiters without waiter selection

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

from django.urls import reverse

@login_required
def generate_manager_report(request):
    today = timezone.now().date()

    # Fetch the current manager
    try:
        manager = Manager.objects.get(user=request.user)
    except Manager.DoesNotExist:
        return {'error': 'Manager not found'}

    # Get all waiters managed by this manager
    waiters_managed = Waiter.objects.filter(manager=manager)

    # Get all completed shifts for today
    shifts = Shift.objects.filter(waiter__in=waiters_managed, completed=True)

    # Fetch only orders that have not been included in any report yet
    unreported_orders = Order.objects.filter(shift__in=shifts, reported=False)

    # Aggregate totals for sales and phone payments
    total_sales = unreported_orders.aggregate(total_sales=Sum('total_cost'))['total_sales'] or Decimal('0.00')
    total_phone_payments = unreported_orders.filter(payment_method='phone').aggregate(
        total=Sum('total_cost'))['total'] or Decimal('0.00')
    # Fetch all expenses related to closed shifts, excluding previously reported expenses
    total_expenses = Expense.objects.filter(
        waiter__in=waiters_managed,shift__in=shifts,reported=False).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Calculate the amount to submit to the CEO
    amount_to_submit = total_sales - total_expenses - total_phone_payments

    # Create context
    context = {
        'orders_by_waiter': {waiter: unreported_orders.filter(shift__waiter=waiter) for waiter in waiters_managed},
        'total_sales': total_sales,
        'total_phone_payments': total_phone_payments,
        'total_expenses': total_expenses,
        'amount_to_submit': amount_to_submit,
        'expenses': Expense.objects.filter(
            waiter__in=waiters_managed,
            shift__in=shifts,reported=False)
    }

    return context


@login_required
def generate_manager_report_view(request):
    context = generate_manager_report(request)  # This should return a dictionary

    if isinstance(context, dict) and 'error' not in context:
        return render(request, 'orders/manager_report.html', context)  # Render it as HTML and return HttpResponse
    else:
        # Handle the error if the context contains an error message or is not a dict
        return HttpResponse('Error generating report', status=500)


from django.contrib.auth.decorators import login_required
from users.models import Report
from django.db.models import Count

@login_required
def save_manager_report(request):
    if request.method == 'POST':
        today = timezone.now().date()

        # Get the current manager and managed waiters
        try:
            manager = Manager.objects.get(user=request.user)
        except Manager.DoesNotExist:
            return render(request, '404.html', {'message': 'Manager not found.'})

        waiters_managed = Waiter.objects.filter(manager=manager)

        # Get all completed shifts for today
        shifts = Shift.objects.filter(waiter__in=waiters_managed, completed=True)

        # Fetch only orders that have not been included in any report yet
        unreported_orders = Order.objects.filter(shift__in=shifts, reported=False)

        # Aggregate totals for sales and phone payments
        total_sales = unreported_orders.aggregate(total_sales=Sum('total_cost'))['total_sales'] or Decimal('0.00')
        total_phone_payments = unreported_orders.filter(payment_method='phone').aggregate(
            total=Sum('total_cost'))['total'] or Decimal('0.00')

        # Get IDs of expenses already included in previous reports
        previous_reports = Report.objects.filter(manager=request.user).values_list('report_data', flat=True)
        previous_expense_ids = []

        for report_data in previous_reports:
            if isinstance(report_data, dict):
                previous_expense_ids.extend(report_data.get('expenses', []))

        # Fetch all unreported expenses related to the closed shifts
        unreported_expenses = Expense.objects.filter(
            waiter__in=waiters_managed, 
            shift__in=shifts,
            reported=False  # Ensure you only include unreported expenses
        )

        # Aggregate total expenses for the report
        total_expenses = unreported_expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        # Calculate the amount to submit to the CEO
        amount_to_submit = total_sales - total_expenses - total_phone_payments

        # Create the report data
        report_data = {
            'total_sales': str(total_sales),
            'total_phone_payments': str(total_phone_payments),
            'total_expenses': str(total_expenses),
            'amount_to_submit': str(amount_to_submit),
            'expenses': list(unreported_expenses.values_list('id', flat=True)),  # Include the expense IDs in the report
            'orders_by_waiter': {
                waiter.id: list(unreported_orders.filter(assigned_waiter=waiter).values_list('id', flat=True))
                for waiter in waiters_managed
            }
        }

        # Check if the report data is meaningful
        if total_sales == Decimal('0.00') and total_expenses == Decimal('0.00') and total_phone_payments == Decimal('0.00'):
            messages.error(request, 'No content to save. Report contains no data.')
            return redirect('orders:generate_manager_report')  # Redirect back if the report is empty

        # Create or update the Report object
        report = Report.objects.create(
            manager=request.user,
            report_data=report_data
        )

        # Mark the included orders and expenses as reported
        unreported_orders.update(reported=True)
        unreported_expenses.update(reported=True)  # Mark the expenses as reported as well

        # Add a success message
        messages.success(request, 'Report has been successfully saved!')

        return redirect('orders:view_saved_report', report_id=report.id)  # Redirect to the saved report view

    return render(request, '404.html', {'message': 'Invalid request method.'})


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from weasyprint import HTML
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required

@login_required
def download_manager_report_pdf(request, report_id):
    # Retrieve the report
    report = get_object_or_404(Report, id=report_id)
    
    # Extract data from the report
    report_data = report.report_data
    total_sales = report_data.get('total_sales', 0)
    total_phone_payments = report_data.get('total_phone_payments', 0)
    total_expenses = report_data.get('total_expenses', 0)
    amount_to_submit = report_data.get('amount_to_submit', 0)
    expenses_ids = report_data.get('expenses', [])
    orders_by_waiter_data = report_data.get('orders_by_waiter', {})
    
    # Fetch detailed expense data
    expense_details = Expense.objects.filter(id__in=expenses_ids)
    
    # Fetch detailed order data and filter out waiters with no orders
    orders_by_waiter = {}
    for waiter_id, order_ids in orders_by_waiter_data.items():
        if order_ids:  # Only include waiters with orders
            waiter = Waiter.objects.get(id=waiter_id)
            orders = Order.objects.filter(id__in=order_ids)
            if orders.exists():  # Ensure the waiter has orders
                orders_by_waiter[waiter] = orders
    
    # Prepare the context for the PDF
    context = {
        'report': report,
        'total_sales': total_sales,
        'total_phone_payments': total_phone_payments,
        'total_expenses': total_expenses,
        'amount_to_submit': amount_to_submit,
        'orders_by_waiter': orders_by_waiter,
        'expenses': expense_details
    }
    
    # Load the template
    template = get_template('orders/pdf_report.html')
    html_content = template.render(context)
    
    # Create PDF
    pdf = HTML(string=html_content).write_pdf()
    
    # Prepare response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="manager_report_{report_id}.pdf"'
    
    return response


#View saved report list
def view_report_list(request):
    # Retrieve all reports from the database
    reports = Report.objects.all()
    # Pass the reports to the template
    return render(request, 'orders/report_list.html', {'reports': reports})

@login_required
def view_saved_report(request, report_id):
    # Retrieve a specific report by its ID
    report = get_object_or_404(Report, id=report_id)
    
    # Extract necessary data from report_data JSON
    report_data = report.report_data
    total_sales = report_data.get('total_sales', 0)
    total_phone_payments = report_data.get('total_phone_payments', 0)
    total_expenses = report_data.get('total_expenses', 0)
    amount_to_submit = report_data.get('amount_to_submit', 0)
    expenses_ids = report_data.get('expenses', [])
    orders_by_waiter_data = report_data.get('orders_by_waiter', {})
    
    # Fetch detailed expense data
    expense_details = Expense.objects.filter(id__in=expenses_ids)
    
    # Fetch detailed order data
    orders_by_waiter = {}
    for waiter_id, order_ids in orders_by_waiter_data.items():
        waiter = Waiter.objects.get(id=waiter_id)
        orders = Order.objects.filter(id__in=order_ids)
        if orders.exists():
            orders_by_waiter[waiter] = orders
    
    context = {
        'report': report,
        'total_sales': total_sales,
        'total_phone_payments': total_phone_payments,
        'total_expenses': total_expenses,
        'amount_to_submit': amount_to_submit,
        'orders_by_waiter': orders_by_waiter,
        'expenses': expense_details
    }
    return render(request, 'orders/view_report.html', context)




@login_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save()
            return redirect('orders:menu_item_detail', id=menu_item.id, slug=menu_item.slug)
    else:
        form = MenuItemForm()

    return render(request, 'orders/add_menu_item.html', {'form': form})

# orders/views.py
from django.shortcuts import render
from oda.models import Order, OrderItem, MenuItem
from django.db.models import Sum, F

def detailed_sales_report(request):
    # Aggregate total sales by calculating the sum of (price * quantity) for each order item
    total_sales = OrderItem.objects.aggregate(
        total_sales=Sum(F('price') * F('quantity'))
    )['total_sales'] or 0
    
    # Aggregate total sales by category by calculating the sum of (price * quantity) grouped by category
    sales_by_category = OrderItem.objects.values('menu_item__category__name').annotate(
        total_sales=Sum(F('price') * F('quantity'))
    ).order_by('menu_item__category__name')

    # Retrieve recent orders
    recent_orders = Order.objects.order_by('-created')[:10]

    # Prepare context for the template
    context = {
        'total_sales': total_sales,
        'sales_by_category': sales_by_category,
        'recent_orders': recent_orders,
    }

    return render(request, 'orders/detailed_sales_report.html', context)

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)

# users/views.py
from django.shortcuts import render
from .models import Waiter

def manage_waiters(request):
    waiters = Waiter.objects.all()
    context = {
        'waiters': waiters,
    }
    return render(request, 'users/manage_waiters.html', context)
