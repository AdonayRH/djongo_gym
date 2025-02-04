from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include


app_name = 'trainer'

urlpatterns = [
    path('listar/<str:tipo>/', views.multi_listados, name='multi_listados'),
    path('crear/rutina/', views.RoutineCreateView, name='crear_rutina'),
    path('ejercicios/crear/', views.ExerciseCreateView, name='crear_ejercicio'),
    path('ejercicios/editar/<str:pk>/', views.ExerciseUpdateView, name='editar_ejercicio'),
    path('ejercicios/eliminar_ejercicio/<int:pk>/', views.ExerciseDeleteView, name='eliminar_ejercicio'), 
]

