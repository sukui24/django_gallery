from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.db.models import Q, F
from django.views import View

from users_app.views import loginUser
from .models import ImageModel
from .forms import ImageForm
from gallery.utils import paginator

# custom image sorting by predefined categories ==> 'sort' OR
# by using search bar ==> 'q'


def images_filter(request, q, sort):
    # order options (for filtering by predefined categories)
    ORDER_OPTIONS = {
        'Most recent': '-created_at',
        'Least recent': 'created_at',
        'Least popular': 'image_views',
        'Most popular': '-image_views',
    }

    _order = ORDER_OPTIONS.get(sort, '-image_views')
    images = ImageModel.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) | Q(tags__name__in=[q]),
        is_private=False).order_by(_order).distinct()
    # we use 'q' and 'sort' for frontend displaying
    page_obj = paginator(request, images)
    return {'images': images, 'q': q, 'sort': sort, 'page_obj': page_obj}


class HomeView(View):

    def get(self, request):
        # sorting by using one of four categories
        q = request.GET.get('q', '')

        # serching via search bar
        sort = request.GET.get('sort', 'Most popular')

        context = images_filter(request, q, sort)
        return render(request, 'base/home.html', context)

    def post(self, request):  # log-in via login modal
        return loginUser(self.request)


class AddImageView(LoginRequiredMixin, View):
    # used for redirect unlogged users using 'LoginRequiredMixin'
    login_url = 'register'
    PAGE = 'add'

    # 'get' method doesn't depend on context of class instance
    # so no need to use 'self'
    @classmethod
    def get(cls, request):
        form = ImageForm()
        return cls.render_form(self=cls, request=request, form=form)

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.host = request.user
            image.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            return redirect('home')
        else:
            return self.render_form(request, form)

    def render_form(self, request, form):
        return render(request, 'base/add_edit_image.html', {
            'form': form, 'page': self.PAGE})


class ViewImage(View):

    template_name = 'base/view_image.html'

    def get(self, request, unique_name, id):
        image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)

        if image.is_private and request.user != image.host:
            return redirect('home')

        # simple image views counter
        ImageModel.objects.filter(
            id=image.id).update(image_views=F('image_views') + 1)

        image_tags = image.tags.all()
        tags_amount = len(image_tags)
        return render(request, self.template_name, {
            'image': image, 'image_tags': image_tags,
            'tags_amount': tags_amount})

    def post(self, request):
        return loginUser(request)


class EditImage(LoginRequiredMixin, View):
    login_url = 'register'

    def get(self, request, unique_name, id):
        image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)

        if request.user != image.host:
            return redirect('home')

        form = ImageForm(instance=image)
        return self.render_form(request, form, image)

    def post(self, request, unique_name, id):
        image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)
        form = ImageForm(request.POST, request.FILES, instance=image)

        if form.has_changed():
            if form.is_valid():
                form.save()
            else:
                return self.render_form(request, form, image)

        return redirect('user-images', request.user.id)

    def render_form(self, request, form, image):
        image_tags = image.tags.all()
        return render(request, 'base/add_edit_image.html', {
            'form': form, 'image': image, 'image_tags': image_tags, })


@login_required(login_url='register')
def deleteImage(request, unique_name, id):
    image = get_object_or_404(ImageModel, id=id, unique_name=unique_name)

    if request.user == image.host:
        if request.method == "POST":
            image.delete()
            return redirect('home')
    else:
        return redirect('home')

    return render(request, 'base/delete_image.html', {'image': image})


@login_required(login_url='register')
def downloadImage(request, id):
    image = get_object_or_404(ImageModel, id=id)
    return FileResponse(image.image.open(), as_attachment=True)
