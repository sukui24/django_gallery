from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_image/', views.addImage, name='add-image'),
    path('view_image/<str:unique_name>', views.viewImage, name='view-image'),
    path('delete_image/<str:unique_name>',
         views.deleteImage, name='delete-image'),
    path('edit_image/<str:unique_name>', views.editImage, name='edit-image'),
    path('download_image/<str:unique_name>',
         views.downloadImage, name='download-image'),
]
