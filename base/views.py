from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404

from django.contrib import messages

from .models import ImageModel, User
from .forms import ImageForm, MyUserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os

from django.forms.models import model_to_dict


def loginUser(request):
    page = 'login'
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

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def registerUser(request):
    future_id = (User.objects.last().id) + 1
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            os.mkdir(f'./media/images/user_{future_id}')

            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile', user.id)
        else:
            messages.error(request, 'Something went wrong during registration')
    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    images = ImageModel.objects.all().order_by('-created_at')
    context = {'images': images}
    return render(request, 'base/home.html', context)

# ! TODO: file extension checking


@login_required(login_url='login')
def addImage(request):
    if request.method == "POST":
        # making sure to create user folder when he try to post image
        if not os.path.exists(f'./media/images/user_{request.user.id}'):
            os.mkdir(f'./media/images/user_{request.user.id}')

        form = ImageForm(request.POST, request.FILES)
        ImageModel.objects.create(
            host=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
        )
        return redirect('home')
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


def userProfile(request, id):
    user = User.objects.get(id=id)
    user_dict = User.objects.filter(id=id)
    images = ImageModel.objects.filter(host_id=id).order_by('-created_at')
    context = {'user': user, 'images': images, }
    return render(request, 'base/profile.html', context)
