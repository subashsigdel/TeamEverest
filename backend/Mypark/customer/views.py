import uuid 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login 
from django.http import HttpResponse
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from open_park.models import Parking, KYC
from geopy.distance import geodesic
from django.contrib import messages

# Create your views here.

def user_index(request):
    return render(request, 'customer/index.html')


def login(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            try:
                # Check if the user has a related Parking entry
                parking = Parking.objects.get(owner=user)
                kyc = KYC.objects.get(parking_code=parking.code)

                if not parking.code or not kyc:
                    # If either parking or KYC is incomplete, redirect to the respective registration page
                    message = "Complete the required forms"
                    if not parking.code:
                        return redirect('register_parking')
                    else:
                        return redirect('register_kyc')

            except Parking.DoesNotExist:
                # If the user doesn't have a related Parking entry, redirect to register parking
                message = "Complete form"
                return redirect('register_parking')

            # If all conditions are met, redirect to owner_dashboard
            message = "Success"
            return redirect('owner_dashboard')

        else:
            # Return an error response or render the login page with an error message
            message = "Incorrect Username or Password"

    context = {
        'message': message
    }
    
    # Handle GET request (display the login form)
    return render(request, 'customer/login.html', context)


# For park owner
def owner(request):
    pass


# For customer

def customer_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            error_message = "Username already taken."
        else:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.save()

            # Authenticate and log in the user
            user = authenticate(username=username, password=password)
            login(request, user)

            # Redirect to a success page or home page
            return redirect('home')  # Replace 'home' with your desired URL name

    else:
        error_message = ""

    return render(request, 'customer/register.html', {'error_message': error_message})


# search
def search(request):
    # query = request.GET("location")
    # if request.user.is_authenticated:
    #     return render(request, 'customer/search.html', {'query': query})
    # else:
    return render(request, 'customer/search.html')

# Choose location
def choose_location(request):
    return render(request, 'customer/choose_location.html')

# User Search Location 
def location_search(request):
    if request.method == 'POST':
        location = request.POST['location']
        geolocator = Nominatim(user_agent="http")
        location2 = geolocator.geocode(location)
        
        if location2:
            user_latitude = location2.latitude
            user_longitude = location2.longitude
            search_radius_km = 5  # Adjust this as needed
            parkings_within_radius = []

            all_parkings = Parking.objects.all()

            for parking in all_parkings:
                parking_latitude = parking.latitude
                parking_longitude = parking.longitude
                distance_km = geodesic((user_latitude, user_longitude), (parking_latitude, parking_longitude)).kilometers

                if distance_km <= search_radius_km:
                    try:
                        kyc = KYC.objects.get(parking_code=parking.code)
                        parking.kyc_name = kyc.name
                        parking.kyc_address = kyc.address
                    except KYC.DoesNotExist:
                        parking.kyc_name = None
                        parking.kyc_address = None

                    parkings_within_radius.append(parking)
            return render(request, 'customer/map.html', {'parkings': parkings_within_radius})

    return render(request, 'customer/search.html')
    



# for map
def select_park(request):
    return render(request, 'customer/map.html')


# owner register
def register_owner_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # first_name = request.POST['first_name']
        if password==password1:
            is_staff = True

            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                error_message = "Username already taken."
            else:
                # Create a new user
                user = User.objects.create_user(username=username, password=password)
                # user.first_name = first_name
                user.is_staff = is_staff
                user.save()

                # Authenticate and log in the user
                user = authenticate(username=username, password=password)
                auth_login(request, user)

                # Redirect to a success page or home page
                return redirect('register_parking')  
        else:
            error_message = "Password Should be matched !"
    else:
        error_message = ""

    return render(request, 'customer/owner1.html', {'error_message': error_message})


def register_owner_parking(request):
    if request.method == 'POST':
        # Extract data from the POST request
        code = str(uuid.uuid4().hex[:8])  
        owner = request.user 
        car_slot = int(request.POST.get('car_slot', 0))
        bike_slot = int(request.POST.get('bike_slot', 0))
        car_charge = int(request.POST.get('car_charge', 0))
        bike_charge = int(request.POST.get('bike_charge', 0))
        opening_time = request.POST.get('opening_time')
        close_time = request.POST.get('close_time')
        full_time = bool(request.POST.get('full_time', False))
        parking_type = request.POST.get('parking_type')
        latitude = float(request.POST.get('latitude', 0))
        longitude = float(request.POST.get('longitude', 0))
        image = request.FILES.get('image')
        status = bool(request.POST.get('status', False))

        # Create a new Parking object and save it
        parking = Parking(
            code=code,
            owner=owner,
            car_slot=car_slot,
            bike_slot=bike_slot,
            car_charge=car_charge,
            bike_charge=bike_charge,
            opening_time=opening_time,
            close_time=close_time,
            full_time=full_time,
            parking_type=parking_type,
            latitude=latitude,
            longitude=longitude,
            image=image,
            status=status
        )
        parking.save()

        messages.success(request, 'Parking registered successfully.')
        return redirect('register_kyc')  # Redirect to the parking list page


    return render(request, 'customer/owner2.html')


def register_owner_kyc(request):
    message = None

    if request.method == 'POST':
        # Extract data from request.POST
        parking_code = Parking.objects.filter(
            owner=request.user).values_list('code', flat=True)
        citizenship_id = request.POST.get('citizenship_id')
        name = request.POST.get('name')
        image = request.FILES.get('image')
        phone = request.POST.get('phone')
        document_type = request.POST.get('document_type')
        address = request.POST.get('address')
        profile = request.FILES.get('profile')

        # Create a KYC entry
        kyc = KYC(
            parking_code=parking_code,
            citizenship_id=citizenship_id,
            name=name,
            image=image,
            phone=phone,
            document_type = document_type,
            address = address,
            profile=profile
        )
        kyc.save()

        messages.success(request, 'KYC registered successfully.')
        return redirect('owner_dashboard')  # Redirect to the KYC list page or another appropriate page

    context = {
        'message': message,
    }
    
    return render(request, 'customer/owner3.html', context)


#QR code
def qr_generator(request):
    return render(request, 'customer/')