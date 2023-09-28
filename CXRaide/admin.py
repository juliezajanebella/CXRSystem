from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

# Remove the uncessary features
admin.site.unregister(Group)
admin.site.site_url = False

# Changes to make it like CXRaide Admin System
admin.site.site_header = "CXRaide System Admin"
admin.site.site_title = "CXRaide System Admin"
admin.site.index_title = "Welcome to the CXRaide System Admin Area"
    
admin.site.register(RawXray)
admin.site.register(Radiologist)

