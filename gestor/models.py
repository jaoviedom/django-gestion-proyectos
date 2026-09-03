from django.db import models

class Proyecto(models.Model):
  '''
  Modelo que representa un Proyecto
  '''
  nombre = models.CharField(max_length=100)
  descripcion = models.TextField()
  duracion = models.IntegerField()
