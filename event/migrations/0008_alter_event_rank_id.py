# Generated by Django 4.2.3 on 2023-07-21 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_remove_event_type_event_rank_id_event_type_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='rank_id',
            field=models.IntegerField(verbose_name='id ранга'),
        ),
    ]