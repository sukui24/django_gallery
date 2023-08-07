from django.apps import AppConfig
from django.core.signals import request_finished
from django.dispatch import receiver


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):

        import base.signals
