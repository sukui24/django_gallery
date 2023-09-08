from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from .models import User
import os

# * ====================== PRE_DELETE SIGNALS ======================


@receiver(pre_delete, sender=User, dispatch_uid='avatar_delete_signal')
def avatar_delete(sender, instance, **kwargs):
    _avatar_path = os.path.join('./media/images/', instance.avatar.name)

    if os.path.isfile(_avatar_path):
        os.remove(_avatar_path)  # remove file if it exists
    else:
        pass  # if avatar not found we have no need to delete it so we just skip

# * ====================== PRE_SAVE SIGNALS ======================


@receiver(pre_save, sender=User, dispatch_uid='delete_old_avatar_signal')
def delete_old_avatar(sender, instance, **kwargs):
    if not instance._state.adding:
        try:
            _old_instance = sender.objects.get(id=instance.id)
            if _old_instance.avatar.name != instance.avatar.name:  # compare to see if avatar changed
                avatar_delete(sender=User, instance=_old_instance, **kwargs)
        except sender.DoesNotExist:
            pass


@receiver(pre_save, sender=User, dispatch_uid='update_avatar_name_signal')
def update_avatar_name(sender, instance, **kwargs):
    # if user didn't add avatar we return default avatar (sets post save)
    if instance.avatar.name == 'default_avatar_4a846998d2c63d936cd7b796c67790343adf5d5b.png':
        return True

    # if image didn't change we return nothing(True)
    if not instance._state.adding:
        _old_instance = sender.objects.get(id=instance.id)
        if _old_instance.avatar.name == instance.avatar.name:
            return True

    # changing avatar name to format "avatar_imagename.jpg"
    instance.avatar.name = 'avatar_%s' % (instance.avatar.name)


@receiver(pre_save, sender=User, dispatch_uid='set_user_id_signal')
def set_user_id(sender, instance, **kwargs):
    if instance._state.adding:
        _future_id = User.objects.last().id + 1
        instance.id = _future_id
# * ====================== POST_SAVE SIGNALS ======================


@receiver(post_save, sender=User, dispatch_uid='create_user_path_signal')
def create_user_path(sender, instance, created, **kwargs):
    if not os.path.exists(f'./media/images/user_{instance.id}'):
        os.mkdir(f'./media/images/user_{instance.id}')
