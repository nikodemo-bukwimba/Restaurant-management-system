# orders/forms.py
from django import forms
from .models import Expense, Waiter
from .models import MenuItem

class ExpenseForm(forms.ModelForm):
    waiter = forms.ModelChoiceField(queryset=Waiter.objects.none(), required=False)  # Only for managers

    class Meta:
        model = Expense
        fields = ['amount', 'description', 'waiter']

    def __init__(self, *args, **kwargs):
        manager = kwargs.pop('manager', None)  # Get the manager if provided
        super().__init__(*args, **kwargs)

        if manager:
            # Show only waiters managed by the current manager
            self.fields['waiter'].queryset = Waiter.objects.filter(manager=manager)
        else:
            # Hide the waiter field if the user is not a manager
            self.fields['waiter'].widget = forms.HiddenInput()

# Form for managers to select a waiter when adding an expense
class ExpenseFormForManager(forms.ModelForm):
    waiter = forms.ModelChoiceField(queryset=Waiter.objects.all(), label="Select Waiter")

    class Meta:
        model = Expense
        fields = ['amount', 'description', 'waiter']


  #MenuItem form
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'image', 'description', 'customer_price', 'available']
