from django.contrib.auth.models import AbstractUser
from djongo import models
from bson.objectid import ObjectId
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from django.conf import settings  # Asegúrate de importar settings

class Rutina(models.Model):
    nom = models.CharField(max_length=100)
    descripcio = models.TextField()
    tipus = models.CharField(
        max_length=10,
        choices=[
            ('DIRIGIDA', 'Activitat Dirigida'),
            ('MUSCULACIO', 'Musculació')
        ],
        default='DIRIGIDA'
    )
    durada_minuts = models.IntegerField()
    capacitat_maxima = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    entrenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'trainer'}
    )

    class Meta:
        db_table = 'rutines'


class SessioRutina(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    data = models.DateField()
    hora_inici = models.TimeField()
    hora_fi = models.TimeField()
    sala = models.CharField(max_length=100)
    participants = models.ManyToManyField(
    settings.AUTH_USER_MODEL,  # En vez de CustomUser
    related_name='sessions_inscrites',
    limit_choices_to={'role': 'user'},  # Usa el rol como string
    blank=True
)
    class Meta:
        db_table = 'sessions_rutina'
        unique_together = ['sala', 'data', 'hora_inici']

