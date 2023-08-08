from django.core.signals import request_finished
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from .models import User
import os


@receiver(pre_delete, sender=User, dispatch_uid='avatar_delete_signal')
def avatar_deleter(sender, instance, **kwargs):
    _avatar_path = os.path.join('./media/images/', instance.avatar.name)

    if os.path.isfile(_avatar_path):
        os.remove(_avatar_path)  # remove file if it exists
    else:
        pass  # if avatar not found we have no need to delete it so we just skip


@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    try:
        _old_instance = sender.objects.get(id=instance.id)
        if _old_instance.avatar.name != instance.avatar.name:  # compare to see if image changed
            avatar_deleter(sender=User, instance=_old_instance, **kwargs)
    except sender.DoesNotExist:
        pass


@receiver(pre_save, sender=User)
def update_avatar_name(sender, instance, **kwargs):
    # if image doesn't change we return nothing(True)
    _old_instance = sender.objects.get(id=instance.id)
    if _old_instance.avatar.name == instance.avatar.name:
        return True

    _name_start = instance.avatar.name.split('.')[0]
    _name_end = instance.avatar.name.split('.')[-1]
    _filename = f'{_name_start}_avatar.{_name_end}'
    # rename avatar to visually see it in user folder/DB
    instance.avatar.name = _filename


@receiver(post_save, sender=User)
def create_user_path(sender, instance, created, **kwargs):
    if created:
        os.mkdir(f'./media/images/user_{instance.id}')
