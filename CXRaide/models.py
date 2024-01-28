from django.db import models

# Create your models here
class Radiologist(models.Model): # details of user (radiologists)
    radiologist_id = models.AutoField(primary_key=True, verbose_name='Radiologist ID')
    radiologist_username = models.CharField(max_length=100, verbose_name='Username')
    radiologist_firstname = models.CharField(max_length=100, verbose_name='First Name')
    radiologist_lastname = models.CharField(max_length=100, verbose_name='Last Name')
    radiologist_password = models.CharField(max_length=100, verbose_name='Password')
    radiologist_email = models.CharField(max_length=100, verbose_name='Email')

    def __str__(self):
        return self.radiologist_id + ' | ' + self.radiologist_username

class RawXray(models.Model): # for raw xray images
    raw_cxray_id = models.AutoField(primary_key=True, verbose_name='Raw CXray Image ID')
    raw_cxray_filename = models.CharField(max_length=100, verbose_name='Raw CXRay File Name')
    raw_cxray_image = models.FileField(upload_to="raw_images/", verbose_name='Raw CXray Image')
    
    def __str__(self):
        return self.raw_cxray_filename

class AnnotatedImage(models.Model):
    annotated_cxray_id = models.AutoField(primary_key=True, verbose_name='Annotated CXray Image ID')
    annotated_cxray_filename = models.CharField(max_length=100, verbose_name='Annotated CXRay File Name')
    annotated_cxray_image = models.ImageField(upload_to='annotated_images/', verbose_name='Annotated CXray Image')

    def __str__(self):
        return self.annotated_cxray_filename
    
class AnnotatedImageByAi(models.Model):
    annotated_cxray_id_ai = models.AutoField(primary_key=True, verbose_name='Annotated CXray Image By AI ID')
    annotated_cxray_filename_ai = models.CharField(max_length=100, verbose_name='Annotated CXRay By AI File Name')
    annotated_cxray_ai_image = models.ImageField(upload_to='annotated_images/', verbose_name='Annotated CXray Image By AI')

    def __str__(self):
        return self.annotated_cxray_filename_ai

    

                                      