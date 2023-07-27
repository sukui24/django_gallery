from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_image/', views.addImage, name='add-image'),
]
