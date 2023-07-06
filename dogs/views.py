from django.shortcuts import render, redirect
from .models import Dog
from .forms import DogsForm
from .models import Breed



# Не будет использоваться в будущем
# def dogs_home(request):
#     dogs = Dog.objects.order_by('id')
#     return render(request, 'dogs/get_all.html', {'dogs': dogs})


# Не будет использоваться в будущем
# def create(request):
#     error = ''
#     if request.method == 'POST':
#         form = DogsForm(request.POST)
#         # if form.is_valid():
#         #     form.save()
#         #     return redirect('dogs_home')
#         # else:
#         #     error = 'Форма заполнена неверно'
#         # Так можно брать значения породы для подстановки
#         breed_name_ru = request.POST.get("breed")
#         breed = Breed.objects.filter(name_ru=breed_name_ru).first()
#         breed_id = breed.id
#         print('breed_id', breed_id)

#     form = DogsForm()
#     breeds = Breed.objects.all()
#     breed_ru_names = []
#     # print(breed_ru_names.get('name_ru'))
#     for el in breeds:
#         # print(el.name_ru)
#         breed_ru_names.append(el.name_ru)

#     del breeds

#     data = {
#         'form': form,
#         'error': error,
#         'breed_ru_names': breed_ru_names
#     }

#     return render(request, 'dogs/create.html', data)


def dogs_main(request):
    
    error = ''
    if request.method == 'POST':
        form = DogsForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect('dogs_home')
        # else:
        #     error = 'Форма заполнена неверно'
        # Так можно брать значения породы для подстановки
        # breed_name_ru = request.POST.get("breed")
        # breed = Breed.objects.filter(name_ru=breed_name_ru).first()
        # breed_id = breed.id
        # print('breed_id', breed_id)
        sex = request.POST.get("sex")
        # print('sex', sex)

        dog = Dog()

        breed_name_ru = request.POST.get("breed")
        breed = Breed.objects.filter(name_ru=breed_name_ru).first()
        dog.breed_id = breed.id

        dog.rkf = request.POST.get("rkf")
        dog.region = request.POST.get("region")
        dog.birth_date = request.POST.get("birth_date")

        sex = request.POST.get("sex")
        if sex == 'male':
            dog.is_male = True
        else:
            dog.is_male = False

        dog.tattoo = request.POST.get("tattoo")
        dog.chip = request.POST.get("chip")
        dog.name_ru = request.POST.get("name_ru")
        dog.name_en = request.POST.get("name_en")
        dog.colour_ru = request.POST.get("colour_ru")
        dog.colour_en = request.POST.get("colour_en")
        dog.breeder_id = request.POST.get("breeder_id")
        dog.owner_id = request.POST.get("owner_id")
        dog.father_id = request.POST.get("father_id")
        dog.mother_id = request.POST.get("mother_id")
        dog.save()
        

    form = DogsForm()
    breeds = Breed.objects.all()
    breed_ru_names = []
    # print(breed_ru_names.get('name_ru'))
    for el in breeds:
        # print(el.name_ru)
        breed_ru_names.append(el.name_ru)

    del breeds
    dogs = Dog.objects.order_by('id')

    data = {
        'dogs': dogs,
        'form': form,
        'error': error,
        'breed_ru_names': breed_ru_names
    }

    return render(request, 'dogs/main.html', data)