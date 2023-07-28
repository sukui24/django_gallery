from django.forms import ModelForm, TextInput, Textarea
from .models import ImageModel


class ImageForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'
        exclude = ['unique_name',]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'cols': '100'}),
        }
