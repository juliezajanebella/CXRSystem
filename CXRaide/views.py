# Create your views here.

# Request -> Response
# Action

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages                          
from .models import Radiologist, RawXray, AnnotatedImage, AnnotatedImageByAi
# from CXRaide.functions import handle_uploaded_file
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
from weasyprint import HTML
from django.template.loader import render_to_string



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

def profile(request):
    return render(request, 'profile.html')

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
        # handle_uploaded_file(raw_cxray)
        RawXray.objects.create(raw_cxray_filename=filename, raw_cxray_image=raw_cxray)

        context = {'raw_cxray_filename': filename, 'raw_cxray': raw_cxray}
        return render(request, 'loadImage.html', context)
    return render(request, 'home.html')   # Return None if no file was uploaded

# Pass    
def change_pass(request):
    # if request.method == 'POST':
    #     password = request.POST['password']
    #     new_pass = request.POST['new_password']
    #     confnew_pass = request.POST['confirm_new_password']
        

    #     if Radiologist.objects.filter(radiologist_password=password).exists():
    #         if new_pass == confnew_pass:
    #             # Get the first radiologist object with the given password
    #             radiologist = Radiologist.objects.filter(radiologist_password=password).first()
    #             # Update the password field
    #             radiologist.radiologist_password = new_pass
    #             # Save the changes to the database
    #             radiologist.save()
                
    #             messages.success(request, 'You successfully change your password. You can now login again.')
    #             return render(request, 'changePass.html')
    #         else:
    #             messages.error(request, 'Password and Confirm Password do not match. Please try again.')  
    #     else:
    #         messages.error(request, 'Old Password is incorrect. Please try again.')               
    # # Return the newPass.html template for GET requests
    return render(request, 'changePass.html')

def change_image(request):
    if request.method == 'POST':
        # fetching user input
        updated_raw_cxray = request.FILES["raw_cxray"]
        updated_filename, file_extension = os.path.splitext(updated_raw_cxray.name)

        # # calling the handler of uploaded file
        # handle_uploaded_file(updated_raw_cxray)

        # fetching the latest created data in database
        latest_cxray = RawXray.objects.order_by('-raw_cxray_id').first()
        update = RawXray.objects.get(raw_cxray_filename=latest_cxray.raw_cxray_filename)
        update.raw_cxray_filename = updated_filename
        update.raw_cxray_image = updated_raw_cxray
        update.save()

        context = {'raw_cxray_filename': updated_filename, 'raw_cxray': updated_raw_cxray}
        return render(request, 'loadImage.html', context)
    return render(request, 'changeImage.html')

def annotation_edit(request):
    raw_xray_obj = RawXray.objects.last()

    if raw_xray_obj:
        raw_cxray_filename = raw_xray_obj.raw_cxray_filename
        raw_cxray = raw_xray_obj.raw_cxray_image

        # Use raw_cxray_name and raw_cxray in your logic or pass to context for rendering
        context = {'raw_cxray_filename': raw_cxray_filename, 'raw_cxray': raw_cxray}
        return render(request, 'annotationEdit.html', context)
    else:
        # Handle case when RawXray object is not found
        pass

def download(request):
    annotated_image_expert = AnnotatedImage.objects.last()
    annotated_image_ai = AnnotatedImageByAi.objects.last()

    context = {}

    if annotated_image_expert:
        annotated_cxray = annotated_image_expert.annotated_cxray_image

        # Add raw_cxray_name and raw_cxray to the context
        context.update({
            'annotated_cxray': annotated_cxray
        })

    if annotated_image_ai:
        annotated_cxray_ai = annotated_image_ai.annotated_cxray_ai_image

        # Add raw_cxray_name_ai and raw_cxray_ai to the context
        context.update({
            'annotated_cxray_ai': annotated_cxray_ai
        })
    return render(request, 'download.html', context)

def download_expert_image(request, filename):
    # Complete file path
    today_str = datetime.now().strftime('%Y-%m-%d')
    file_path = os.path.join("CXRaide/static/upload/annotated-images/", today_str, filename)

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
    today_str = datetime.now().strftime('%Y-%m-%d')
    file_path = os.path.join("CXRaide/static/upload/annotated-images/", today_str, filename)

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
    
def download_pdf_expert_image(request):
    annotated_image_expert = AnnotatedImage.objects.last()

    context = {}

    if annotated_image_expert:
        annotated_cxray = annotated_image_expert.annotated_cxray_image

        context.update({
            'annotated_cxray': annotated_cxray
        })

    # Render the HTML template with the image URLs and other context data
    html_string = render_to_string('CXRaide/includes/document.html', context, request=request)

    # Create a WeasyPrint HTML object and then generate a PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    # Create an HTTP response with the PDF file
    response = HttpResponse(pdf, content_type='application/pdf')
    # Content-Disposition header to make the browser download the PDF
    response['Content-Disposition'] = 'attachment; filename="annotated_chest_xrays_annotated-by-expert.pdf"'

    return response

def download_pdf_ai_image(request):
    annotated_image_ai = AnnotatedImageByAi.objects.last()
    
    context = {}

    if annotated_image_ai:
        annotated_cxray_ai = annotated_image_ai.annotated_cxray_ai_image

        context.update({
            'annotated_cxray_ai': annotated_cxray_ai
        })

    # Render the HTML template with the image URLs and other context data
    html_string = render_to_string('CXRaide/includes/document.html', context, request=request)

    # Create a WeasyPrint HTML object and then generate a PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    # Create an HTTP response with the PDF file
    response = HttpResponse(pdf, content_type='application/pdf')
    # Content-Disposition header to make the browser download the PDF
    response['Content-Disposition'] = 'attachment; filename="annotated_chest_xrays_ai-generated.pdf"'

    return response

def get_today_folder_path():
    # Get the current date as a string formatted as 'MM-DD-YYYY'
    date_str = datetime.now().strftime('%m-%d-%Y')
    # Create the directory path
    return (date_str)

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

            # Create the folder path for today's date
            today_folder_path = get_today_folder_path()
            # os.makedirs(today_folder_path, exist_ok=True)

       
            # Define the filename with the directory
            filename = os.path.join(today_folder_path, "CXRaide-Annotated-Image-By-Experts.jpg")

            annotated_image = AnnotatedImage()
            annotated_image.annotated_cxray_filename = filename
            annotated_image.annotated_cxray_image.save(filename, data, save=True)

            return JsonResponse({'message': 'Image saved successfully.'})
        else:
            return JsonResponse({'message': 'No image data provided.'}, status=400)
    else:
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

    # Convert the annotated image to bytes
    buffered = io.BytesIO()
    annotated_image.save(buffered, format="JPEG")
    annotated_image_data = buffered.getvalue()

    # Create the folder path for today's date
    today_folder_path = get_today_folder_path()
    # os.makedirs(today_folder_path, exist_ok=True)

    # Define the filename with the directory
    filename = os.path.join(today_folder_path, "CXRaide-Annotated-Image-By-AI.jpg")

    # Save the annotated image to AnnotatedImageByAi model
    annotated_image_instance = AnnotatedImageByAi()
    annotated_image_instance.annotated_cxray_filename_ai = filename
    annotated_image_instance.annotated_cxray_ai_image.save(filename, ContentFile(annotated_image_data), save=True)

    # Return the annotated image as a file
    response = HttpResponse(annotated_image_data, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="' + os.path.basename(filename) + '"'
    return response
