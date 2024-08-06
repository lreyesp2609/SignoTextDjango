from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=128)
    rol = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'Usuario'