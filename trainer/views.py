from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId
from django import forms
from .forms import RoutineForm
from django.http import JsonResponse

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

@login_required
def multi_listados(request, tipo):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

    if tipo == 'ejercicios':
        items = list(db['trainer_exercise'].find())
        crear_url = 'trainer:crear_ejercicio'  # Nombre correcto de la URL para crear
    elif tipo == 'rutinas':
        items = list(db['trainer_routine'].find())
        crear_url = 'trainer:crear_rutina'  # Asegúrate de que esta URL existe en urls.py
    else:
        messages.error(request, 'Vista no válida')
        return redirect('trainer:multi_listados', tipo='ejercicios')  

    return render(request, 'trainer/multi_listados.html', {
        'items': items,
        'tipo': tipo,
        'crear_url': crear_url  # Pasamos la URL correcta según el tipo
    })

@login_required
def RoutineCreateView(request):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

    # Obtener todos los ejercicios disponibles en la base de datos
    ejercicios = list(db['trainer_exercise'].find({}, {'id': 1, 'name': 1, 'duration': 1}))

    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            try:
                # Obtener el último ID de rutina y aumentarlo en 1
                last_routine = db['trainer_routine'].find_one(sort=[("id", -1)])
                new_id = last_routine['id'] + 1 if last_routine else 1

                rutina = {
                    'id': new_id,
                    'name': form.cleaned_data['nombre'],
                    'description': form.cleaned_data['descripcion'],
                    'difficulty': form.cleaned_data['dificultad'],
                    'energy_level': form.cleaned_data['energia'],
                    'trainer': form.cleaned_data['entrenador'],
                    'exercises': [int(request.POST.get('ejercicio'))]  # Guardamos el ID del ejercicio seleccionado
                }

                db['trainer_routine'].insert_one(rutina)
                messages.success(request, 'Rutina creada exitosamente')
                return redirect('trainer:multi_listados', tipo='rutinas')
            except Exception as e:
                messages.error(request, f'Error al crear la rutina: {str(e)}')
    else:
        form = RoutineForm()

    return render(request, 'trainer/crear_rutina.html', {
        'form': form,
        'ejercicios': ejercicios  # Pasamos la lista de ejercicios al template
    })

@login_required
def ExerciseCreateView(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            try:
                client = MongoClient(settings.MONGO_URI)
                db = client[settings.MONGO_DB_NAME]
                
                # Obtener el último ID y aumentar en 1
                last_exercise = db['trainer_exercise'].find_one(sort=[("id", -1)])
                new_id = last_exercise['id'] + 1 if last_exercise else 1
                
                ejercicio = {
                    'id': new_id,
                    'name': form.cleaned_data['nombre'],
                    'description': form.cleaned_data['descripcion'],
                    'duration': int(form.cleaned_data['duracion'])
                }
                
                db['trainer_exercise'].insert_one(ejercicio)
                messages.success(request, 'Ejercicio creado exitosamente')
                return redirect('trainer:multi_listados')
            except Exception as e:
                messages.error(request, f'Error al crear el ejercicio: {str(e)}')
    else:
        form = ExerciseForm()
    
    return render(request, 'trainer/crear_ejercicio.html', {'form': form})

@login_required
def ExerciseUpdateView(request, pk):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    
    ejercicio = db['trainer_exercise'].find_one({'id': int(pk)})
    
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            try:
                db['trainer_exercise'].update_one(
                    {'id': int(pk)},
                    {'$set': {
                        'name': form.cleaned_data['nombre'],
                        'description': form.cleaned_data['descripcion'],
                        'duration': int(form.cleaned_data['duracion'])
                    }}
                )
                
                messages.success(request, 'Ejercicio actualizado exitosamente')
                return redirect('trainer:multi_listados')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')
    else:
        form = ExerciseForm(initial={
            'nombre': ejercicio.get('name', ''),
            'descripcion': ejercicio.get('description', ''),
            'duracion': str(ejercicio.get('duration', ''))
        })
    
    return render(request, 'trainer/crear_ejercicio.html', {
        'form': form, 
        'ejercicio': ejercicio, 
        'edit_mode': True
    })

@login_required
def ExerciseDeleteView(request, pk):
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    
    # Busca el ejercicio usando el campo 'id'
    ejercicio = db['trainer_exercise'].find_one({'id': int(pk)})
    
    if request.method == 'POST':
        try:
            # Elimina el ejercicio usando el campo 'id'
            result = db['trainer_exercise'].delete_one({'id': int(pk)})
            
            if result.deleted_count:
                messages.success(request, 'Ejercicio eliminado exitosamente')
            else:
                messages.error(request, 'Ejercicio no encontrado')
            
            return redirect('trainer:multi_listados')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
            return redirect('trainer:multi_listados')
    
    return render(request, 'trainer/eliminar_ejercicio.html', {'ejercicio': ejercicio})
