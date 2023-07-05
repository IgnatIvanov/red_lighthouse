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
            'pedigree_code',
            'pedigree_num',
            'region',
            'birth_date',
            'is_male',
            'tattoo_code',
            'tattoo_num',
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
            'pedigree_code': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'код РФК'
            }),
            'pedigree_num': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'цифры РФК'
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
            'is_male': CheckboxInput(),
            'tattoo_code': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Код клейма'
            }),
            'tattoo_num': TextInput(attrs={
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