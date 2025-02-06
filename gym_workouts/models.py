from djongo import models
from django.conf import settings
from datetime import timedelta, date

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    max_workouts_per_week = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.price}€/mes"

    class Meta:
        db_table = "subscription_plans"

class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def is_active(self):
        """Verifica si la suscripción sigue activa."""
        return date.today() <= self.end_date

    def remaining_workouts(self):
        """Calcula los entrenamientos restantes según la suscripción actual."""
        if self.plan.max_workouts_per_week == -1:  # Rutinas ilimitadas
            return float('inf')  
        start_of_week = date.today() - timedelta(days=date.today().weekday())  # Lunes de la semana actual
        workouts_this_week = UserWorkout.objects.filter(user=self.user, date__gte=start_of_week).count()
        return self.plan.max_workouts_per_week - workouts_this_week

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    class Meta:
        db_table = "user_subscriptions"

class WorkoutSession(models.Model):
    rutina = models.ForeignKey("trainer.TrainerRutina", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    max_participants = models.IntegerField(default=10)

    def available_spots(self):
        """Calcula cuántos lugares quedan en la rutina."""
        return self.max_participants - self.userworkout_set.count()

    def __str__(self):
        return f"{self.rutina.nom} - {self.date} {self.time}"

    class Meta:
        db_table = "workout_sessions"
        unique_together = ["rutina", "date", "time"]

class UserWorkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.session.rutina.nom} ({self.date})"

    class Meta:
        db_table = "user_workouts"
        unique_together = ["user", "session"]
