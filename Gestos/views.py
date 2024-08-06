from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import cv2
import torch
from Usuarios.models import Usuario
from .models import Gestos
from Traduccion.models import Traduccion
from .evaluate import get_transform, load_model
from PIL import Image

@method_decorator(csrf_exempt, name='dispatch')
class SignLanguageTranslationView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener el archivo de imagen del request
            image_file = request.FILES.get('image')
            if not image_file:
                return JsonResponse({'error': 'No se ha proporcionado ninguna imagen'}, status=400)

            # Leer la imagen usando OpenCV
            image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

            # Convertir la imagen de OpenCV (numpy array) a PIL.Image
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Aplicar transformaciones y añadir dimensión de batch
            image = get_transform()(image).unsqueeze(0)

            # Cargar el modelo
            model = load_model()

            # Realizar predicción
            with torch.no_grad():
                outputs = model(image)
                _, predicted = torch.max(outputs, 1)
                predicted_class = predicted.item()

            # Obtener la descripción del gesto
            gesto, created = Gestos.objects.get_or_create(id=predicted_class, defaults={'descripcion': f'Gesto {predicted_class}'})

            # Obtener el usuario con ID 16
            try:
                usuario = Usuario.objects.get(id=1)  # Usa Usuario en lugar de User
            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuario con ID 16 no encontrado'}, status=404)

            # Guardar la traducción
            traduccion = Traduccion(
                textoTraducido=gesto.descripcion,
                mostrar=gesto.descripcion,
                usuario=usuario,  # Asignar el usuario con ID 16
                sistema=None,  # Ajusta esto si tienes un sistema específico
            )
            traduccion.save()

            return JsonResponse({'textoTraducido': gesto.descripcion}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
