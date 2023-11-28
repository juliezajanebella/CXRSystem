# Create your views here.

# Request -> Response
# Action

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages                           # alert messages
from django.contrib.auth.models import User
from .models import Radiologist, RawXray
from CXRaide.functions import handle_uploaded_file
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404



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

        # calling the handler of uploaded file
        handle_uploaded_file(raw_cxray)
        RawXray.objects.create(raw_cxray_name=raw_cxray_name, raw_cxray=raw_cxray)

        return (raw_cxray_name, raw_cxray)  # Return the values as a tuple
        
    return render(request, 'home.html')   # Return None if no file was uploaded


def generate_cxr_home(request):
    generate_cxray = home(request)

    if generate_cxray:
        raw_cxray_name, raw_cxray = generate_cxray

        context = {'raw_cxray_name': raw_cxray_name, 'raw_cxray': raw_cxray}
        return render(request, 'generateCXR.html', context)
    
    # If no data was uploaded, render the template without context
    return render(request, 'generateCXR.html')


def update(request):
    if request.method == 'POST':
        # fetching user input
        prev_raw_cxray_name = request.POST.get('prev_raw_cxray_name')
        updated_raw_cxray_name = request.POST.get('raw_cxray_name')
        updated_raw_cxray = request.FILES["raw_cxray"]

        # calling the handler of uploaded file
        handle_uploaded_file(updated_raw_cxray)

        # fetching the previous input of the user / from the database
        current_input = RawXray.objects.filter(raw_cxray_name=prev_raw_cxray_name).exists()

        if current_input:
            update = RawXray.objects.get(raw_cxray_name=prev_raw_cxray_name)
            update.raw_cxray_name = updated_raw_cxray_name
            update.raw_cxray = updated_raw_cxray
            update.save()

            return (updated_raw_cxray_name, updated_raw_cxray)
        
    return render(request, 'update.html') # final and annotated CXR image


def generate_cxr_update(request):
    generate_cxray = update(request)

    if generate_cxray:
        updated_raw_cxray_name, updated_raw_cxray = generate_cxray
        
        context = {'raw_cxray_name': updated_raw_cxray_name, 'raw_cxray': updated_raw_cxray}
        return render(request, 'generateCXR.html', context)

    # If no data was uploaded, render the template without context
    return render(request, 'generateCXR.html')


def annotations_edit(request, ):
    # NOTHING WORKING :(
        # kuhaa ang ID
        # query parameters 
    
    # TRY HUHU
  


    
    return render(request, 'annotationEdit.html')
    
def download(request):
    
    return render(request, 'download.html')
 

