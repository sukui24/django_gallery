import os

from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver

from dotenv import load_dotenv

from users_app.models import User

load_dotenv()

cwd = os.getcwd()
parent_dir = os.path.dirname(os.path.abspath(cwd))
# media folder path
data_path = os.path.join(parent_dir, os.environ.get("DATA"))

# * ====================== PRE_DELETE SIGNALS ======================


@receiver(pre_delete, sender=User, dispatch_uid='avatar_delete_signal')
def avatar_delete(sender: User, instance: User, **kwargs) -> None:
    _avatar_path = os.path.join(data_path, str(instance.avatar.name))

    if os.path.isfile(_avatar_path):
        os.remove(_avatar_path)  # remove file if it exists
    else:
        pass

# * ====================== PRE_SAVE SIGNALS ======================


@receiver(pre_save, sender=User, dispatch_uid='delete_old_avatar_signal')
def delete_old_avatar(sender: User, instance: User, **kwargs) -> None:
    if not instance._state.adding:
        try:
            _old_instance = sender.objects.get(id=instance.id)
            # compare to see if avatar changed
            if _old_instance.avatar.name != instance.avatar.name:
                avatar_delete(sender=User, instance=_old_instance, **kwargs)
        except sender.DoesNotExist:
            pass


@receiver(pre_save, sender=User, dispatch_uid='update_avatar_name_signal')
def update_avatar_name(sender: User, instance: User, **kwargs) -> None:

    # if image didn't change we return nothing(True)
    if not instance._state.adding:
        _old_instance = sender.objects.get(id=instance.id)
        if _old_instance.avatar.name == 'user_%s/avatar_%s' % (instance.id, str(instance.avatar.name)):
            return None
    # changing avatar name to format "avatar_imagename.jpg"
    elif instance.avatar.name != '':
        instance.avatar.name = 'avatar_%s' % str(instance.avatar.name)
    else:
        pass


@receiver(pre_save, sender=User, dispatch_uid='set_user_id_signal')
def set_user_id(sender: User, instance: User, **kwargs) -> None:
    if instance._state.adding:
        _last_user = User.objects.last()

        if _last_user is None:
            _last_user_id = 0
        else:
            _last_user_id = _last_user.id
        _future_id = _last_user_id + 1
        instance.id = _future_id
# * ====================== POST_SAVE SIGNALS ======================


@receiver(post_save, sender=User, dispatch_uid='create_user_path_signal')
def create_user_path(sender: User, instance: User, created: bool, **kwargs) -> None:
    path = os.path.join(data_path, f"user_{instance.id}")
    if not os.path.exists(path):
        os.mkdir(path)
