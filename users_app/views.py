from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from base.models import ImageModel
from .forms import MyUserCreationForm, UserForm
from .models import User

import os


def paginator(request, images):
    # paginate after 9 images on page
    paginator = Paginator(images, 9)
    page_number = request.GET.get('page')  # current page
    page_obj = paginator.get_page(page_number)
    return page_obj


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username,
                            password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return redirect('home')


def registerUser(request):
    form = MyUserCreationForm()
    # using excluded_fields to manage frontend decoration
    excluded_fields = [
        'username', 'email', 'avatar',
        'bio', 'phone_number', 'adress'
    ]
    # checking if one of required fields in post request
    # to see if it register or login via modal
    if request.method == "POST" and 'email' in request.POST:
        form = MyUserCreationForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile', user.id)

    elif request.method == "POST":
        return loginUser(request)

    return render(request, 'users_app/register.html', {'form': form, 'excluded_fields': excluded_fields})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def userProfile(request, id):
    user = User.objects.get(id=id)
    images = ImageModel.objects.filter(host_id=id).order_by('-created_at')
    context = {'user': user, 'images': images, }

    if request.method == "POST":
        return loginUser(request)

    return render(request, 'users_app/profile.html', context)


@login_required(login_url='login')
def editUser(request, id):

    user = User.objects.get(id=id)
    form = UserForm(instance=user)
    # using excluded_fields to manage frontend decoration
    excluded_fields = [
        'username', 'email', 'avatar',
        'bio', 'phone_number', 'adress'
    ]
    if user != request.user:
        return HttpResponse("You're not allowed here!")

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)

        if not form.has_changed():
            return redirect('profile', id)

        elif form.is_valid():
            form.save()
            return redirect('profile', id)

    context = {'form': form, 'excluded_fields': excluded_fields}
    return render(request, 'users_app/edit_user.html', context)


def userImages(request, id, privacity=False):

    user = User.objects.get(id=id)
    images = ImageModel.objects.filter(
        host_id=id, is_private=privacity).order_by('-image_views')
    page_obj = paginator(request, images)
    # send privacity in context to show the right button on page
    context = {'images': images, 'user': user,
               'privacity': privacity, 'page_obj': page_obj}

    if request.method == "POST":
        return loginUser(request)

    return render(request, 'users_app/user_images.html', context)


def userImagesPrivate(request, id):
    # if user isn't host send him home
    if request.user != User.objects.get(id=id):
        return redirect('home')
    # if we want to open private images page we just reuse userImages view
    # but set the filter's 'is_private' attribute on True
    return userImages(request=request, id=id, privacity=True)


def deleteAccout(request, id):

    user = User.objects.get(id=id)

    if request.method == "POST":
        user.delete()
        return redirect('home')

    context = {'user': user}
    return render(request, 'users_app/delete_account.html', context)
