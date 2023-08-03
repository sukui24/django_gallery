from django.forms import ModelForm, TextInput, Textarea, EmailField
from .models import ImageModel, User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ImageForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'
        exclude = ['unique_name', 'host', 'image_flag']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'cols': '100'}),
        }


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
