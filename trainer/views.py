from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from trainer.forms import RoutineForm, ExerciseForm
from .models import TrainerRutina, TrainerExercise, HorarioRutina
from bson import ObjectId
import hashlib

@login_required
def multi_listados(request, tipo):
    if tipo == 'ejercicios':
        items = TrainerExercise.objects.all()
        crear_url = 'trainer:crear_ejercicio'
    elif tipo == 'rutinas':
        items = TrainerRutina.objects.all()
        crear_url = 'trainer:crear_rutina'
    else:
        messages.error(request, 'Vista no válida')
        return redirect('trainer:multi_listados', tipo='ejercicios')

    return render(request, 'trainer/multi_listados.html', {
        'items': items,
        'tipo': tipo,
        'crear_url': crear_url
    })

@login_required
def RoutineCreateView(request):
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Rutina creada exitosamente')
                return redirect('trainer:multi_listados', tipo='rutinas')
            except Exception as e:
                messages.error(request, f'Error al crear la rutina: {str(e)}')
    else:
        form = RoutineForm()

    return render(request, 'trainer/crear_rutina.html', {
        'form': form
    })

@login_required
def RoutineCreateUpdateView(request, pk=None):
    ejercicios = TrainerExercise.objects.all()

    if pk:
        rutina = get_object_or_404(TrainerRutina, pk=pk)
    else:
        rutina = None

    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=rutina)
        if form.is_valid():
            rutina = form.save()
            rutina.exercises.set(request.POST.getlist('ejercicios'))  # Asociar ejercicios seleccionados
            rutina.save()

            if pk:
                messages.success(request, 'Rutina actualizada exitosamente')
            else:
                messages.success(request, 'Rutina creada exitosamente')
            return redirect('trainer:multi_listados', tipo='rutinas')
    else:
        form = RoutineForm(instance=rutina)

    return render(request, 'trainer/crear_rutina.html', {
        'form': form,
        'ejercicios': ejercicios,
        'edit_mode': bool(pk)
    })

import traceback  # Importar para capturar el detalle del error

@login_required
def ExerciseCreateView(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Ejercicio creado exitosamente')
                return redirect('trainer:multi_listados', tipo='ejercicios')
            except Exception as e:
                print(f'Error al crear el ejercicio: {e}')
                traceback.print_exc()  # Esto imprimirá el detalle completo del error en la consola
                messages.error(request, f'Error al crear el ejercicio: {str(e)}')
        else:
            print(f'Errores de validación del formulario: {form.errors}')
            messages.error(request, 'El formulario no es válido')
    else:
        form = ExerciseForm()

    return render(request, 'trainer/crear_ejercicio.html', {'form': form})



@login_required
def ExerciseUpdateView(request, pk):
    ejercicio = get_object_or_404(TrainerExercise, id=ObjectId(pk))
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=ejercicio)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Ejercicio actualizado exitosamente')
                return redirect('trainer:multi_listados', tipo='ejercicios')
            except Exception as e:
                messages.error(request, f'Error al actualizar el ejercicio: {str(e)}')
    else:
        form = ExerciseForm(instance=ejercicio)

    return render(request, 'trainer/crear_ejercicio.html', {'form': form, 'edit_mode': True})

@login_required
def RoutineCreateUpdateView(request, pk=None):
    ejercicios = TrainerExercise.objects.all()

    if pk:
        try:
            rutina = get_object_or_404(TrainerRutina, id=int(pk))
            edit_mode = True
        except Exception:
            messages.error(request, "Rutina no encontrada.")
            return redirect('trainer:multi_listados', tipo='rutinas')
    else:
        rutina = None
        edit_mode = False

    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=rutina)
        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.save()

            # Asociar los ejercicios seleccionados
            ejercicios_ids = request.POST.getlist('exercises')
            rutina.exercises.set(ejercicios_ids)
            rutina.save()

            if edit_mode:
                messages.success(request, 'Rutina actualizada exitosamente')
            else:
                messages.success(request, 'Rutina creada exitosamente')

            return redirect('trainer:multi_listados', tipo='rutinas')
        else:
            print(f'Errores en el formulario: {form.errors}')
            messages.error(request, 'El formulario no es válido')
    else:
        form = RoutineForm(instance=rutina)

    return render(request, 'trainer/crear_rutina.html', {
        'form': form,
        'ejercicios': ejercicios,
        'edit_mode': edit_mode,
        'rutina': rutina
    })

