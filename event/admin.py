from django.contrib import admin
from .models import Event, Type, Rank


admin.site.register(Event)
admin.site.register(Type)
admin.site.register(Rank)