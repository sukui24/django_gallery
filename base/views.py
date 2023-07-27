<<<<<<< HEAD
from django.shortcuts import render, redirect
from .models import ImageModel
from .forms import ImageForm
=======
from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
>>>>>>> 3059175a15a1141aae62dd945006ac891423502d
# Create your views here.


def home(request):
<<<<<<< HEAD
    images = ImageModel.objects.all()
    context = {'images': images}
    return render(request, 'home.html', context)


def addImage(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ImageForm()
    context = {'form': form}
    return render(request, 'add_image_page.html', context)
=======
    return render(request, 'base/home.html')


def imageAdd(request):
    form = AddImageForm()
    if request.method == "POST":
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/image_adding_page.html', context)


def imageEdit(request):
    return HttpResponse('Image editing page')


def imagePage(request):
    return HttpResponse('Image viewing page')


def loginPage(request):
    return HttpResponse('login page')


def registerPage(request):
    return HttpResponse('register page')
>>>>>>> 3059175a15a1141aae62dd945006ac891423502d
