from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import user_passes_test

def registro(request):
  datos = ''
  errors = []

  if request.method == "POST":
    username = request.POST.get("username")
    email = request.POST.get("email")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    datos = request.POST

    if password1 != password2:
      errors.append("Las contraseñas no coinciden.")
    
    if User.objects.filter(username=username).exists():
      errors.append("El nombre de usuario ya existe.")
    
    if User.objects.filter(email=email).exists():
      errors.append("El correo electrónico ya estpa registrado.")
    
    if not errors:
      user = User.objects.create_user(
        username=username,
        email=email,
        password=password1,
        first_name=first_name,
        last_name=last_name
      )
      login(request, user)
      return redirect("home")

  return render(request, "registro.html", {"errors": errors, "datos": datos})

def es_admin(user):
  return user.is_authenticated and user.is_staff

@user_passes_test(es_admin)
def grupos(request):
  if request.method == "POST":
    nombre = request.POST.get('nombre_grupo')
    if nombre and not Group.objects.filter(name=nombre).exists():
      Group.objects.create(name=nombre)
    return redirect('grupos')
  
  grupos = Group.objects.all()
  return render(request, 'grupos.html', {'grupos': grupos})

@user_passes_test(es_admin)
def eliminar_grupo(request, id_grupo):
  if request.method == "POST":
    grupo = get_object_or_404(Group, id=id_grupo)
    if grupo:
      grupo.delete()
  
  return redirect('grupos')

def dar_miembros(grupo):
  return grupo.user_set.all()

def dar_no_miembros(grupo):
  miembros = dar_miembros(grupo)
  return User.objects.exclude(id__in=miembros.values_list('id', flat=True))

@user_passes_test(es_admin)
def editar_grupo(request, id_grupo):
  grupo = get_object_or_404(Group, id=id_grupo)
  if request.method == "POST":
    nuevo_nombre = request.POST.get('name')
    grupo.name = nuevo_nombre
    grupo.save()
    return redirect('grupos')
  
  miembros = dar_miembros(grupo)
  no_miembros = dar_no_miembros(grupo)

  return render(request, 'editar_grupo.html', {
    'grupo': grupo,
    'miembros': miembros,
    'no_miembros': no_miembros,
  })

@user_passes_test(es_admin)
def agregar_usuario_grupo(request, id_grupo):
  grupo = get_object_or_404(Group, id=id_grupo)
  if request.method == "POST":
    id_user = request.POST.get('id_user')
    if id_user:
      user = get_object_or_404(User, id=id_user)
      grupo.user_set.add(user)
    
    return redirect('editar_grupo', id_grupo=grupo.id)
  
  return render(request, 'editar_grupo.html', id_grupo=grupo.id)

@user_passes_test(es_admin)
def eliminar_usuario_grupo(request, id_grupo):
  grupo = get_object_or_404(Group, id=id_grupo)
  if request.method == "POST":
    id_user = request.POST.get('id_user')
    if id_user:
      user = get_object_or_404(User, id=id_user)
      grupo.user_set.remove(user)
    
    return redirect('editar_grupo', id_grupo=grupo.id)
  
  return render(request, 'editar_grupo.html', id_grupo=grupo.id)

@user_passes_test(es_admin)
def permisos(request):
  permisos = Permission.objects.all()
  grupos = Group.objects.all()

  grupo_id = request.POST.get('grupo') if request.POST.get('grupo') else request.GET.get('grupo')

  if grupo_id:
    grupo = get_object_or_404(Group, id=grupo_id)
  else:
    grupo = grupos.first()
  
  if request.method == "POST":
    permisos_ids = request.POST.getlist('permisos')
    grupo.permissions.set(permisos_ids)
    return redirect(f"{reverse('permisos')}?grupo={grupo.id}")
  
  if grupo:
    permisos_grupo = set(grupo.permissions.values_list('id', flat=True))
  else:
    permisos_grupo = set()
  
  return render(request, 'permisos.html', {
    'permisos': permisos,
    'grupos': grupos,
    'grupo': grupo,
    'permisos_grupo': permisos_grupo,
  })