from .models import Event
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import DateTimeInput



class EventsForm(ModelForm):

    class Meta:

        model = Event
        fields = [
            'date',
            'comment'
        ]

        widgets = {
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата проведения'
            }),
            'comment': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дополнительная информация'
            })
        }