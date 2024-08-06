from django.urls import path
from .views import *

urlpatterns = [
    path('registrar/', RegistrarUsuarioView.as_view(), name='registrar_usuario'),
    path('login/', IniciarSesionView.as_view(), name='login'),

]
