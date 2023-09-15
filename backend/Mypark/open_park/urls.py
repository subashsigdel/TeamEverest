from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_bookings, name="bookings"),
    path('bookings/car', views.my_car_bookings, name="my_car_bookings"),
    
]