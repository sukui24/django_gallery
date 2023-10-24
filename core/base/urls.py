from django.urls import path
from base import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add_image/', views.AddImageView.as_view(), name='add-image'),
    path('view_image/<str:id>',
         views.ViewImage.as_view(), name='view-image'),
    path('delete_image/<str:id>',
         views.delete_image, name='delete-image'),
    path('edit_image/<str:id>',
         views.EditImage.as_view(), name='edit-image'),
    path('download_image/<str:id>',
         views.download_image, name='download-image'),
]
