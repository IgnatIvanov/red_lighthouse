from django.contrib import admin
from django.urls import path
from event import views as events_views

urlpatterns = [
    # path('', dogs_views.dogs_home, name='dogs_home'),
    # path('create', dogs_views.create, name='dogs_create'),
    path('', events_views.events_main, name='events_main')    
]