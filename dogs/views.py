from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Dog
from .models import Breed




def dogs_update(request, dog_id):

    error = ''

    if request.method == 'POST':

        if request.POST.get("btn") == 'update':

            breed_name_ru = request.POST.get("breed")
            breed = Breed.objects.filter(name_ru=breed_name_ru).first()

            number = Dog.objects.filter(id=dog_id).update(
                breed_id = breed.id,
                region = request.POST.get("region"),
                rkf = request.POST.get("rkf"),
                birth_date = request.POST.get("birth_date"),
                is_male = request.POST.get("sex") == 'male',
                tattoo = request.POST.get("tattoo"),
                chip = request.POST.get("chip"),
                name_ru = request.POST.get("name_ru"),
                name_en = request.POST.get("name_en"),
                colour_ru = request.POST.get("colour_ru"),
                colour_en = request.POST.get("colour_en"),
                breeder = request.POST.get("breeder"),
                owner = request.POST.get("owner"),
                father_tattoo = request.POST.get("father_tattoo"),
                mother_tattoo = request.POST.get("mother_tattoo"),
                father_name = request.POST.get("father_name"),
                mother_name = request.POST.get("mother_name"),
                short_address = request.POST.get("short_address"),
            )
            
            return redirect('dogs_main')
        
    
    dogs = Dog.objects.order_by('-id')
    current_dog = Dog.objects.filter(id=dog_id).first()
    
    breed = Breed.objects.filter(id=current_dog.breed_id).first()
    current_breed = breed.name_ru

    # Подготовка русских названий пород
    breeds = Breed.objects.all()
    breed_ru_names = []
    for el in breeds:
        breed_ru_names.append(el.name_ru)
    del breeds  

    data = {
        'dogs': dogs,
        'error': error,
        'breed_ru_names': breed_ru_names,
        'dog': current_dog,
        'dog_id': dog_id,
        'dog_breed': current_breed,
        'dog_date': str(current_dog.birth_date)
    }

    return render(request, 'dogs/main.html', data)



def dogs_main(request):
    
    error = ''

    if request.method == 'POST' and request.POST.get("btn") == 'add':
        # form = DogsForm(request.POST)
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
        # sex = request.POST.get("sex")
        # print('sex', sex)

        dog = Dog()

        breed_name_ru = request.POST.get("breed")
        breed = Breed.objects.filter(name_ru=breed_name_ru).first()
        dog.breed_id = breed.id

        dog.rkf = request.POST.get("rkf")
        dog.region = request.POST.get("region")
        dog.birth_date = request.POST.get("birth_date")
        dog.is_male = request.POST.get("sex") == 'male'
        dog.tattoo = request.POST.get("tattoo")
        dog.chip = request.POST.get("chip")
        dog.name_ru = request.POST.get("name_ru")
        dog.name_en = request.POST.get("name_en")
        dog.colour_ru = request.POST.get("colour_ru")
        dog.colour_en = request.POST.get("colour_en")
        dog.breeder = request.POST.get("breeder")
        dog.owner = request.POST.get("owner")
        dog.father_tattoo = request.POST.get("father_tattoo")
        dog.mother_tattoo = request.POST.get("mother_tattoo")
        dog.father_name = request.POST.get("father_name"),
        dog.mother_name = request.POST.get("mother_name"),
        dog.short_address = request.POST.get("short_address"),
        dog.save()


    breeds = Breed.objects.all()
    breed_ru_names = []
    for el in breeds:
        breed_ru_names.append(el.name_ru)

    del breeds
    dogs = Dog.objects.order_by('-id')

    data = {
        'dogs': dogs,
        'error': error,
        'breed_ru_names': breed_ru_names
    }

    return render(request, 'dogs/main.html', data)