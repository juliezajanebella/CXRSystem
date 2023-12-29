from django.db import models

# Create your models here
class RawXray(models.Model): # for raw xray images
    raw_cxray_id = models.AutoField(primary_key=True, verbose_name='Raw CXray Image ID')
    raw_cxray_filename = models.CharField(max_length=100, verbose_name='Raw CXRay File Name')
    raw_cxray = models.FileField(upload_to="", verbose_name='Raw CXray Image')
    
    def __str__(self):
        return self.raw_cxray_id

class Radiologist(models.Model): # details of user (radiologists)
    radiologist_id = models.AutoField(primary_key=True, verbose_name='Radiologist ID')
    radiologist_username = models.CharField(max_length=100, verbose_name='Username')
    radiologist_firstname = models.CharField(max_length=100, verbose_name='First Name')
    radiologist_lastname = models.CharField(max_length=100, verbose_name='Last Name')
    radiologist_password = models.CharField(max_length=100, verbose_name='Password')
    radiologist_email = models.CharField(max_length=100, verbose_name='Email')

    def __str__(self):
        return self.radiologist_id + ' | ' + self.radiologist_username

    

                                      