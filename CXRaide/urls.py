# Create your URLs here.
# URL configuration of each function
# Mapping URL to views

from django.urls import path
from CXRaide import views  

# url patterns in an array
urlpatterns = [
    path('', views.login, name='login'), # as of now; after deployment the url will be 'cxraide.com'
    path('home/', views.home, name='home'),
    path('generate-cxr/', views.generate_cxr, name='generate-cxr'),
    path('annotation-edit/', views.annotation_edit, name='annotations-edit'),
    path('download/', views.download, name='download')

]