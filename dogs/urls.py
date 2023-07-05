from django.contrib import admin
from django.urls import path
from breed import views as breed_views
from dogs import views as dogs_views

urlpatterns = [
    path('', dogs_views.dogs_home, name='dogs_home'),
    path('create', dogs_views.create, name='dogs_create')    
]