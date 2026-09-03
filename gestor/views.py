from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Proyecto

def hello(request):
  return HttpResponse("¡Hola mundo!")

def acerca_de(request):
  return HttpResponse("<h1>Acerca de</h1>")

def proyectos(request):
  proyectos = Proyecto.objects.all()
  return render(request, 'proyectos.html', {'proyectos': proyectos})

def proyecto_detalle(request, proyecto_id):
  proyecto = Proyecto.objects.get(id=proyecto_id)
  return render(request, 'detalle_proyecto.html', {'proyecto': proyecto})

def nuevo_proyecto(request):
  if request.method == "POST":
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    duracion = request.POST.get('duracion')

    if nombre and descripcion and duracion:
      proyecto = Proyecto(
        nombre=nombre,
        descripcion=descripcion,
        duracion=duracion
      )
      proyecto.save()
    
    return redirect('proyectos')

  return render(request, 'crear-proyecto.html')

def eliminar_proyecto(request, id):
  proyecto = Proyecto.objects.get(id=id)
  proyecto.delete()
  return redirect('proyectos')