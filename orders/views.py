from django.shortcuts import render, get_object_or_404
from .models import MenuCategory, MenuItem
from orders.models import MenuItem
from cart.forms import CartAddMenuItemForm
from oda.models import Order

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
    orders = Order.objects.filter(user=request.user).order_by('-created')
    total_sales = sum(order.get_total_cost() for order in orders)
    return render(request, 'orders/user_orders.html', {
        'orders': orders,
        'total_sales': total_sales
    })