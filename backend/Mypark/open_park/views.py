import random
import string
from django.shortcuts import render, redirect
from .models import *
from customer.models import Ticket
from django.db.models import Sum
from datetime import date, timedelta
from django.db.models import DateField
from django.db.models.functions import Trunc
# Create your views here.


# admin site
def my_bookings(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Get all parking codes owned by the logged-in staff member
        owner_parking_codes = Parking.objects.filter(
            owner=request.user).values_list('code', flat=True)

        # Find all tickets that match the parking_code in the owner's parking codes
        parking_tickets = Ticket.objects.filter(
            parking_code__in=owner_parking_codes)
    else:
        return redirect('login')

    return render(request, 'open_park/Owner.html', {'parking_tickets': parking_tickets})


# Car Bookings
def my_car_bookings(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Get all parking codes owned by the logged-in staff member
        owner_parking_codes = Parking.objects.filter(
            owner=request.user).values_list('code', flat=True)
        print(owner_parking_codes)

        # Find all tickets that match the parking_code in the owner's parking codes
        parking_tickets = Ticket.objects.filter(
            parking_code__in=owner_parking_codes, vehicle_type='Car')
        print(parking_tickets)
    else:
        return redirect('login')

    return render(request, 'open_park/car.html', {'parking_tickets': parking_tickets})


# Bike Bookings
def my_bike_bookings(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Get all parking codes owned by the logged-in staff member
        owner_parking_codes = Parking.objects.filter(
            owner=request.user).values_list('code', flat=True)
        print(owner_parking_codes)

        # Find all tickets that match the parking_code in the owner's parking codes
        parking_tickets = Ticket.objects.filter(
            parking_code__in=owner_parking_codes, vehicle_type='Bike')
        print(parking_tickets)
    else:
        return redirect('login')

    return render(request, 'open_park/bike.html', {'parking_tickets': parking_tickets})


# Active Bookings
def my_active_bookings(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Get all parking codes owned by the logged-in staff member
        owner_parking_codes = Parking.objects.filter(
            owner=request.user).values_list('code', flat=True)
            
        # Find all tickets that match the parking_code in the owner's parking codes
        parking_tickets = Ticket.objects.filter(
            parking_code__in=owner_parking_codes, status='Booked')
        print(parking_tickets)
    else:
        return redirect('login')

    return render(request, 'open_park/booking.html', {'parking_tickets': parking_tickets})


# Owner Dashboard
def owner_dashboard(request):
    if request.user.is_staff:
        # Get the parking codes owned by the logged-in staff member
        owner_parking_codes = Parking.objects.filter(
            owner=request.user).values_list('code', flat=True)
        
        # Total bikes
        total_bikes = Ticket.objects.filter(
            parking_code__in=owner_parking_codes, vehicle_type='Bike', status="Booked").count()
        total_cars = Ticket.objects.filter(
            parking_code__in=owner_parking_codes, vehicle_type='Car', status="Booked").count()
        
        # Get the total car slots and bike slots from Parking
        total_car_slots = Parking.objects.aggregate(total_car_slots=Sum('car_slot'))['total_car_slots'] or 0
        total_bike_slots = Parking.objects.aggregate(total_bike_slots=Sum('bike_slot'))['total_bike_slots'] or 0
        
        # Calculate the total booked car slots and bike slots
        total_booked_cars = Ticket.objects.filter(parking_code__in=Parking.objects.values('code'), vehicle_type='Car', status='Booked').count()
        total_booked_bikes = Ticket.objects.filter(parking_code__in=Parking.objects.values('code'), vehicle_type='Bike', status='Booked').count()
        
        # Calculate the total available car slots and bike slots
        available_car_slots = total_car_slots - total_booked_cars
        available_bike_slots = total_bike_slots - total_booked_bikes

        # Apply the conversion factor to calculate equivalent car slots from bikes
        equivalent_bike_slots_from_cars = available_car_slots * 4

        # Calculate the total available car slots considering equivalent car slots from bikes
        total_available_bike_slots = available_bike_slots + equivalent_bike_slots_from_cars

        # Calculate the available slot percentage
        if total_bike_slots > 0:
            available_slot_percentage = 100 - ((equivalent_bike_slots_from_cars + total_booked_bikes)/ total_bike_slots) * 100
        else:
            available_slot_percentage = 0


        # Calculate the date 7 days ago from today
        end_date = date.today()
        start_date = end_date - timedelta(days=6)

        # Initialize empty lists for dates and daily total amounts
        dates = []
        daily_total_amounts = []

        # Query the database to get daily revenue data for the past 7 days for the owner
        current_day = start_date
        while current_day <= end_date:
            daily_revenue = (
                Ticket.objects
                .filter(parking_code__in=owner_parking_codes)
                .annotate(booked_date_date=Trunc('booked_date', 'day', output_field=DateField()))
                .filter(booked_date_date=current_day)
                .aggregate(daily_total=Sum('amount'))['daily_total'] or 0
            )
            dates.append(current_day.strftime('%Y-%m-%d'))
            daily_total_amounts.append(daily_revenue)
            current_day += timedelta(days=1)

        print(dates,)
        print(daily_total_amounts)
        return render(request, 'open_park/Owner.html', {
            'dates': dates,
            'daily_total_amounts': daily_total_amounts,
            'total_cars': total_cars,
            'total_bikes': total_bikes,
            'available_slot_percentage': available_slot_percentage,
        })
    else:
        return redirect('login')

