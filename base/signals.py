from django.core.signals import request_finished
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver

from django.shortcuts import redirect
from .models import ImageModel
import os
import fnmatch

# * Image deleting signal


@receiver(pre_delete, sender=ImageModel, dispatch_uid='image_delete_signal')
def image_deleter(sender, instance, **kwargs):
    _image_path = os.path.join('./media/images/', instance.image.name)

    if os.path.isfile(_image_path):
        os.remove(_image_path)  # remove file if it exists
    else:
        pass  # if image not found we have no need to delete it so we just skip


# * deleting old image (if we edit image)
@receiver(pre_save, sender=ImageModel)
def delete_old_image(sender, instance, **kwargs):
    if instance._state.adding:  # if adding new image we do nothing
        return True

    try:
        _old_instance = sender.objects.get(pk=instance.pk)
        if _old_instance.image.name != instance.image.name:  # compare to see if image changed
            image_deleter(sender=ImageModel, instance=_old_instance, **kwargs)
    except sender.DoesNotExist:
        pass

# * setting (if image just created) or updating (if image updated) unique_name


# ? we're not deleting user_id/ part from image db field to get url to user path
# ex. image_url = user_id/filename.jpg (now we can display image from user folder)
@receiver(post_save, sender=ImageModel)
def update_unique_name(sender, instance, created, **kwargs):
    if created or instance.unique_name:
        # split filename on 2 pieces ['user_id/', 'filename']
        # and getting last element - 'filename'
        _filename = instance.image.name.split('/')[-1]
        instance.__class__.objects.filter(pk=instance.pk).update(
            unique_name=_filename)  # now unique_name = filename without 'user_id/'
