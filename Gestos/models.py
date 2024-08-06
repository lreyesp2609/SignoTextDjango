from django.db import models

class Gestos(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=30, null=False)
    sistema = models.ForeignKey('Sistema.Sistema', on_delete=models.CASCADE, related_name='gestos', null=True)
    diccionarioGestos = models.ForeignKey('DiccionarioGestos.DiccionarioGestos', on_delete=models.CASCADE, related_name='gestos_diccionario', null=True)

    class Meta:
        db_table = 'Gestos'

    def __str__(self):
        return self.descripcion
