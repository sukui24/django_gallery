from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.db.models import Q, F
from django.views import View

from users_app.views import login_user
from gallery.utils import paginator

from base.models import ImageModel
from base.forms import ImageForm
from base.constans import ORDER_OPTIONS_MAP


# custom image sorting by predefined categories ==> 'sort' OR
# by using search bar ==> 'q'


def images_filter(request, q, sort):

    _ordering = ORDER_OPTIONS_MAP.get(sort, '-image_views')

    images = ImageModel.objects.filter(
        Q(title__icontains=q) | Q(
            description__icontains=q) | Q(tags__name__in=[q]),
        is_private=False).order_by(_ordering).distinct()

    # we use 'q' and 'sort' for frontend displaying
    page_obj = paginator(request, images)
    # make correct displaying on frontend
    sort = ' '.join(sort.split('_'))
    return {'images': images, 'q': q, 'sort': sort, 'page_obj': page_obj}


class HomeView(View):

    def get(self, request):
        # sorting by using one of four categories
        q = request.GET.get('q', '')

        # serching via search bar
        sort = request.GET.get('sort', 'most_popular')

        context = images_filter(request, q, sort)
        return render(request, 'base/home.html', context)

    def post(self, request):  # log-in via login modal
        return login_user(self.request)


class AddImageView(LoginRequiredMixin, View):
    # used for redirect unlogged users using 'LoginRequiredMixin'
    login_url = 'register'
    _PAGE = 'add'

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
            'form': form, 'page': self._PAGE})


class ViewImage(View):

    template_name = 'base/view_image.html'

    def get(self, request, id):
        image = get_object_or_404(ImageModel, id=id)

        if image.is_private and request.user != image.host:
            return redirect('home')

        # simple image views counter
        ImageModel.objects.filter(
            id=id).update(image_views=F('image_views') + 1)

        image_tags = image.tags.all()
        tags_amount = len(image_tags)
        return render(request, self.template_name, {
            'image': image, 'image_tags': image_tags,
            'tags_amount': tags_amount})

    def post(self, request):
        return login_user(request)


class EditImage(LoginRequiredMixin, View):
    login_url = 'register'

    def get(self, request, id):
        image = get_object_or_404(ImageModel, id=id)

        if request.user != image.host:
            return redirect('home')

        form = ImageForm(instance=image)
        return self.render_form(request, form, image)

    def post(self, request, id):
        image = get_object_or_404(ImageModel, id=id)
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
            'form': form, 'image': image, 'image_tags': image_tags,
        })


@login_required(login_url='register')
def delete_image(request, id):
    image = get_object_or_404(ImageModel, id=id)

    if request.user == image.host:
        if request.method == "POST":
            image.delete()
            return redirect('home')
    else:
        return redirect('home')

    return render(request, 'base/delete_image.html', {'image': image})


@login_required(login_url='register')
def download_image(request, id):
    image = get_object_or_404(ImageModel, id=id)
    return FileResponse(image.image.open(), as_attachment=True)
