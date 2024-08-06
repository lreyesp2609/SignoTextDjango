from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
from django.contrib.auth.hashers import make_password
from django.db import transaction, IntegrityError
import jwt
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
from django.conf import settings
from django.contrib.auth.hashers import check_password

@method_decorator(csrf_exempt, name='dispatch')
class RegistrarUsuarioView(View):
    def post(self, request, *args, **kwargs):
        try:
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            email = request.POST.get('email')
            contrasena = request.POST.get('contrasena')
            rol = request.POST.get('rol')

            if not nombres or not apellidos or not email or not contrasena or not rol:
                return JsonResponse({'error': 'Faltan datos necesarios'}, status=400)

            nombres_lista = nombres.split()
            apellidos_lista = apellidos.split()

            if len(nombres_lista) < 1 or len(apellidos_lista) < 1:
                return JsonResponse({'error': 'Nombres y apellidos deben contener al menos un nombre y un apellido'}, status=400)

            primer_nombre = nombres_lista[0].lower()
            primer_apellido = apellidos_lista[0].lower()
            segundo_nombre = nombres_lista[1] if len(nombres_lista) > 1 else ''

            if Usuario.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Correo electrónico ya registrado'}, status=400)

            with transaction.atomic():
                usuario = self.generar_nombre_usuario(primer_nombre, primer_apellido, segundo_nombre)

                if Usuario.objects.filter(usuario=usuario).exists():
                    return JsonResponse({'error': 'Nombre de usuario ya existe'}, status=400)

                nuevo_usuario = Usuario(
                    usuario=usuario,
                    nombres=nombres,
                    apellidos=apellidos,
                    email=email,
                    contrasena=make_password(contrasena),  # Encriptar la contraseña
                    rol=rol
                )
                nuevo_usuario.save()

            return JsonResponse({'message': 'Registro exitoso'}, status=201)

        except IntegrityError as e:
            return JsonResponse({'error': 'Error en la base de datos: {}'.format(str(e))}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def generar_nombre_usuario(self, primer_nombre, primer_apellido, segundo_nombre):
        base_usuario = f"{primer_nombre}.{primer_apellido}"
        usuario = base_usuario

        contador = 1
        while Usuario.objects.filter(usuario=usuario).exists():
            usuario = f"{base_usuario}{segundo_nombre[0].lower()}{contador}"
            contador += 1

        return usuario
   
@method_decorator(csrf_exempt, name='dispatch')
class IniciarSesionView(View):
    def generate_token(self, usuario):
        payload = {
            'id_usuario': usuario.id,
            'nombre_usuario': usuario.usuario,
            'rol': usuario.rol
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    def post(self, request, *args, **kwargs):
        try:
            nombre_usuario = request.POST.get('usuario')
            contrasenia = request.POST.get('contrasena')

            if not nombre_usuario or not contrasenia:
                return JsonResponse({'error': 'Faltan datos necesarios'}, status=400)

            user = Usuario.objects.filter(usuario=nombre_usuario).first()

            if user is not None:
                if check_password(contrasenia, user.contrasena):  # Verifica la contraseña
                    token = self.generate_token(user)
                    
                    # Verifica si el usuario necesita cambiar su contraseña (opcional, según tu lógica)
                    needs_password_change = False
                    # Puedes definir tu lógica para determinar si necesita cambiar la contraseña

                    return JsonResponse({
                        'token': token,
                        'nombre_usuario': nombre_usuario,
                    })
                else:
                    return JsonResponse({'mensaje': 'Contraseña incorrecta'}, status=401)
            else:
                return JsonResponse({'mensaje': 'Credenciales incorrectas'}, status=401)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)