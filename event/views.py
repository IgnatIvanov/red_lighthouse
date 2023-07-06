from django.shortcuts import render
from .models import Event
from .forms import EventsForm
from classes.models import DogClass



def events_main(request):

    error = ''
    if request.method == 'POST':
        form = EventsForm(request.POST)

        event = Event()

        class_name_ru = request.POST.get("class")
        dog_class = DogClass.objects.filter(name_ru=class_name_ru).first()
        event.class_id = dog_class.id

        event.org_id = 0
        event.name = request.POST.get("name")
        event.type = request.POST.get("type")
        event.date = request.POST.get("date")
        event.save()


    form  = EventsForm()
    
    classes = DogClass.objects.all()
    classes_names = []
    for el in classes:
        classes_names.append(el.name_ru)

    events = Event.objects.order_by('id')

    data = {
        'form': form,
        'events': events,
        'classes_names': classes_names
    }

    return render(request, 'event/main.html', data)
