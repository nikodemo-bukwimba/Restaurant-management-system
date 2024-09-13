from django import forms
from django.contrib.auth import authenticate
from .models import Waiter


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid login")
        return cleaned_data

class WaiterForm(forms.ModelForm):
    class Meta:
        model = Waiter
        fields = ['name', 'manager']  # List all the fields you want to include in the form
