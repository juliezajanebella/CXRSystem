# Create your URLs here.
# URL configuration of each function
# Mapping URL to views

from django.urls import path
from . import views

# url patterns in an array
urlpatterns = [
    path('', views.user_login, name='login'), # as of now; after deployment the url will be 'cxraide.com'
    path('home/', views.home, name='home'),
    path('generate-cxr-home/', views.generate_cxr_home, name='generate-cxr-home'),
    path('generate-cxr-update/', views.generate_cxr_update, name='generate-cxr-update'),
    path('update/', views.update, name='update'),
    path('annotation-edit/', views.annotations_edit, name='annotations-edit'),
    path('download/', views.download, name='download')
]

