from django.shortcuts import render, redirect, HttpResponse
from .models import User
from base.models import ImageModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from django.contrib import messages
from .forms import MyUserCreationForm, UserForm
# Create your views here.


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

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
    if request.method == "POST":
        form = MyUserCreationForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile', user.id)
    return render(request, 'users_app/login_register.html', {'form': form, 'excluded_fields': excluded_fields})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def userProfile(request, id):
    user = User.objects.get(id=id)
    images = ImageModel.objects.filter(host_id=id).order_by('-created_at')
    context = {'user': user, 'images': images, }
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
        if form.is_valid():
            form.save()
            return redirect('profile', id)
    context = {'form': form, 'excluded_fields': excluded_fields}
    return render(request, 'users_app/edit_user.html', context)


def userImages(request, id):

    user = User.objects.get(id=id)
    images = ImageModel.objects.filter(host_id=id).order_by('-image_views')
    context = {'images': images, 'user': user}
    return render(request, 'users_app/user_images.html', context)


def deleteAccout(request, id):

    user = User.objects.get(id=id)
    if request.method == "POST":
        user.delete()
        return redirect('home')
    context = {'user': user}
    return render(request, 'users_app/delete_account.html', context)
