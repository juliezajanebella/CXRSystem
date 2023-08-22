# Create your views here.
# Request Handler
# Request -> Response
# Action

from django.shortcuts import render
from django.http import HttpResponse 

# function
def login(request):
    return render(request, 'login.html') # able to login users

def home(request):
    return render(request, 'home.html', {'name': ' Jane'}) # able to upload image, welcome page

def generate_cxr(request):
    return render(request, 'generateCXR.html') # AI able to annotate

def annotation_edit(request):
    return render(request, 'annotationEdit.html') # experts able to annotate

def download(request):
    return render(request, 'download.html') # final and annotated CXR image