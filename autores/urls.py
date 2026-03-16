from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_autores, name='lista_autores'),
    path('crear/', views.crear_autor, name='crear_autor'),
    path('editar/<int:id>/', views.editar_autor, name='editar_autor'),
    path('eliminar/<int:id>/', views.eliminar_autor, name='eliminar_autor'),
]