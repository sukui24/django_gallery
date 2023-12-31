import os
import mimetypes

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator(object):

    """
    * Validator for files, checking the size, extension and mimetype.
    Initialization parameters:
        allowed_extensions: iterable with allowed file extensions
            ie. ('txt', 'doc')
        allowd_mimetypes: iterable with allowed mimetypes
            ie. ('image/png', )
        min_size: minimum number of bytes allowed
            ie. 100
        max_size: maximum number of bytes allowed
            ie. 24 * 1024 * 1024 for 24 MB
    """

    extension_message = (
        """
        Extension "%(extension)s" not allowed.
         Allowed extensions are: ( %(allowed_extensions)s ).
        """)
    mime_message = (
        """
        MIME type "%(mimetype)s" is not valid.
         Allowed types are: ( %(allowed_mimetypes)s ).
        """)
    min_size_message = (
        """
        The current file %(size)s, which is too small.
         The minumum file size is %(allowed_size)s.
        """)
    max_size_message = (
        """
        The current file %(size)s, which is too large.
         The maximum file size is %(allowed_size)s.
        """)

    def __init__(self, *args, **kwargs):
        # get argument if exists or set default (None/0)
        self.allowed_extensions = kwargs.get('allowed_extensions', None)
        self.allowed_mimetypes = kwargs.get('allowed_mimetypes', None)
        self.min_size = kwargs.get('min_size', 0)
        self.max_size = kwargs.get('max_size', None)

    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """

        # Check the extension
        ext = os.path.splitext(value.name)[1][1:].lower()
        if self.allowed_extensions and (ext not in self.allowed_extensions):
            message = self.extension_message % {
                'extension': ext,
                'allowed_extensions': ', '.join(self.allowed_extensions)
            }

            raise ValidationError(message)

        # Check the content type
        mimetype = mimetypes.guess_type(value.name)[0]
        if self.allowed_mimetypes and (mimetype not in self.allowed_mimetypes):
            message = self.mime_message % {
                'mimetype': mimetype,
                'allowed_mimetypes': ', '.join(self.allowed_mimetypes)
            }

            raise ValidationError(message)

        # Check the file size
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_size)
            }

            raise ValidationError(message)

        elif filesize < self.min_size:
            message = self.min_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.min_size)
            }

            raise ValidationError(message)
