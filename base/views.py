from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.http import FileResponse
from .models import ImageModel
from .forms import ImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from django.views.generic import TemplateView
from django.views import View
from django.forms.models import model_to_dict
from django.db.models import Q
from users_app.views import loginUser

# TemplateView - uses to show static pages or pages that uses GET request
#


def images_filter(q, sort):
    order_options = {
        'Most recent': '-created_at',
        'Least recent': 'created_at',
        'Least popular': 'image_views',
        'Most popular': '-image_views',
    }

    _order = order_options.get(sort, '-image_views')

    images = ImageModel.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(tags__name__in=[q]), is_private=False).order_by(_order).distinct()
    # we use q and s for frontend displaying so sending it in context
    return {'images': images, 'q': q, 'sort': sort}


class Home(View):

    def get(self, request):
        # searching from categories (for ex. most popular)
        q = request.GET.get('q', '')

        # serching from search bar
        sort = request.GET.get('sort', 'Most popular')

        # using my custom filter for images that returns context
        context = images_filter(q, sort)

        return render(self.request, 'base/home.html', context)

    def post(self, request):  # here we got post request after logging in with using modal
        return loginUser(self.request)  # using login user view


class AddImage(View):
    page = 'add'

    def get(self, requset):
        form = ImageForm()
        context = {'form': form, 'page': self.page}
        return render(self.request, 'base/add_edit_image.html', context)

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.host = request.user
            image.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            return redirect('home')
        else:
            return render(self.request, 'base/add_image.html', {'form': form, 'page': self.page})


def viewImage(request, unique_name, id):

    image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)

    if image.is_private == True and request.user != image.host:
        return redirect('home')
    # image views (doesn't depend on the user's IP)
    # we save only image_views field so DB feels ok :)
    image.image_views += 1
    image.save(update_fields=['image_views'])

    image_tags = image.tags.all()

    context = {'image': image, 'image_tags': image_tags}
    return render(request, 'base/view_image.html', context)


@login_required(login_url='register')
def editImage(request, unique_name, id):

    image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)
    form = ImageForm(instance=image)
    image_tags = image.tags.all()

    if request.user != image.host:
        return HttpResponse("You're not allowed here !")

    # updating image info
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        # we have no need to force save method if user didn't change any data
        if len(form.changed_data) <= 0:
            return redirect('home')

        elif form.is_valid():
            form.save()
            return redirect('user-images', request.user.id)

    context = {'form': form, 'image_tags': image_tags}
    return render(request, 'base/add_edit_image.html', context)


@login_required(login_url='register')
def deleteImage(request, unique_name, id):
    image = ImageModel.objects.get(id=id, unique_name=unique_name)

    if request.user != image.host:
        return redirect('home')
    else:
        if request.method == "POST":

            image.delete()
            return redirect('home')

    return render(request, 'base/delete_image.html', {'image': image})


@login_required(login_url='register')
def downloadImage(request, id):
    image = ImageModel.objects.get(id=id)
    return FileResponse(image.image.open(), as_attachment=True)
