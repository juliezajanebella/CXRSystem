# Create your views here.

# Request -> Response
# Action

from django.shortcuts import render, redirect
from django.contrib import messages                           # alert messages
from django.contrib.auth.models import User
from .models import Radiologist, RawXray
from CXRaide.functions import handle_uploaded_file
from django.contrib.auth import authenticate, login


# function
def user_login(request): 
    if request.method == 'POST':
        # input from user
        username = request.POST.get('username')              
        password = request.POST.get('password') 

        # data from database
        cxraide_admin = authenticate(request, username=username, password=password)
        radiologist = Radiologist.objects.filter(radiologist_username=username, radiologist_password=password).exists()

        if cxraide_admin is not None:
            login(request, cxraide_admin)
            messages.success(request, 'CXRaide ADMIN')
            return redirect('admin/')
        elif radiologist:
            return redirect('home/')              
        else:
            messages.error(request, 'Invalid Username or Password.')
    return render(request, 'login.html') 

def home(request):
    if request.method == 'POST':
        # fetching user input
        raw_cxray_name = request.POST.get('raw_cxray_name')
        raw_cxray = request.FILES["raw_cxray"]

        # calling function handler for upload image
        handle_uploaded_file(raw_cxray)

        # 'create' is like an insert function in database
        # first raw_cxray_name is from database, the equivalent (=) is from the form/user
        RawXray.objects.create(raw_cxray_name=raw_cxray_name, raw_cxray=raw_cxray)
        return render(request, 'generateCXR.html') 

    return render(request, 'home.html')


def generate_cxr(request):
    return render(request, 'generateCXR.html') # AI able to annotate


def annotation_edit(request):
    return render(request, 'annotationEdit.html')
 
def download(request):
    return render(request, 'download.html') # final and annotated CXR image
