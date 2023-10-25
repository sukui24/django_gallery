import os

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class CustomStorage(FileSystemStorage):
    """
    Custom storage for testing. Used for storing test images
    """

    def __init__(self, location=None, base_url=None) -> None:
        if location is None:
            location = os.path.join(
                settings.BASE_DIR, "base/tests/test_images/")
        if base_url is None:
            base_url = '/data/'

        super().__init__(location, base_url)

    def _save(self, name, content) -> None:
        return super()._save(name, content)
