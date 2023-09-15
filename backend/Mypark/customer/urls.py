from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_index, name="user_index"),
    path('login', views.login, name="login"),
    path('register', views.customer_registration, name="register"),
    
]