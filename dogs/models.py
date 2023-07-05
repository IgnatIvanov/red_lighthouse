from django.db import models
from breed.models import Breed
# from .models import Breed


def get_empty_breed_id():
    return ''


# Create your models here.
class Dog(models.Model):

    breed_id = models.IntegerField('id породы в таблице')
    rkf = models.TextField('Номер РКФ')
    region = models.TextField('Регион')
    birth_date = models.DateField('Дата рождения')
    is_male = models.BooleanField('Признак пола')
    tattoo = models.TextField('Клеймо')
    chip = models.TextField('Чип')
    name_ru = models.TextField('Кличка на русском')
    name_en = models.TextField('Кличка на английском')
    colour_ru = models.TextField('Окрас на русском')
    colour_en = models.TextField('Окрас на английском')
    breeder_id = models.IntegerField('Заводчик')
    owner_id = models.IntegerField('Владелец')
    father_id = models.IntegerField('Отец')
    mother_id = models.IntegerField('Мать')

    class Meta:
        
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'
