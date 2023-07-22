from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
# Create your views here.


def home(request):
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
