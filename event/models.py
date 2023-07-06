from django.db import models


class Event(models.Model):

    org_id = models.IntegerField('id Организатора')
    name = models.TextField('Название события')
    type = models.TextField('Тип')
    date = models.DateField('Дата проведения')
    class_id = models.IntegerField('id Класса')

    class Meta:
        
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    # def __str__(self):
    #     return "{}. {} - {}".format(self.id, self.name_ru, self.name_en)
