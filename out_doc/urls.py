from django.urls import path
from out_doc import views as out_doc_views



urlpatterns = [
    path('main', out_doc_views.main, name='out_doc_main'),
    path('', out_doc_views.select_project, name='out_doc_select_project'),
    path('edit_project/<int:project_id>', out_doc_views.edit_project, name='out_doc_edit_project'),
    path('create_project_doc/<int:project_id>', out_doc_views.create_project_doc, name='create_project_doc'),
    path('rename_project/<int:project_id>', out_doc_views.rename_project, name='out_doc_rename_project'),
    path('delete_project/<int:project_id>', out_doc_views.delete_project, name='out_doc_delete_project'),
    path('delete_participant/<int:participant_id>', out_doc_views.delete_participant, name='out_doc_delete_participant'),
    path('project_add_dog', out_doc_views.project_add_dog, name='project_add_dog'),
    path('get_dog_by_tattoo', out_doc_views.get_dog_by_tattoo, name='get_dog_by_tattoo'),
    path('get_judges', out_doc_views.get_judges, name='get_judges'),
    path('save_judges', out_doc_views.save_judges, name='save_judges'),
]