from django.db import models

# Create your models here
class RawXray(models.Model): # for raw xray images
    raw_cxray_id = models.AutoField(primary_key=True, verbose_name='Raw CXray Image ID')
    raw_cxray_name = models.CharField(max_length=100, unique=True, verbose_name='Raw CXRay Name')
    raw_cxray = models.FileField(upload_to="", verbose_name='Raw CXray Image')
    
    def __str__(self):
        return self.raw_cxray_id

class Radiologist(models.Model): # details of user (radiologists)
    radiologist_id = models.AutoField(primary_key=True, verbose_name='Radiologist ID')
    radiologist_name = models.CharField(max_length=100, verbose_name='Name')
    radiologist_email = models.CharField(max_length=100, verbose_name='Email')
    radiologist_username = models.CharField(max_length=100, verbose_name='Username')
    radiologist_password = models.CharField(max_length=100, verbose_name='Password')

    def __str__(self):
        return self.radiologist_id + ' | ' + self.radiologist_name

    

                                      