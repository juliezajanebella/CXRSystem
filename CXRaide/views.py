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


# main functions
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

        context = {'raw_cxray_name': raw_cxray_name, 'raw_cxray': raw_cxray}
        return render(request, 'generateCXR.html', context)
        
    return render(request, 'home.html')   # Return None if no file was uploaded


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

            context = {'raw_cxray_name': updated_raw_cxray_name, 'raw_cxray': updated_raw_cxray}
            return render(request, 'generateCXR.html', context)
        
    return render(request, 'update.html') # final and annotated CXR image


def annotation_edit(request):
    raw_xray_obj = RawXray.objects.last()

    if raw_xray_obj:
        raw_cxray_name = raw_xray_obj.raw_cxray_name
        raw_cxray = raw_xray_obj.raw_cxray

        # Use raw_cxray_name and raw_cxray in your logic or pass to context for rendering
        context = {'raw_cxray_name': raw_cxray_name, 'raw_cxray': raw_cxray}
        return render(request, 'annotationEdit.html', context)
    else:
        # Handle case when RawXray object is not found
        pass

def download(request):
    
    return render(request, 'download.html')


 

