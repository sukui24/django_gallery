from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from .models import ImageModel
import os
import shutil


@receiver(pre_delete, sender=ImageModel, dispatch_uid='image_delete_signal')
def image_deleter(sender, instance, **kwargs):
    _images_path = './media/images/'
    _original_image_path = os.path.join(_images_path, instance.image.name)

    # thumbnail folder handling
    _thumbnail_folder_path = os.path.join(_images_path, 'CACHE/images')
    _tmp_folder_name = instance.image.name.split('.')
    # handling situation when img have multiple dots in name
    # we forced to do this check so we won't force 'for' cycle for no reasons
    _thumbnail_folder_name = ''
    if len(_tmp_folder_name) > 2:
        _tmp_folder_name = _tmp_folder_name[:-1]
        # collecting all list items in one string
        for i in _tmp_folder_name:
            # if last item we don't add dot at end
            if i == _tmp_folder_name[-1]:
                _thumbnail_folder_name += i
            else:
                _thumbnail_folder_name = _thumbnail_folder_name + i + '.'
    else:
        # if one dot we just get first part without 'png/jpg/etc...'
        _thumbnail_folder_name = _tmp_folder_name[0]
    _thumbnail_image_path = os.path.join(
        _thumbnail_folder_path, _thumbnail_folder_name)

    if os.path.isfile(_original_image_path):
        os.remove(_original_image_path)  # remove file if it exists
        shutil.rmtree(_thumbnail_image_path)  # remove thumbnail
    else:
        pass  # if image not found we have no need to delete it so we just skip


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

# * update unique name while creating/updating image
# we're not deleting user_id/ part from image db field to get url to user path
# ex. image_url = user_id/filename.jpg (now we can display image from user folder)


@receiver(post_save, sender=ImageModel)
def update_unique_name(sender, instance, created, **kwargs):
    if created or instance.unique_name:
        # split filename on 2 pieces ['user_id/', 'filename']
        # and getting last element - 'filename.jpg'
        _filename = instance.image.name.split('/')[-1]
        instance.__class__.objects.filter(pk=instance.pk).update(
            unique_name=_filename)  # now unique_name = filename without 'user_id/'
