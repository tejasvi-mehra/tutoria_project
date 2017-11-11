from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class AddFunds(forms.Form):
    amount = forms.FloatField(max_value=5000, help_text='Enter amount')

    def clean_amount(self):
        data = self.cleaned_data['amount']
        return data   
