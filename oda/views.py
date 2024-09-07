from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.cart import Cart
from django.contrib import messages
from users.models import Waiter, Shift
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request):
    cart = Cart(request)
    is_manager = hasattr(request.user, 'manager')  # Check if user is a manager
    waiters = Waiter.objects.all() if is_manager else []  # Get waiters if manager

    if request.method == 'POST':
        if len(cart) == 0:  # Check if cart is empty
            messages.error(request, 'Your cart is empty.')
            return redirect('orders:menu_item_list')

        total_cost = 0  # Initialize total cost

        # Create an order with details from the logged-in user
        order = Order(user=request.user)

        if is_manager:
            waiter_id = request.POST.get('waiter')
            if waiter_id:
                try:
                    waiter = Waiter.objects.get(id=waiter_id)
                    order.assigned_waiter = waiter  # Assign waiter to the order

                    # Fetch the latest active shift for the assigned waiter
                    shift = Shift.objects.filter(waiter=waiter, end_time__isnull=True).last()
                    if shift is None:
                        messages.error(request, 'The selected waiter does not have an active shift.')
                        return redirect('oda:order_create')
                    order.shift = shift

                except Waiter.DoesNotExist:
                    messages.error(request, 'Selected waiter does not exist.')
                    return redirect('oda:order_create')
            else:
                messages.error(request, 'Please select a waiter.')
                return redirect('oda:order_create')

        else:  # This part handles waiters creating their own orders
            # Fetch the current waiter and their active shift
            try:
                waiter = Waiter.objects.get(user=request.user)
                shift = Shift.objects.filter(waiter=waiter, end_time__isnull=True).last()

                if shift is None:
                    messages.error(request, 'You do not have an active shift. Please start a shift to place an order.')
                    return redirect('orders:menu_item_list')  # Redirect back if no active shift

                # Assign the shift to the order
                order.shift = shift

            except Waiter.DoesNotExist:
                messages.error(request, 'You are not authorized to create orders.')
                return redirect('orders:menu_item_list')

        # Save the order to the database before creating OrderItems
        order.save()

        # Iterate through the cart and create OrderItem for each item
        for item in cart:
            OrderItem.objects.create(
                order=order,
                menu_item=item['menu_item'],
                price=item['price'],
                quantity=item['quantity']
            )
            total_cost += item['price'] * item['quantity']  # Calculate total cost

        # Set total cost for the order
        order.total_cost = total_cost
        order.save()  # Save the updated order with total cost and assigned waiter

        # Clear the cart after creating the order
        cart.clear()

        # Add a success message
        messages.success(request, 'Order placed successfully!')

        # Redirect to the menu list page
        return redirect('orders:menu_item_list')

    # Context for rendering the form
    context = {
        'cart': cart,
        'is_manager': is_manager,
        'waiters': waiters
    }

    return render(request, 'oda/order_create.html', context)

