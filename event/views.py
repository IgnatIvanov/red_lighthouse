from django.shortcuts import render
from .models import Event
from .models import Type
from .models import Rank
from .forms import EventsForm
from classes.models import DogClass



def events_main(request):

    error = ''
    if request.method == 'POST':
        form = EventsForm(request.POST)

        event = Event()

        # class_name_ru = request.POST.get("class")
        # dog_class = DogClass.objects.filter(name_ru=class_name_ru).first()
        # event.class_id = dog_class.id

        event_type = request.POST.get("type")
        type_name = Type.objects.filter(name=event_type).first()
        event.type_id = type_name.id

        event_rank = request.POST.get("rank")
        rank_name = Rank.objects.filter(name=event_rank).first()
        event.rank_id = rank_name.id


        event.org_id = 0
        event.type = request.POST.get("type")
        event.date = request.POST.get("date")
        event.comment = request.POST.get("comment")
        event.save()


    form  = EventsForm()
    
    # classes = DogClass.objects.all()
    # classes_names = []
    # for el in classes:
    #     classes_names.append(el.name_ru)

    events = Event.objects.order_by('id')

    types = Type.objects.all()
    types_names = []
    for el in types:
        types_names.append(el.name)

    ranks = Rank.objects.all()
    ranks_names = []
    for el in ranks:
        ranks_names.append(el.name)

    data = {
        'form': form,
        'events': events,
        'types_names': types_names,
        'ranks_names': ranks_names
    }

    return render(request, 'event/main.html', data)
