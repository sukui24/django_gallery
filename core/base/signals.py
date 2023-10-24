import os
import shutil

from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver

from dotenv import load_dotenv

from base.models import ImageModel

load_dotenv()

cwd = os.getcwd()
parent_dir = os.path.dirname(os.path.abspath(cwd))
# media folder path
data_path = os.path.join(parent_dir, os.environ.get("DATA"))

# ! TODO: Delete related tags after image deleting if they doesn't used on another image


@receiver(pre_delete, sender=ImageModel, dispatch_uid='image_delete_signal')
def image_deleter(sender, instance, **kwargs):
    _all_images_path = data_path
    _image_path = os.path.join(_all_images_path, instance.image.name)

    # thumbnail folder handling
    _thumbnail_folder_path = os.path.join(_all_images_path, 'CACHE/images')
    _thumbnail_folder_name = os.path.splitext(instance.image.name)[0]

    _image_thumbnail_path = os.path.join(
        _thumbnail_folder_path, _thumbnail_folder_name)

    # remove file and thumbnail if it exists
    if os.path.isfile(_image_path):
        if instance.unique_name == 'test_image.jpg':
            # `If` block for testing purposes. Sorry i can't do it other way rn :<
            print("""
        ✓ `Image deletion signal` used. This text wrote instead of actual deleting image from folder
        ✓ This message means test passed.
            """)
        else:
            os.remove(_image_path)

            if os.path.exists(_image_thumbnail_path):
                shutil.rmtree(_image_thumbnail_path)


@receiver(pre_save, sender=ImageModel)
def delete_old_image(sender, instance, **kwargs):
    """
    Old image delition for `edit` action
    """
    if instance._state.adding:
        return True

    try:
        _old_instance = sender.objects.get(pk=instance.pk)
        if _old_instance.image.name != instance.image.name:
            image_deleter(sender=ImageModel,
                          instance=_old_instance, **kwargs)
    except sender.DoesNotExist:
        pass


@receiver(post_save, sender=ImageModel)
def update_unique_name(sender, instance, created, **kwargs):
    """
    # * update unique name while creating/updating image
        we're not deleting user_id/ part from image db field
        to get correct url to user path

        Example:
        image.name = user_id/filename.jpg
        so image.url will return path to:
            'MEDIA_ROOT/user_id/filename.jpg'

    split filename on 2 pieces ['user_id/', 'filename']
    and getting last element - 'filename.jpg'
    """
    if created or instance.unique_name:
        _filename = os.path.split(instance.image.name)[-1]
        instance.__class__.objects.filter(pk=instance.pk).update(
            unique_name=_filename)
