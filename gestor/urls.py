from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.hello, name='home'),
  path('acerca-de/', views.acerca_de),
  path('proyectos/', views.proyectos, name='proyectos'),
  path('proyectos/<int:proyecto_id>/', views.proyecto_detalle, name='proyecto_detalle'),
  path('proyectos/nuevo/', views.nuevo_proyecto, name="nuevo_proyecto"),
  path('proyectos/<int:id>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),
  path('proyectos/<int:id>/editar/', views.editar_proyecto, name='editar_proyecto'),
  
  path('proyectos/<int:proyecto_id>/tareas/nueva/', views.crear_tarea, name='crear_tarea'),
  path('tareas/<int:id>/avanzar/', views.avanzar_estado_tarea, name='avanzar_estado_tarea'),
]