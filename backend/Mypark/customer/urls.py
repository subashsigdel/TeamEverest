from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_index, name="user_index"),
    path('login', views.login, name="login"),
    path('register', views.customer_registration, name="register"),
    path('location', views.search, name="search"),
    path('parkings', views.location_search, name="locations"),
    path('location/choose', views.choose_location, name="choose_location"),
]