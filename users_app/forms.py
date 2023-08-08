from django.forms import Textarea, ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'avatar',
            'bio', 'phone_number', 'city', 'country', 'adress', 'password1', 'password2',
        ]
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='UA'),
            'bio': Textarea(attrs={'cols': '70', 'rows': '5'})
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'avatar',
            'bio', 'phone_number', 'city', 'country', 'adress'
        ]
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='UA'),
            'bio': Textarea(attrs={'cols': '70', 'rows': '5'})
        }
