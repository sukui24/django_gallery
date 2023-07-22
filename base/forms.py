from django.forms import ModelForm
from .models import *


class AddImageForm(ModelForm):

    class Meta:
        model = ImageRoom
        fields = '__all__'
