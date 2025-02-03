from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include


app_name = 'trainer'

urlpatterns = [
    path('rutines/', views.RutinaListView.as_view(), name='rutina-list'),
    path('rutines/crear/', views.RutinaCreateView.as_view(), name='rutina-create'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

