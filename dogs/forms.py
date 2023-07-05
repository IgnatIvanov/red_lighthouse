from .models import Dog
from .models import Breed
from django.forms import ModelForm, TextInput
from django.forms import DateTimeInput, Textarea
from django.forms import ModelChoiceField, BooleanField
from django.forms import CheckboxInput


class DogsForm(ModelForm):

    class Meta:

        model = Dog
        fields = [
            'breed_id',
            'rkf',
            'region',
            'birth_date',
            # 'is_male',
            'tattoo',
            'chip',
            'name_ru',
            'name_en',
            'colour_ru',
            'colour_en',
            'breeder_id',
            'owner_id',
            'father_id',
            'mother_id'
        ]

        widgets = {            
            # 'breed_id': ModelChoiceField(queryset=Breed.objects.all()),
            'rkf': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер РФК'
            }),
            'region': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Регион'
            }),
            'birth_date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата рождения'
            }),
            # 'is_male': BooleanField(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Дата рождения'
            # }),
            # 'is_male': BooleanField(),
            # 'is_male': CheckboxInput(),
            'tattoo': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Клеймо'
            }),
            'chip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Чип'
            }),
            'name_ru': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кличка на русском'
            }),
            'name_en': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кличка на английском'
            }),
            'colour_ru': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Окрас на русском'
            }),
            'colour_en': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Окрас на английском'
            }),
            'breeder_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заводчик'
            }),
            'owner_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Владелец'
            }),
            'father_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отец'
            }),
            'mother_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Мать'
            }),
        }