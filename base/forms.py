from django.forms import ModelForm
<<<<<<< HEAD

from .models import ImageModel


class ImageForm(ModelForm):
    class Meta:
        model = ImageModel
=======
from .models import *


class AddImageForm(ModelForm):

    class Meta:
        model = ImageRoom
>>>>>>> 3059175a15a1141aae62dd945006ac891423502d
        fields = '__all__'
