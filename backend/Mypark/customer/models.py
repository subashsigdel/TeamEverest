from django.db import models
from open_park.models import Parking
# Create your models here.


def upload_qr(instance, filename):
    return "static/pictures/{id}_{host_to}/{filename}".format(host_to=instance.code, filename=filename,
                                                             id=instance.id)


class Ticket(models.Model):
    parking_code = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=50,default="dibas")
    bookedSeat = models.CharField(max_length=10,default="")
    vehicle_type = models.CharField(max_length=255, null=True, blank=True)
    payment = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    qr_code = models.ImageField(upload_to=upload_qr, null=True, blank=True)
    fine = models.IntegerField(null=True, blank=True)
    departureTime = models.TimeField(default='00:00:00')
    arrivalTime = models.TimeField(default='00:00:00')
    departureDate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    vehicleID = models.CharField(max_length=50)
    booked_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.code