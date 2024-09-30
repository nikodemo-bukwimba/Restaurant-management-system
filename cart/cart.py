from decimal import Decimal
from django.conf import settings
from orders.models import MenuItem  # Import your MenuItem model

class Cart: 
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, menu_item, quantity=1, update_quantity=False):
        """
        Add a menu item to the cart or update its quantity.
        """
        menu_item_id = str(menu_item.id)
        
        # Check if the item is already in the cart
        if menu_item_id not in self.cart:
            self.cart[menu_item_id] = {
                'name': menu_item.name,
                'price': str(menu_item.customer_price),
                'quantity': 0,
                'image': menu_item.image.url if menu_item.image else ''
            }

        # Update quantity
        if update_quantity:
            self.cart[menu_item_id]['quantity'] = quantity
        else:
            self.cart[menu_item_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Save the cart to the session.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, menu_item):
        """
        Remove a menu item from the cart.
        """
        menu_item_id = str(menu_item.id)
        if menu_item_id in self.cart:
            del self.cart[menu_item_id]
            self.save()

    def get_items(self):
        """
        Get all items in the cart.
        """
        return self.cart.values()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the items from the database.
        """
        menu_item_ids = self.cart.keys()
        menu_items = MenuItem.objects.filter(id__in=menu_item_ids)
        for menu_item in menu_items:
            self.cart[str(menu_item.id)]['menu_item'] = menu_item

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total price of the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True