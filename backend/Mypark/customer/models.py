from django.db import models

# Create your models here.


class Ticket(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=50,default="dibas")
    routeId = models.IntegerField()
    bookedSeat = models.CharField(max_length=10,default="")
    vehicle_type = models.CharField(max_length=255, null=True, blank=True)
    payment = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    qr_code = models.CharField(max_length=500, null=True, blank=True)
    departureLocation = models.CharField(max_length=50, default="Kathmandu")
    destinationLocation = models.CharField(max_length=50, default="Pokhara")
    departureTime = models.TimeField(default='00:00:00')
    arrivalTime = models.TimeField(default='00:00:00')
    departureDate = models.DateField()
    vehicleID = models.CharField(max_length=50)
    booked_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.code