from django import forms
from .models import TrainerExercise, TrainerRutina
class RutinaForm(forms.ModelForm):
    class Meta:
        model = TrainerRutina
        fields = ['nom', 'descripcio', 'dificultat', 'energia']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el nombre de la rutina'}),
            'descripcio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe la rutina'}),
            'dificultat': forms.Select(attrs={'class': 'form-select'}),
            'energia': forms.Select(attrs={'class': 'form-select'})
        }

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = TrainerExercise
        fields = ['name', 'description', 'duration']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el nombre del ejercicio'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el ejercicio'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración en minutos'})
        }

class RoutineForm(forms.ModelForm):
    class Meta:
        model = TrainerRutina
        fields = ['nom', 'descripcio', 'dificultat', 'energia']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el nombre de la rutina'}),
            'descripcio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe la rutina'}),
            'dificultat': forms.Select(attrs={'class': 'form-select'}),
            'energia': forms.Select(attrs={'class': 'form-select'})
        }
