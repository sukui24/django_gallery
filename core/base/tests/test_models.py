import os

from django.urls import reverse
from django.test import TestCase
from base.models import ImageModel
from gallery.settings import BASE_DIR
from .utils import create_superuser


class TestModels(TestCase):
    """
    Test some model actions. Actually most of them are just signals
    """

    def setUp(self):
        self.edit_image_path = reverse('edit-image', args=['1'])

    def test_image_unique_name_updating_after_create(self):
        """
        => test_models => TestModels
        """
        image_path = os.path.join(BASE_DIR,
                                  'base/tests/test_images/test_image.jpg')
        host = create_superuser(self.client)
        ImageModel.objects.create(
            id=1,
            title='images',
            image=image_path,
            host=host,
        )
        # didn't return image creation in variable cause unique_name
        # changes after saving the model
        image = ImageModel.objects.get(pk=1)

        self.assertEquals(image.image, image_path)
        self.assertEquals(image.unique_name, 'test_image.jpg')

    def test_old_image_deletion_after_edit(self):
        """
        => test_models => TestModels
        """
        host = create_superuser(self.client)
        old_image_path = os.path.join(BASE_DIR,
                                      'base/tests/test_images/test_image.jpg')
        ImageModel.objects.create(
            id=1,
            title='old_image',
            image=old_image_path,
            host=host
        )
        old_image = ImageModel.objects.get(pk=1)
        new_image_path = os.path.join(BASE_DIR,
                                      'base/tests/test_images/test_edit_image.jpg')

        with open(new_image_path, 'rb') as image:
            response = self.client.post(self.edit_image_path, {
                "title": old_image.title,
                "is_private": old_image.is_private,
                "description": old_image.description,
                "tags": old_image.tags,
                "image": image
            })

        new_image = ImageModel.objects.get(pk=1)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_image.unique_name, 'test_edit_image.jpg')
        self.assertEquals(new_image.image, 'user_1/test_edit_image.jpg')
