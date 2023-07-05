from django.shortcuts import render
from .models import Breed



def breed_home(request):
    breeds = Breed.objects.order_by('id')
    return render(request, 'breed/get_all.html', {'breeds': breeds})
