from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim

# Create your views here.

def user_index(request):
    return render(request, 'customer/index.html')


# login 
def login(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_staff:
                # Redirect to a success page or return a success response
                message = "success"
                return redirect('owner')
            else:
                message = "success"
                return redirect('customer')
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
def location_search(request, query='Bike'):
    query = request.GET.get('query', '')
    if request.method == 'POST':
        location = request.POST['location']  # Use square brackets to access POST data
        geolocator = Nominatim(user_agent="http")
        location2 = geolocator.geocode(location)
        if location2:
            raw = location2.raw
            boundingBox = raw.get('boundingbox')
            return render(request, 'customer/index.html')
    
    return render(request, 'customer/index.html.html')