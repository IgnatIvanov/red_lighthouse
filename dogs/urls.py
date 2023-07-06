from django.urls import path
from dogs import views as dogs_views

urlpatterns = [
    path('', dogs_views.dogs_main, name='dogs_main')    
]