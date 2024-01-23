# Create your views here.

# Request -> Response
# Action

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages                          
from .models import Radiologist, RawXray, AnnotatedImage, AnnotatedImageByAi
from CXRaide.functions import handle_uploaded_file
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
import tensorflow as tf
import numpy as np
from PIL import Image, ImageDraw
import io
import base64
from django.conf import settings


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
    annotated_image_raw = AnnotatedImage.objects.last()
    annotated_image_ai = AnnotatedImageByAi.objects.last()

    context = {}

    if annotated_image_raw:
        annotated_cxray = annotated_image_raw.annotated_cxray

        # Add raw_cxray_name and raw_cxray to the context
        context.update({
            'annotated_cxray': annotated_cxray
        })

    if annotated_image_ai:
        annotated_cxray_ai = annotated_image_ai.annotated_cxray_ai

        # Add raw_cxray_name_ai and raw_cxray_ai to the context
        context.update({
            'annotated_cxray_ai': annotated_cxray_ai
        })
    return render(request, 'download.html', context)

def download_expert_image(request, filename):
    # Complete file path
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Check if file exists
    if os.path.exists(file_path):
        # Open the file for reading in binary mode
        with open(file_path, 'rb') as fh:
            # Set the MIME type to image/jpeg or the correct MIME type for your file
            response = HttpResponse(fh.read(), content_type="image/jpeg")
            # Set the Content-Disposition header to force download
            response['Content-Disposition'] = 'attachment; filename="' + os.path.basename(file_path) + '"'
            return response
    else:
        # Return a 404 Not Found response if the file doesn't exist
        return HttpResponse("File not found", status=404)

def download_ai_image(request, filename):
    # Complete file path
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Check if file exists
    if os.path.exists(file_path):
        # Open the file for reading in binary mode
        with open(file_path, 'rb') as fh:
            # Set the MIME type to image/jpeg or the correct MIME type for your file
            response = HttpResponse(fh.read(), content_type="image/jpeg")
            # Set the Content-Disposition header to force download
            response['Content-Disposition'] = 'attachment; filename="' + os.path.basename(file_path) + '"'
            return response
    else:
        # Return a 404 Not Found response if the file doesn't exist
        return HttpResponse("File not found", status=404)

@csrf_exempt
def save_image_annotated(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data', None)

        if image_data:
            # Strip the header of the data URL
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1] 

            # Decode the base64 data
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) 
            
            annotated_image = AnnotatedImage()
            annotated_image.annotated_cxray_filename = "CXRaide-Annotated-Image-By-Expert." + ext
            annotated_image.annotated_cxray.save(annotated_image.annotated_cxray_filename, data, save=True)

            return JsonResponse({'message': 'Image saved successfully.'})
        else:
            return JsonResponse({'message': 'No image data provided.'}, status=400)
    return JsonResponse({'message': 'Invalid request method.'}, status=400)


# FOR AI MODEL
def load_label_map(label_map_path):
    label_map = {}
    with open(label_map_path, 'r') as file:
        for line in file:
            if "id:" in line:
                id = int(line.split(': ')[1])
                label_map[id] = next(file).split(': ')[1].replace('\n', '').replace("'", "")
    return label_map

def draw_detections(image_np, detections, label_map):
    image = Image.fromarray(image_np)
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size

    # Processing detections
    detection_boxes = detections['detection_boxes'][0].numpy()
    detection_classes = detections['detection_classes'][0].numpy().astype(np.int64)
    detection_scores = detections['detection_scores'][0].numpy()

    for i in range(len(detection_scores)):
        if detection_scores[i] < 0.1:  # Set a threshold
            continue

        # Bounding box and label drawing
        ymin, xmin, ymax, xmax = detection_boxes[i]
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
        draw.rectangle([(left, top), (right, bottom)], outline=(0, 100, 0), width=4)
        object_name = label_map[detection_classes[i]]
        draw.text((left, top), object_name, fill=(139, 0, 0))

    # Return the image
    return image

@csrf_exempt
@require_POST
def ai_annotation(request):
    # Load the TensorFlow model and label map (use your paths)
    # Updated paths
    SAVED_MODEL_PATH = os.path.join('./static/models/saved_model')
    LABEL_MAP_PATH = os.path.join('./static/models/label_map2.pbtxt')
    model = tf.saved_model.load(SAVED_MODEL_PATH)
    label_map = load_label_map(LABEL_MAP_PATH)

    # Get the image from the request
    image_data = request.FILES['image'].read()
    image_np = np.array(Image.open(io.BytesIO(image_data)).convert("RGB"))

    # Prepare the image for inference
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run inference
    detections = model(input_tensor)

    # Process detections and draw annotations
    annotated_image = draw_detections(image_np, detections, label_map)

    # After drawing the detections:
    annotated_image = draw_detections(image_np, detections, label_map)

    # Convert the annotated image to bytes
    buffered = io.BytesIO()
    annotated_image.save(buffered, format="PNG")
    annotated_image_data = buffered.getvalue()

    # Save the annotated image to AnnotatedImageByAi model
    annotated_image_instance = AnnotatedImageByAi()
    filename = "CXRaide-Annotated-Image-By-AI.png"
    annotated_image_instance.annotated_cxray_filename_ai = filename
    annotated_image_instance.annotated_cxray_ai.save(filename, ContentFile(annotated_image_data), save=True)

    # Return the annotated image as JSON response
    # return JsonResponse({'image_data': annotated_image_data.decode('latin-1')})
    # Return the annotated image as a file
    # Return the annotated image as a file
    response = HttpResponse(annotated_image_data, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response