from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Accounts


class RegisterForm(UserCreationForm):
    class Meta:
        model = Accounts
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'department', 'occupation', 'photo', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=50)
