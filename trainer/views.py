from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Rutina, SessioRutina
from .forms import RutinaForm, SessioRutinaForm
from gym_app.models import User
from gym_app.views import user_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


class EntrenadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.role == User.Roles.ENTRENADOR

class RutinaListView(EntrenadorRequiredMixin, ListView):
    model = Rutina
    template_name = 'trainer/rutina_list.html'
    context_object_name = 'rutines'

    def get_queryset(self):
        return Rutina.objects.filter(entrenador=self.request.user)

class RutinaCreateView(EntrenadorRequiredMixin, CreateView):
    model = Rutina
    form_class = RutinaForm
    template_name = 'trainer/rutina_form.html'
    success_url = reverse_lazy('trainer:rutina-list')

    def form_valid(self, form):
        form.instance.entrenador = self.request.user
        return super().form_valid(form)

@login_required
def dashboard(request):
    return render(request, 'trainer/dashboard.html')

