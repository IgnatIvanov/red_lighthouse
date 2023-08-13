from django.urls import path
from out_doc import views as out_doc_views



urlpatterns = [
    path('main', out_doc_views.main, name='out_doc_main'),
    path('', out_doc_views.select_project, name='out_doc_select_project'),
    path('edit_project/<str:project_name>', out_doc_views.edit_project, name='out_doc_edit_project'),
    path('rename_project/<str:old_name>', out_doc_views.rename_project, name='out_doc_rename_project'),
    path('delete_project/<str:project_name>', out_doc_views.delete_project, name='out_doc_delete_project'),
    path('delete_participant/<int:participant_id>', out_doc_views.delete_participant, name='out_doc_delete_participant'),
]