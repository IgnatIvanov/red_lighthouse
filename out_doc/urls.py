from django.urls import path
from out_doc import views as out_doc_views



urlpatterns = [
    path('', out_doc_views.main, name='out_doc_main'),
    # path('<int:dog_id>', dogs_views.dogs_update, name='dogs_update') 
]