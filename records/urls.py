from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-tables/', views.create_tables, name='create_tables'),
    path('drop-tables/', views.drop_tables, name='drop_tables'),
    path('query-tables/', views.query_tables, name='query_tables'),
    path('manage/', views.manage_records, name='manage_records'),
    path('add-person/', views.add_person, name='add_person'),
    path('delete-person/<int:person_id>/', views.delete_person, name='delete_person'),
]