@login_required
def DeleteItemView(request, tipo, pk):
    if tipo == 'ejercicio':
        item = get_object_or_404(TrainerExercise, id=ObjectId(pk))
    elif tipo == 'rutina':
        item = get_object_or_404(TrainerRutina, id=ObjectId(pk))
    else:
        messages.error(request, 'Tipo de elemento no válido')
        return redirect('trainer:multi_listados', tipo='ejercicios')

    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, f'{tipo.capitalize()} eliminado exitosamente')
            return redirect('trainer:multi_listados', tipo=tipo + 's')
        except Exception as e:
            messages.error(request, f'Error al eliminar el {tipo}: {str(e)}')

    return render(request, 'trainer/eliminar_item.html', {
        'item': item,
        'tipo': tipo
    })

@login_required
def HorarioView(request):
    rutinas = TrainerRutina.objects.all()
    horario = HorarioRutina.objects.all()

    # Lista de días de la semana
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

    # Crear un diccionario de colores basado en el ID de la rutina
    rutina_colores = {
        str(rutina.id): f"#{hashlib.md5(str(rutina.id).encode()).hexdigest()[:6]}"
        for rutina in rutinas
    }

    # Crear una lista de horarios con estructura más simple
    horario_lista = []
    for dia in dias_semana:
        for hora in range(16, 22):
            entry = horario.filter(dia=dia, hora=hora).first()
            horario_lista.append({
                "dia": dia,
                "hora": hora,
                "entry": entry,
                "rutina_color": rutina_colores.get(str(entry.rutina.id), "#cccccc") if entry else "#cccccc"
            })

    if request.method == "POST":
        dia = request.POST.get("dia")
        hora = int(request.POST.get("hora"))
        rutina_id = request.POST.get("rutina_id")

        if not rutina_id:
            HorarioRutina.objects.filter(dia=dia, hora=hora).delete()
            messages.success(request, "Rutina eliminada.")
        else:
            rutina = get_object_or_404(TrainerRutina, id=int(rutina_id))
            HorarioRutina.objects.update_or_create(dia=dia, hora=hora, defaults={"rutina": rutina})
            messages.success(request, "Rutina programada correctamente.")

        return redirect("trainer:horario")

    return render(request, "trainer/horario.html", {
        "horario_lista": horario_lista,
        "rutinas": rutinas,
        "dias_semana": dias_semana  # PASAMOS la lista de días al template
    })

@login_required
def DashboardView(request):
    if request.method != 'GET':  # Asegura que solo acepte GET
        return render(request, '403.html', status=403)

    rutinas = TrainerRutina.objects.all()
    horario = HorarioRutina.objects.all()

    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

    rutina_colores = {
        str(rutina.id): f"#{hashlib.md5(str(rutina.id).encode()).hexdigest()[:6]}"
        for rutina in rutinas
    }

    horario_lista = []
    for dia in dias_semana:
        for hora in range(16, 22):
            entry = horario.filter(dia=dia, hora=hora).first()
            horario_lista.append({
                "dia": dia,
                "hora": hora,
                "entry": entry,
                "rutina_color": rutina_colores.get(str(entry.rutina.id), "#cccccc") if entry else "#f8f9fa"
            })

    return render(request, "trainer/dashboard.html", {
        "horario_lista": horario_lista,
        "dias_semana": dias_semana
    })