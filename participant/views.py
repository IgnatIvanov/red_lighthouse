from django.shortcuts import render
from dogs.models import Dog
from event.models import Event
from event.models import Type
from event.models import Rank
from classes.models import DogClass
from .models import Participant



def part_main(request):

    error = ''

    # Формирование списка имён событий
    events = Event.objects.all()
    events_names = []
    for el in events:
        event = {}
        event['id'] = el.id
        event['name'] = str(el.date)
        event['name'] += ' ' + str(Type.objects.filter(id=el.type_id).first().name)
        event['name'] += ' ' + str(Rank.objects.filter(id=el.rank_id).first().name)
        event['name'] += ' ' + str(el.comment)
        events_names.append(event)


    # Формирование списка классов
    classes = DogClass.objects.all()
    classes_names = []
    for el in classes:
        dog_class = {}
        dog_class['id'] = el.id
        dog_class['name'] = el.name_ru + ' / ' + el.name_en
        classes_names.append(dog_class)


    # Обработка входящего POST запроса
    if request.method == 'POST':

        # Создание новой записи об участии
        participant = Participant()

        # Заполнение dog_id участника
        dog_tattoo = request.POST.get("dog")
        dog = Dog.objects.filter(tattoo=dog_tattoo).first()
        participant.dog_id = dog.id

        # Заполнение выбранного события на участие
        chosed_event = request.POST.get("event")        
        for el in events_names:
            if chosed_event == el['name']:
                # event_id = el['id']
                participant.event_id = el['id']
                break

        # Заполнение класса участника
        chosed_class = request.POST.get("class")
        for el in classes_names:
            if chosed_class == el['name']:
                participant.class_id = el['id']

        # Заполнение статуса оплаты
        pay = request.POST.get("pay")
        if pay == 'no_pay':
            participant.is_pay = False
        else:
            participant.is_pay = True

        # Сохранение новой записи
        participant.save()


    dogs = Dog.objects.all()
    dog_tattoos = []
    for el in dogs:
        dog_tattoos.append(el.tattoo)

    participants = Participant.objects.all().order_by('-id')

    p = []
    for el in participants:
        part = {}

        part['id'] = el.id

        dog = Dog.objects.filter(id=el.dog_id).first()
        part['dog_tattoo'] = dog.tattoo

        # event = Event.objects.filter(id=el.event_id).first()
        # # part['event'] = event.name + '-;-' + str(event.date)
        # part['event'] = str(event.date) + event.comment
        for el2 in events_names:
            if el2['id'] == el.event_id:
                part['event'] = el2['name']

        for el2 in classes_names:
            if el2['id'] == el.class_id:
                part['class'] = el2['name']

        if el.is_pay == True:
            part['status'] = 'оплачен'
        else:
            part['status'] = 'ожидает оплаты'

        p.append(part)

    data = {
        'error': error,
        'dog_tattoos': dog_tattoos,
        'events_names': events_names,
        'classes_names': classes_names,
        'participants': p
    }

    return render(request, 'participant/main.html', data)