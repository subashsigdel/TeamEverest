from django.contrib import admin
from customer.models import Ticket
from open_park.models import Parking, KYC
# Register your models here.


admin.site.register(Ticket)
admin.site.register(Parking)
admin.site.register(KYC)