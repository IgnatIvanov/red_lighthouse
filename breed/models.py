from django.db import models

class Breed(models.Model):
    
    group = models.IntegerField('Группа')
    bid = models.IntegerField('Код породы')
    name_ru = models.TextField('Название русское')
    name_en = models.TextField('Название английское')    
    country_ru = models.TextField('Страна на русском')
    country_en = models.TextField('Страна на английском')
    size = models.TextField('Размер особи')

    # def __str__(self):
    #     return '{}. {}'.format(self.bid, self.name_ru)
    
    # def get_fields(self):
    #     return [[(field, field.value_to_string(self)) for field in Order._meta.fields]]

    class Meta:
        
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'