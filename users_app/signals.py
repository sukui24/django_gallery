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
            if _old_instance.avatar.name != instance.avatar.name:  # compare to see if image changed
                avatar_delete(sender=User, instance=_old_instance, **kwargs)
        except sender.DoesNotExist:
            pass


@receiver(pre_save, sender=User, dispatch_uid='update_avatar_name_signal')
def update_avatar_name(sender, instance, **kwargs):
    # we do nothing if we create user without avatar (avatar.svg - default)
    if instance.avatar.name == 'avatar.svg':
        return True

    # if image doesn't change we return nothing(True)
    _old_instance = sender.objects.get(id=instance.id)
    if _old_instance.avatar.name == instance.avatar.name:
        return True

    # if image changes or created user with avatar we change
    # avatar name to format "imagename_avatar.jpg"
    _name_start = instance.avatar.name.split('.')[0]
    _name_end = instance.avatar.name.split('.')[-1]
    _filename = f'{_name_start}_avatar.{_name_end}'
    # rename avatar to visually see it in user folder/DB
    instance.avatar.name = _filename


@receiver(pre_save, sender=User, dispatch_uid='set_user_id_signal')
def set_user_id(sender, instance, **kwargs):
    if instance._state.adding:
        _futureID = User.objects.last().id + 1
        instance.id = _futureID

# * ====================== POST_SAVE SIGNALS ======================


@receiver(post_save, sender=User, dispatch_uid='create_user_path_signal')
def create_user_path(sender, instance, created, **kwargs):
    if not os.path.exists(f'./media/images/user_{instance.id}'):
        os.mkdir(f'./media/images/user_{instance.id}')
