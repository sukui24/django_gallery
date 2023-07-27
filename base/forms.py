from django.forms import ModelForm

from .models import ImageModel


class ImageForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'
