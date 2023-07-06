from django.db import models



class Participant(models.Model):

    dog_id = models.IntegerField('id собаки')
    event_id = models.IntegerField('id события')
    is_pay = models.BooleanField('Признак оплаты')