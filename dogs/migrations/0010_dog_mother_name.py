# Generated by Django 4.2.3 on 2023-10-26 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0009_dog_father_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='mother_name',
            field=models.TextField(default='Кличка мамы не указана', verbose_name='Кличка мамы'),
            preserve_default=False,
        ),
    ]