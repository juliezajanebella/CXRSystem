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
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/change-password', views.change_pass, name='change-password'),
    path('change_image/', views.change_image, name='change-image'),
    path('annotation-edit/', views.annotation_edit, name='annotation-edit'),
    path('download/', views.download, name='download'),
    path('ai_annotation/', views.ai_annotation, name='ai-annotation'),
    path('download_pdf/expert-image', views.download_pdf_expert_image, name='download_pdf_expert_image'),
    path('download_pdf/ai-image', views.download_pdf_ai_image, name='download_pdf_ai_image'),
    path('save_image_annotated/', views.save_image_annotated, name='save_image_annotated'),
    path('download/expert/<str:filename>/', views.download_expert_image, name='download_expert'),
    path('download/ai/<str:filename>/', views.download_ai_image, name='download_ai'),
    path('api/save_abnormality', views.save_abnormality, name='save_abnormality'),
]

