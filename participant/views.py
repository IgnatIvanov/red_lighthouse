from django.shortcuts import render
from dogs.models import Dog
from event.models import Event
from .models import Participant



def part_main(request):

    error = ''

    if request.method == 'POST':

        participant = Participant()

        dog_tattoo = request.POST.get("dog")
        dog = Dog.objects.filter(tattoo=dog_tattoo).first()
        participant.dog_id = dog.id

        chosed_event = request.POST.get("event")
        event_name = chosed_event.split('-;-')[0]
        event_date = chosed_event.split('-;-')[1]
        event = Event.objects.filter(name=event_name, date=event_date).first()
        participant.event_id = event.id
        # print('event_id', event.id)

        pay = request.POST.get("pay")
        if pay == 'no_pay':
            participant.is_pay = False
        else:
            participant.is_pay = True

        participant.save()

    dogs = Dog.objects.all()
    dog_tattoos = []
    for el in dogs:
        dog_tattoos.append(el.tattoo)

    events = Event.objects.all()
    events_names = []
    for el in events:
        event = el.name + '-;-' + str(el.date)
        events_names.append(event)

    participants = Participant.objects.all().order_by('-id')

    p = []
    for el in participants:
        part = {}
        part['id'] = el.id

        dog = Dog.objects.filter(id=el.dog_id).first()
        part['dog_tattoo'] = dog.tattoo

        event = Event.objects.filter(id=el.event_id).first()
        part['event'] = event.name + '-;-' + str(event.date)

        if el.is_pay == True:
            part['status'] = 'оплачен'
        else:
            part['status'] = 'ожидает оплаты'

        p.append(part)

    data = {
        'error': error,
        'dog_tattoos': dog_tattoos,
        'events_names': events_names,
        'participants': p
    }

    return render(request, 'participant/main.html', data)