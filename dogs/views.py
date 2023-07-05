from django.shortcuts import render, redirect
from .models import Dog
from .forms import DogsForm
from .models import Breed



def dogs_home(request):
    dogs = Dog.objects.order_by('id')
    return render(request, 'dogs/get_all.html', {'dogs': dogs})


def create(request):
    error = ''
    if request.method == 'POST':
        form = DogsForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect('dogs_home')
        # else:
        #     error = 'Форма заполнена неверно'
        # Так можно брать значения породы для подстановки
        print(request.POST.get("breed"))

    form = DogsForm()
    breeds = Breed.objects.all()
    breed_ru_names = []
    # print(breed_ru_names.get('name_ru'))
    for el in breeds:
        # print(el.name_ru)
        breed_ru_names.append(el.name_ru)

    del breeds

    data = {
        'form': form,
        'error': error,
        'breed_ru_names': breed_ru_names
    }

    return render(request, 'dogs/create.html', data)