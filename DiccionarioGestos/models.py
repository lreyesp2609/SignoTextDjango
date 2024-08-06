from django.db import models

class DiccionarioGestos(models.Model):
    id = models.AutoField(primary_key=True)
    actualizarDiccionario = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'DiccionarioGestos'

    def __str__(self):
        return self.actualizarDiccionario
