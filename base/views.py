from django.shortcuts import render, redirect
from .models import ImageModel
from .forms import ImageForm
# Create your views here.


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
