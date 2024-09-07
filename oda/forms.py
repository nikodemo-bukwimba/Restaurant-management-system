from django import forms
from .models import Order
from users.models import Waiter

class OrderCreateForm(forms.ModelForm):
    # Only managers should see the waiter field
    waiter = forms.ModelChoiceField(queryset=Waiter.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['waiter']  # Include other fields as needed

    def __init__(self, *args, **kwargs):
        is_manager = kwargs.pop('is_manager', False)
        super().__init__(*args, **kwargs)
        
        if not is_manager:
            self.fields['waiter'].widget = forms.HiddenInput()
