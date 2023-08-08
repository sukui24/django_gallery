from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.http import FileResponse
from .models import ImageModel
from .forms import ImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os

from django.forms.models import model_to_dict
from django.db.models import Q


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    images = ImageModel.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q)).order_by('-created_at')
    context = {'images': images}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def addImage(request):
    if request.method == "POST":

        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            ImageModel.objects.create(
                host=request.user,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                image=request.FILES.get('image'),
            )
            return redirect('home')
        else:
            return render(request, 'base/add_image.html', {'form': form})
    else:
        form = ImageForm()
    context = {'form': form}
    return render(request, 'base/add_image.html', context)


def viewImage(request, unique_name):
    image = get_object_or_404(ImageModel, unique_name=unique_name)
    context = {'image': image}
    return render(request, 'base/view_image.html', context)


def editImage(request, unique_name):
    image = get_object_or_404(ImageModel, unique_name=unique_name)
    form = ImageForm(instance=image)

    if request.user != image.host:
        return HttpResponse("You're not allowed here !")

    # updating image info
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            if 'image' in form.changed_data:
                image.unique_name = form.cleaned_data['image']
            return redirect('view-image', image.unique_name)

    context = {'form': form}
    return render(request, 'base/edit_image.html', context)


@login_required(login_url='login')
def deleteImage(request, unique_name):
    image = ImageModel.objects.get(unique_name=unique_name)

    if request.user != image.host:
        return redirect('home')
    else:
        if request.method == "POST":

            image.delete()
            return redirect('home')

    return render(request, 'base/delete_image.html', {'image': image})


def downloadImage(request, unique_name):
    image = ImageModel.objects.get(unique_name=unique_name)
    return FileResponse(image.image.open(), as_attachment=True)
