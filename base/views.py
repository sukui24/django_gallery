from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.http import FileResponse
from .models import ImageModel
from .forms import ImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os

from django.forms.models import model_to_dict
from django.db.models import Q
from users_app.views import loginUser


def Test(request):
    image = ImageModel.objects.filter(id=16)
    return render(request, 'album_component_new.html', {'image': image})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    images = ImageModel.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(tags__name__in=[q])).order_by('-image_views').distinct()
    context = {'images': images}
    # login from modal when you try to load image unsigned in
    if request.method == "POST":
        return loginUser(request)
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def addImage(request):
    page = 'add'
    if request.method == "POST":

        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.host = request.user
            image.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            return redirect('home')
        else:
            return render(request, 'base/add_image.html', {'form': form, 'page': page})
    else:
        form = ImageForm()
    context = {'form': form, 'page': page}
    return render(request, 'base/add_edit_image.html', context)


def viewImage(request, unique_name, id):

    image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)
    # image views (doesn't depend on the user's IP)
    # we save only image_views field so DB feels ok :)
    image.image_views += 1
    image.save(update_fields=['image_views'])

    image_tags = image.tags.all()
    context = {'image': image, 'image_tags': image_tags}
    return render(request, 'base/view_image.html', context)


@login_required(login_url='login')
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

        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form, 'image_tags': image_tags}
    return render(request, 'base/add_edit_image.html', context)


@login_required(login_url='login')
def deleteImage(request, unique_name, id):
    image = ImageModel.objects.get(id=id, unique_name=unique_name)

    if request.user != image.host:
        return redirect('home')
    else:
        if request.method == "POST":

            image.delete()
            return redirect('home')

    return render(request, 'base/delete_image.html', {'image': image})


def downloadImage(request, id):
    image = ImageModel.objects.get(id=id)
    return FileResponse(image.image.open(), as_attachment=True)
