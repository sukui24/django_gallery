from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'base/home.html')


def imageAdd(request):
    return HttpResponse('Image creating page')


def imageEdit(request):
    return HttpResponse('Image adding page')


def imagePage(request):
    return HttpResponse('Image viewing page')
