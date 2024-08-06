from django.db import models

class Sistema(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=30, null=False)
    verificarEstado = models.BooleanField(null=False)
    camara = models.OneToOneField('Camara.Camara', on_delete=models.SET_NULL, null=True, related_name='sistema')

    class Meta:
        db_table = 'Sistema'
