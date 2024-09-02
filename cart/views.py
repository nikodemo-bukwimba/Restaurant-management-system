from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from orders.models import MenuItem  # Assuming MenuItem is in orders.models
from .cart import Cart
from .forms import CartAddMenuItemForm  # Adjusted form name
from oda.models import Order, OrderItem  # Ensure the correct import

@require_POST
def cart_add(request, menu_item_id):
    cart = Cart(request)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    form = CartAddMenuItemForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd.get('quantity', 1)  # Default to 1 if not provided
        update_quantity = cd.get('update_quantity', False)  # Default to False if not provided
        cart.add(menu_item=menu_item, quantity=quantity, update_quantity=update_quantity)
    
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, menu_item_id):
    cart = Cart(request)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    cart.remove(menu_item)  # Remove menu items from the cart
    return redirect('cart:cart_detail')  # Redirect to cart detail page

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddMenuItemForm(
            initial={'quantity': item['quantity']}
        )
    
    return render(request, 'cart/detail.html', {'cart': cart})

# def order_confirmation(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'orders/order_confirmation.html', {'order': order})
