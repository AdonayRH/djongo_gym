from django import forms
from .models import Rutina, SessioRutina

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nom', 'descripcio', 'tipus', 'durada_minuts', 'capacitat_maxima']

class SessioRutinaForm(forms.ModelForm):
    class Meta:
        model = SessioRutina
        fields = ['rutina', 'data', 'hora_inici', 'hora_fi', 'sala']

from django import forms

class ExerciseForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el nombre del ejercicio'}),
        required=True
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el ejercicio'}),
        required=True
    )
    duracion = forms.ChoiceField(
        choices=[
            ('5', '5 minutos'),
            ('10', '10 minutos'),
            ('15', '15 minutos'),
            ('20', '20 minutos')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

class RoutineForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el nombre de la rutina'}),
        required=True
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe la rutina'}),
        required=True
    )
    dificultad = forms.ChoiceField(
        choices=[
            ('Fácil', 'Fácil'),
            ('Intermedio', 'Intermedio'),
            ('Difícil', 'Difícil')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    entrenador = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del entrenador'}),
        required=True
    )