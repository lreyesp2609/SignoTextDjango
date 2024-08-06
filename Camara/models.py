from django.db import models

# Create your models here.
class Camara(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=30, null=False)
    verificarEstado = models.BooleanField(null=False)
    
    class Meta:
        db_table = 'Camara'