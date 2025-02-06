from django.urls import path
from . import views

app_name = "gym_workouts"

urlpatterns = [
    path('subscriptions/', views.subscriptions_view, name='subscriptions'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('join/<int:session_id>/', views.join_workout, name='join_workout'),
    path('leave/<int:session_id>/', views.leave_workout, name='leave_workout'),
]
