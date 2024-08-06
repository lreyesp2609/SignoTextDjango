from django.db import models

class Historial(models.Model):
    id = models.AutoField(primary_key=True)
    traducciones = models.CharField(max_length=30)
    usuario = models.ForeignKey('Usuarios.Usuario', on_delete=models.CASCADE, related_name='historiales', null=True)

    class Meta:
        db_table = 'Historial'
