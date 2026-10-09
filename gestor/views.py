from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from .models import Proyecto, Tarea

@login_required
def hello(request):
  return render(request, 'home.html')

def acerca_de(request):
  return HttpResponse("<h1>Acerca de</h1>")

@permission_required('gestor.view_proyecto', raise_exception=True)
def proyectos(request):
  proyectos = Proyecto.objects.all()
  return render(request, 'proyectos.html', {'proyectos': proyectos})

@permission_required('gestor.view_proyecto', raise_exception=True)
def proyecto_detalle(request, proyecto_id):
  proyecto = Proyecto.objects.get(id=proyecto_id)
  return render(request, 'detalle_proyecto.html', {'proyecto': proyecto})

@permission_required('gestor.add_proyecto', raise_exception=True)
def nuevo_proyecto(request):
  if request.method == "POST":
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    duracion = request.POST.get('duracion')
    imagen = request.FILES.get('imagen')

    if nombre and descripcion and duracion:
      proyecto = Proyecto(
        nombre=nombre,
        descripcion=descripcion,
        duracion=duracion,
        imagen=imagen
      )
      proyecto.save()
    
    return redirect('proyectos')

  return render(request, 'crear-proyecto.html')

@permission_required('gestor.delete_proyecto', raise_exception=True)
def eliminar_proyecto(request, id):
  proyecto = Proyecto.objects.get(id=id)
  proyecto.delete()
  return redirect('proyectos')

@permission_required('gestor.change_proyecto', raise_exception=True)
def editar_proyecto(request, id):
  proyecto = Proyecto.objects.get(id=id)

  if request.method == "POST":
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    duracion = request.POST.get('duracion')

    proyecto.nombre = nombre
    proyecto.descripcion = descripcion
    proyecto.duracion = duracion
    proyecto.save()

    return redirect('proyectos')

  return render(request, 'editar-proyecto.html', {'proyecto': proyecto})

@permission_required('gestor.add_tarea', raise_exception=True)
def crear_tarea(request, proyecto_id):
  proyecto = Proyecto.objects.get(id=proyecto_id)

  if request.method == "POST":
    titulo = request.POST.get('titulo')
    prioridad = request.POST.get('prioridad')
    estado = request.POST.get('estado')

    if titulo:
      Tarea.objects.create(
        proyecto=proyecto,
        titulo=titulo,
        prioridad=prioridad,
        estado=estado
      )
      return redirect('proyecto_detalle', proyecto_id=proyecto.id)

  return render(request, 'crear-tarea.html', {'proyecto': proyecto, 'prioridad_choices': Tarea.PRIORIDAD_CHOICES, 'estado_choices': Tarea.ESTADO_CHOICES})

@require_POST
@permission_required('gestor.change_tarea', raise_exception=True)
def avanzar_estado_tarea(request, id):
  tarea = Tarea.objects.get(id=id)

  if tarea.estado == "PENDIENTE":
    tarea.estado = "EN_PROGRESO"
    tarea.save()
  elif tarea.estado == "EN_PROGRESO":
    tarea.estado = "COMPLETADO"
    tarea.save()

  return redirect('proyecto_detalle', proyecto_id=tarea.proyecto.id)

