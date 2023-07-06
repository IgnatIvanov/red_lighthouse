from django.urls import path
from participant import views as part_views

urlpatterns = [
    path('', part_views.part_main, name='part_main')    
]