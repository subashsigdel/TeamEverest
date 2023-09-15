from django.shortcuts import render

# Create your views here.


# admin site
def my_bookings(request):
    return render(request, 'open_park/Owner.html')