from django.db import models

from Camara.models import Camara

# Create your models here.
class ConfiguracionCamara(models.Model):
    id = models.AutoField(primary_key=True)
    nombreConfiguracion = models.CharField(max_length=30, null=False)
    configurarCamara = models.CharField(max_length=30, null=False)
    camara = models.ForeignKey(Camara, on_delete=models.CASCADE, related_name='configuraciones', blank=True, null=True)

    class Meta:
        db_table = 'ConfiguracionCamara'