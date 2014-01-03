# bring in the django module
from django.db import models

# now bring in the Arduino module
from Arduino import Arduino

# Create your models here.
class Device(models.Model): # Outputs
	digital = models.BooleanField()
	analog = models.BooleanField()
	pin = models.IntegerField()
	name = models.CharField()

class Sensor(models.Model): # Inputs
        digital = models.BooleanField()
        analog = models.BooleanField()
        pin = models.IntegerField()
        name = models.CharField()
