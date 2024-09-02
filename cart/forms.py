from django import forms

# Define quantity choices, allowing the user to select a quantity from 1 to 20
MENU_ITEM_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddMenuItemForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=MENU_ITEM_QUANTITY_CHOICES,
        coerce=int
    )
    update_quantity = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)