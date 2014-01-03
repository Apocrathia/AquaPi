from django.contrib import admin

# Import your models here
from main.models import Device, Sensor

# Register your models here.
admin.site.register(Device, Sensor)
