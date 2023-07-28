from django.forms import ModelForm, TextInput, Textarea, EmailField
from .models import ImageModel, User
from django.contrib.auth.forms import UserCreationForm


class ImageForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'
        exclude = ['unique_name', 'host']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'cols': '100'}),
        }


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'password1']
        widgets = {
            'bio': Textarea(attrs={'cols': '70', 'rows': '5'})
        }
