from django.forms import Textarea, ModelForm, FileInput, TextInput
from django.contrib.auth.forms import UserCreationForm

from .models import User

from phonenumber_field.widgets import PhoneNumberPrefixWidget


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'email', 'avatar', 'bio',
            'phone_number', 'city', 'country',
            'adress', 'password1', 'password2',
        ]
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(
                country_attrs={
                    'class': 'form-control col'
                },
                number_attrs={
                    'class': 'form-control col me-lg-4',
                    'placeholder': 'xxx xxx-xx-xx'
                }, initial='UA'),

            'bio': Textarea(attrs={
                'cols': '70', 'rows': '5',
                'class': 'form-control col me-lg-4'}),

            'first_name': TextInput(attrs={
                'class': 'form-control col me-lg-2'}),

            'last_name': TextInput(attrs={
                'class': 'form-control col'}),

            'username': TextInput(attrs={
                'class': 'form-control col me-lg-4'}),

            'email': TextInput(attrs={
                'class': 'form-control col me-lg-4'}),

            'avatar': FileInput(attrs={
                'class': 'form-control col me-lg-4'}),

            'city': TextInput(attrs={
                'class': 'form-control col me-lg-2'}),

            'country': TextInput(attrs={
                'class': 'form-control col'}),

            'adress': TextInput(attrs={
                'class': 'form-control col me-lg-4'}),
        }

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control col me-lg-2'
        self.fields['password2'].widget.attrs['class'] = 'form-control col'
        self.fields['phone_number'].widget.attrs['maxlength'] = '12'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'avatar',
            'bio', 'phone_number', 'city', 'country', 'adress'
        ]
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(
                country_attrs={'class': 'form-control col'},
                number_attrs={
                    'class': 'form-control col me-lg-4',
                    'placeholder': 'xxx xxx-xx-xx'},
                initial='UA'),

            'bio': Textarea(attrs={
                'cols': '70', 'rows': '5',
                'class': 'form-control col me-lg-4'}),

            'first_name': TextInput(attrs={
                'class': 'form-control col me-lg-2'}),

            'last_name': TextInput(attrs={
                'class': 'form-control col'}),

            'username': TextInput(attrs={
                'class': 'form-control col me-lg-4'}),

            'email': TextInput(attrs={
                'class': 'form-control col me-lg-4'}),

            'avatar': FileInput(attrs={
                'class': 'form-control col me-lg-4'}),

            'city': TextInput(attrs={
                'class': 'form-control col me-lg-2'}),

            'country': TextInput(attrs={
                'class': 'form-control col'}),

            'adress': TextInput(attrs={
                'class': 'form-control col me-lg-4'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['phone_number'].widget.attrs['maxlength'] = '12'
