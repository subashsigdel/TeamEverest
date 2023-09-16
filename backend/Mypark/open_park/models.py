from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# Upload profile picture
def upload_parking_picture(instance, filename):
    return "static/pictures/{id}_{host_to}/{filename}".format(host_to=instance.name, filename=filename,
                                                             id=instance.id)

# upload parking picture
def upload_parking_picture(instance, filename):
    return "static/pictures/{id}_{host_to}/{filename}".format(host_to=instance.code, filename=filename,
                                                             id=instance.id)



# upload image with 
def upload_kyc_picture(instance, filename):
    return "static/pictures/{id}_{host_to}/{filename}".format(host_to=instance.name, filename=filename,
                                                             id=instance.id)


# Parking space detail
class Parking(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    owner= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car_slot = models.IntegerField(null=True, blank=True)
    bike_slot = models.IntegerField(null=True, blank=True)
    car_charge = models.IntegerField(null=True, blank=True)
    bike_charge = models.IntegerField(null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    full_time = models.BooleanField(null=True, blank=True, default=False)
    parking_type = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_parking_picture, null=True, blank=True)
    status = models.BooleanField(default=False, blank=True, null=True)


    def __str__(self):
        return self.code
    

# KYC of Owner
class KYC(models.Model):
    parking_code = models.CharField(max_length=255, null=True, blank=True)
    citizenship_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_kyc_picture)
    phone = models.IntegerField(null=True, blank=True)
    profile = models.ImageField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    document_type = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.name
