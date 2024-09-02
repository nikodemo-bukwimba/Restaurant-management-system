from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.cart import Cart
from django.contrib import messages

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Create an order with details from the logged-in user
        order = Order.objects.create(user=request.user)
        
        # Iterate through the cart and create OrderItem for each item
        for item in cart:
            OrderItem.objects.create(
                order=order,
                menu_item=item['menu_item'],
                price=item['price'],
                quantity=item['quantity']
            )
        
        # Clear the cart after creating the order
        cart.clear()
        
        # Add a success message
        messages.success(request, 'Your order has been placed successfully!')
        
        # Redirect to the menu list page
        return redirect('orders:menu_item_list')
    return render(request, 'oda/order_create.html')

# def order_confirmation(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'oda/order_confirmation.html', {'order': order})

