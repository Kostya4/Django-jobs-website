from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    avatar = forms.ImageField(required=False)
    birth_date = forms.DateField(required=False)

    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "avatar", "birth_date")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "avatar", "birth_date")


class LoginUserForm(forms.Form):
    email = forms.CharField()
    password2 = forms.CharField()


