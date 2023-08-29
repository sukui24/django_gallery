from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import FileResponse
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.views.generic.detail import DetailView
from users_app.views import loginUser
from .models import ImageModel
from .forms import ImageForm


# custom image sorting by predefined categories ==> 'sort'
# or by using search bar ==> 'q'
def images_filter(q, sort):
    # static order options (for filtering by predefined categories)
    _order_options = {
        'Most recent': '-created_at',
        'Least recent': 'created_at',
        'Least popular': 'image_views',
        'Most popular': '-image_views',
    }

    _order = _order_options.get(sort, '-image_views')

    images = ImageModel.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) | Q(tags__name__in=[q]),
        is_private=False).order_by(_order).distinct()
    # we use 'q' and 'sort' for frontend displaying
    return {'images': images, 'q': q, 'sort': sort}


class HomeView(View):

    def get(self, request):
        # sorting by using one of four categories
        q = request.GET.get('q', '')

        # serching via search bar
        sort = request.GET.get('sort', 'Most popular')

        context = images_filter(q, sort)

        return render(request, 'base/home.html', context)

    def post(self, request):  # log-in via login modal
        return loginUser(self.request)


class AddImageView(LoginRequiredMixin, View):
    # used for redirect unlogged users using 'LoginRequiredMixin'
    login_url = 'register'

    PAGE = 'add'
    form = ImageForm
    template_name = 'base/add_edit_image.html'
    context = {'form': form, 'page': PAGE}

    # 'get' method doesn't depend on context of class instance so no need to use 'self'
    @staticmethod
    def get(request):
        form = AddImageView.form()
        return render(request, AddImageView.template_name, AddImageView.context)

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.host = request.user
            image.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            return redirect('home')
        else:
            return render(request, self.template_name, self.context)


class ViewImage(View):

    template_name = 'base/view_image.html'

    def get(self, request, unique_name, id):
        image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)

        if image.is_private == True and request.user != image.host:
            return redirect('home')

        # image views (doesn't depend on the user's IP)
        image.image_views += 1
        image.save(update_fields=['image_views'])
        image_tags = image.tags.all()
        return render(request, self.template_name, {'image': image, 'image_tags': image_tags})

    def post(self, request):
        return loginUser(request)


class EditImage(LoginRequiredMixin, View):
    login_url = 'register'

    template_name = 'base/add_edit_image.html'
    form = ImageForm

    def get(self, request, unique_name, id):
        image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)
        if request.user != image.host:
            return redirect('home')

        form = self.form(instance=image)
        return render(request, self.template_name, {'image': image, 'form': form})

    def post(self, request, unique_name, id):
        image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)
        form = self.form(request.POST, request.FILES, instance=image)

        if not form.has_changed():
            return redirect('user-images', request.user.id)

        elif form.is_valid():
            form.save()
            return redirect('user-images', request.user.id)


@login_required(login_url='register')
def deleteImage(request, unique_name, id):
    image = ImageModel.objects.get(id=id, unique_name=unique_name)

    if request.user == image.host:
        if request.method == "POST":
            image.delete()
            return redirect('home')
    else:
        return redirect('home')

    return render(request, 'base/delete_image.html', {'image': image})


@login_required(login_url='register')
def downloadImage(request, id):
    image = ImageModel.objects.get(id=id)
    return FileResponse(image.image.open(), as_attachment=True)
