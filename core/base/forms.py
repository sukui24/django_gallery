from django.forms import (
    ModelForm, TextInput, Textarea,
    FileInput, CheckboxInput
)
from .models import ImageModel


class ImageForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'
        exclude = ['unique_name', 'host', 'image_views']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={
                'class': 'form-control', 'cols': '100', 'rows': '12'}),
            'image': FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'tags': TextInput(attrs={'class': 'form-control', }),
            'is_private': CheckboxInput(attrs={'class': 'form-check-input'})
        }
