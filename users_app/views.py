from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from base.models import ImageModel
from gallery.utils import paginator
from .forms import MyUserCreationForm, UserForm
from .models import User


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
    # if 'email' in POST that means user register
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

    return render(request, 'users_app/register.html',
                  {'form': form, 'excluded_fields': excluded_fields})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def userProfile(request, id):

    user = get_object_or_404(User, id=id)

    images = ImageModel.objects.filter(
        host_id=id, is_private=False).order_by('-created_at')

    # that all should be done by frontend through API
    images_count = ImageModel.objects.filter(host_id=id).count()
    public_images_count = images.count()
    private_images_count = ImageModel.objects.filter(
        host_id=id, is_private=True).count()

    context = {'user': user, 'images': images,
               'public_images_count': public_images_count,
               'private_images_count': private_images_count,
               'images_count': images_count}

    if request.method == "POST":
        return loginUser(request)

    return render(request, 'users_app/profile.html', context)


@login_required(login_url='login')
def editUser(request, id):

    user = get_object_or_404(User, id=id)

    form = UserForm(instance=user)
    # using excluded_fields to manage frontend decoration
    excluded_fields = [
        'username', 'email', 'avatar',
        'bio', 'phone_number', 'adress'
    ]
    context = {'form': form, 'excluded_fields': excluded_fields}

    if user != request.user:
        return HttpResponse("You're not allowed here!")

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.has_changed():
            if form.is_valid():
                form.save()
            else:
                return render(request, 'users_app/edit_user.html', context)
        return redirect('profile', id)

    return render(request, 'users_app/edit_user.html', context)


def userImages(request, id, privacity=False):

    user = get_object_or_404(User, id=id)

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
    user = get_object_or_404(User, id=id)
    if request.user != user:
        return redirect('home')
    # set privacity on True to see private images
    return userImages(request=request, id=id, privacity=True)


def deleteAccout(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.delete()
        return redirect('home')

    context = {'user': user}
    return render(request, 'users_app/delete_account.html', context)
