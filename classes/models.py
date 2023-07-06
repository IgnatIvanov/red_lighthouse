from django.db import models



class DogClass(models.Model):

    name_ru = models.TextField('Название русское')
    name_en = models.TextField('Название английское')

    class Meta:
        
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    def __str__(self):
        return "{}. {} - {}".format(self.id, self.name_ru, self.name_en)
