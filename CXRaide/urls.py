# Create your URLs here.
# URL configuration of each function
# Mapping URL to views

from django.urls import path
from . import views

# url patterns in an array
urlpatterns = [
    path('', views.user_login, name='login'), # as of now; after deployment the url will be 'cxraide.com'
    path('create-acc/', views.create_acc, name='create-acc'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('update/', views.update, name='update'),
    path('annotation-edit/', views.annotation_edit, name='annotation-edit'),
    path('download/', views.download, name='download'),
]

