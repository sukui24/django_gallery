from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class CustomStorage(FileSystemStorage):
    """
    Custom storage for testing `base` app. Used for storing test images
    """

    def __init__(self, location=None, base_url=None):
        if location is None:
            location = os.path.join(
                settings.BASE_DIR, "base/tests/test_images/")
        if base_url is None:
            base_url = '/data/'

        super().__init__(location, base_url)

    def _save(self, name, content):
        return super()._save(name, content)
