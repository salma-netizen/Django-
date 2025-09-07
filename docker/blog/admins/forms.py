from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class LoginAdmin(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username..'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'}))
