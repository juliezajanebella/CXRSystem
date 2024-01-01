# Create your views here.

# Request -> Response
# Action

import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages                           # alert messages
from django.contrib.auth.models import User
from .models import Radiologist, RawXray, AnnotatedImage
from CXRaide.functions import handle_uploaded_file
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
import os
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile
import uuid
from django.utils import timezone

# main functions
def create_acc(request):
    if request.method == 'POST':
    # input from user
        username = request.POST.get('username')    
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')          
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_password') 
        email = request.POST.get('email')

        # hash password
        hashed_password = make_password(password)

        # data from database
        Radiologist.objects.create(radiologist_username=username, radiologist_firstname=firstname, radiologist_lastname=lastname, radiologist_password=hashed_password, radiologist_email=email)
    return render(request, 'createAcc.html')

def user_login(request): 
    if request.method == 'POST':
        username = request.POST.get('username')              
        password = request.POST.get('password') 

        # Check for cxraide_admin
        cxraide_admin = authenticate(request, username=username, password=password)
        if cxraide_admin is not None:
            login(request, cxraide_admin)
            messages.success(request, 'CXRaide ADMIN')
            return redirect('admin/')

        # Check for radiologist
        radiologist = Radiologist.objects.filter(radiologist_username=username).first()
        if radiologist and check_password(password, radiologist.radiologist_password):
            # Correct password for Radiologist
            # Here, handle the login for Radiologist
            return redirect('home/')              

        # Invalid login credentials
        messages.error(request, 'Invalid Username or Password.')

    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def home(request):
    if request.method == 'POST':
        # fetching user input
        raw_cxray = request.FILES["raw_cxray"]
        filename, file_extension = os.path.splitext(raw_cxray.name)

        # calling the handler of uploaded file
        handle_uploaded_file(raw_cxray)
        RawXray.objects.create(raw_cxray_filename=filename, raw_cxray=raw_cxray)

        context = {'raw_cxray_filename': filename, 'raw_cxray': raw_cxray}
        return render(request, 'loadImage.html', context)
        
    return render(request, 'home.html')   # Return None if no file was uploaded


def change_image(request):
    if request.method == 'POST':
        # fetching user input
        updated_raw_cxray = request.FILES["raw_cxray"]
        updated_filename, file_extension = os.path.splitext(updated_raw_cxray.name)

        # calling the handler of uploaded file
        handle_uploaded_file(updated_raw_cxray)

        # fetching the latest created data in database
        latest_cxray = RawXray.objects.order_by('-raw_cxray_id').first()
        update = RawXray.objects.get(raw_cxray_filename=latest_cxray.raw_cxray_filename)
        update.raw_cxray_filename = updated_filename
        update.raw_cxray = updated_raw_cxray
        update.save()

        context = {'raw_cxray_filename': updated_filename, 'raw_cxray': updated_raw_cxray}
        return render(request, 'loadImage.html', context)
        
    return render(request, 'changeImage.html')

def annotation_edit(request):
    raw_xray_obj = RawXray.objects.last()

    if raw_xray_obj:
        raw_cxray_filename = raw_xray_obj.raw_cxray_filename
        raw_cxray = raw_xray_obj.raw_cxray

        # Use raw_cxray_name and raw_cxray in your logic or pass to context for rendering
        context = {'raw_cxray_filename': raw_cxray_filename, 'raw_cxray': raw_cxray}
        return render(request, 'annotationEdit.html', context)
    else:
        # Handle case when RawXray object is not found
        pass

def download(request):
    # Retrieve the latest annotated image
    annotated_image = AnnotatedImage.objects.order_by('-annotated_cxray_id').first()  # Assuming 'id' is your primary key field
    context = {'annotated_image': annotated_image}
    return render(request, 'download.html', context)

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data['annotated_cxray_id']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            # Create a unique file name using UUID and timestamp
            unique_filename = 'annotated_image_{}_{}.{}'.format(uuid.uuid4(), timezone.now().strftime("%Y%m%d%H%M%S"), ext)

            # Convert base64 image to ContentFile
            image_file = ContentFile(base64.b64decode(imgstr), name=unique_filename)
            
            # Save the image to the ImageField
            annotated_image = AnnotatedImage()
            annotated_image.image.save(unique_filename, image_file, save=True)

            return JsonResponse({'message': 'Image saved successfully!'})
        except Exception as e:
            # Log the error here
            return JsonResponse({'error': 'Failed to save image', 'details': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)


 

