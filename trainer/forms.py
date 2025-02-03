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
