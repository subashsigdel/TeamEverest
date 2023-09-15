from django.shortcuts import render, redirect
from .models import *
from customer.models import Ticket
# Create your views here.


# admin site
def my_bookings(request):
    if request.user.is_authenticated:
        current_user = request.user
        if current_user.is_staff:
            parking = Ticket.objects.filter()
    else:
        return redirect('login')
    return render(request, 'open_park/Owner.html')