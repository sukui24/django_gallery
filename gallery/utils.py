from django.core.paginator import Paginator
import os
import mimetypes


def paginator(request, images):
    # paginate after 9 images
    paginator = Paginator(images, 9)
    page_number = request.GET.get('page')  # current page
    page_obj = paginator.get_page(page_number)
    return page_obj


def user_avatar_path(instance, filename):

    return f'user_{instance.id}/{filename}'


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'user_{instance.host.id}/{filename}'
