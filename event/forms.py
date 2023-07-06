from .models import Event
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import DateTimeInput



class EventsForm(ModelForm):

    class Meta:

        model = Event
        fields = [
            'name',
            'type',
            'date'
        ]

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название события'
            }),
            'type': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тип события'
            }),
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата проведения'
            }),
        }