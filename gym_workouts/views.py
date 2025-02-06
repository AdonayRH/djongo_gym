from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubscriptionPlan, UserSubscription, WorkoutSession, UserWorkout
from datetime import date, timedelta

@login_required
def subscriptions_view(request):
    """ Muestra los planes de suscripción y permite elegir uno. """
    plans = SubscriptionPlan.objects.all()

    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)

        # Crear o actualizar suscripción
        subscription, created = UserSubscription.objects.update_or_create(
            user=request.user,
            defaults={
                "plan": plan,
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=30),
            }
        )
        messages.success(request, f"Te has suscrito al plan {plan.name}")
        return redirect("gym_workouts:schedule")

    return render(request, "gym_workouts/subscriptions.html", {"plans": plans})

@login_required
def schedule_view(request):
    """ Muestra las sesiones disponibles y permite apuntarse. """
    user_subscription = UserSubscription.objects.filter(user=request.user).first()
    if not user_subscription or not user_subscription.is_active():
        messages.error(request, "Necesitas una suscripción activa para reservar sesiones.")
        return redirect("gym_workouts:subscriptions")

    sessions = WorkoutSession.objects.filter(date__gte=date.today())  # Solo futuras
    return render(request, "gym_workouts/schedule.html", {"sessions": sessions, "subscription": user_subscription})

@login_required
def join_workout(request, session_id):
    """ Permite a un usuario unirse a una sesión. """
    session = get_object_or_404(WorkoutSession, id=session_id)
    user_subscription = UserSubscription.objects.filter(user=request.user).first()

    # Verifica si hay cupo
    if session.available_spots() <= 0:
        messages.error(request, "No hay más cupos disponibles para esta sesión.")
        return redirect("gym_workouts:schedule")

    # Verifica si tiene entrenamientos disponibles
    if user_subscription.remaining_workouts() <= 0:
        messages.error(request, "Has excedido tu límite de entrenamientos semanales.")
        return redirect("gym_workouts:schedule")

    # Registrar la sesión
    UserWorkout.objects.create(user=request.user, session=session, date=session.date)
    messages.success(request, "Te has unido a la sesión correctamente.")
    return redirect("gym_workouts:schedule")

@login_required
def leave_workout(request, session_id):
    """ Permite cancelar la reserva de una sesión con una semana de antelación. """
    session = get_object_or_404(WorkoutSession, id=session_id)
    user_workout = UserWorkout.objects.filter(user=request.user, session=session).first()

    if not user_workout:
        messages.error(request, "No estás registrado en esta sesión.")
        return redirect("gym_workouts:schedule")

    if session.date - timedelta(days=7) < date.today():
        messages.error(request, "Solo puedes cancelar con al menos 7 días de antelación.")
        return redirect("gym_workouts:schedule")

    user_workout.delete()
    messages.success(request, "Has cancelado tu inscripción correctamente.")
    return redirect("gym_workouts:schedule")
