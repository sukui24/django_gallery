from django.shortcuts import render, redirect, get_object_or_404

from .models import ImageModel
from .forms import ImageForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def loginUser(request):
    pass


@login_required(login_url='home')
def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    images = ImageModel.objects.all()
    context = {'images': images}
    return render(request, 'base/home.html', context)


def addImage(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ImageForm()
    context = {'form': form}
    return render(request, 'base/add_image_page.html', context)


def viewImage(request, unique_name):
    image = get_object_or_404(ImageModel, unique_name=unique_name)
    context = {'image': image}
    return render(request, 'base/view_image_page.html', context)
