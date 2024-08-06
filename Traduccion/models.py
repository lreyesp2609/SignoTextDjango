from django.db import models

class Traduccion(models.Model):
    id = models.AutoField(primary_key=True)
    textoTraducido = models.CharField(max_length=100, null=False)
    fechaHora = models.DateTimeField(auto_now_add=True)
    mostrar = models.CharField(max_length=30, null=False)
    usuario = models.ForeignKey('Usuarios.Usuario', on_delete=models.CASCADE, related_name='traducciones', null=True)
    historial = models.ForeignKey('Historial.Historial', on_delete=models.CASCADE, related_name='traducciones_historial', null=True)
    sistema = models.ForeignKey('Sistema.Sistema', on_delete=models.CASCADE, related_name='traducciones', null=True)

    class Meta:
        db_table = 'Traduccion'
