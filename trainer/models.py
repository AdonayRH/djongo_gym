from django.contrib.auth.models import AbstractUser
from djongo import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from bson import ObjectId

# class SessioRutina(models.Model):
#     rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
#     data = models.DateField()
#     hora_inici = models.TimeField()
#     hora_fi = models.TimeField()
#     sala = models.CharField(max_length=100)
#     participants = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='sessions_inscrites',
#         limit_choices_to={'role': 'user'},
#         blank=True
#     )

#     class Meta:
#         db_table = 'sessions_rutina'
#         unique_together = ['sala', 'data', 'hora_inici']

class TrainerExercise(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'trainer_exercise'
    
class TrainerRutina(models.Model):
    nom = models.CharField(max_length=100)
    descripcio = models.TextField()
    exercises = models.ManyToManyField(TrainerExercise, related_name='rutinas')
    dificultat = models.CharField(
        max_length=10,
        choices=[
            ('Fácil', 'Fácil'),
            ('Intermedio', 'Intermedio'),
            ('Difícil', 'Difícil')
        ],
        default='Fácil'
    )
    energia = models.IntegerField(
        choices=[
            (3, 'Bajo'),
            (7, 'Medio'),
            (10, 'Alto')
        ],
        default=7
    )

    class Meta:
        db_table = 'rutines'

class HorarioRutina(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    rutina = models.ForeignKey("TrainerRutina", on_delete=models.CASCADE)
    dia = models.CharField(
        max_length=10,
        choices=[
            ('Lunes', 'Lunes'),
            ('Martes', 'Martes'),
            ('Miércoles', 'Miércoles'),
            ('Jueves', 'Jueves'),
            ('Viernes', 'Viernes')
        ]
    )
    hora = models.IntegerField(choices=[(16, "16:00"), (17, "17:00"), (18, "18:00"), (19, "19:00"), (20, "20:00"), (21, "21:00")])

    class Meta:
        unique_together = ['dia', 'hora']