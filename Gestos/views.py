from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import cv2
from Usuarios.models import Usuario
from .models import Gestos
from Traduccion.models import Traduccion
from PIL import Image
from tensorflow.keras.models import load_model
import os

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
            if image is None:
                return JsonResponse({'error': 'No se pudo leer la imagen'}, status=400)

            # Redimensionar la imagen
            image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            # Convertir la imagen a un array numpy y darle la forma adecuada para el modelo
            image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
            image_array = (image_array / 127.5) - 1  # Normalización

            # Cargar el modelo
            model_path = os.path.join('Data', 'keras_model.h5')
            model = load_model(model_path, compile=False)

            # Realizar la predicción
            prediction = model.predict(image_array)
            predicted_class = np.argmax(prediction)
            
            # Cargar las etiquetas
            labels_path = os.path.join('Data', 'labels.txt')
            with open(labels_path, "r") as file:
                class_names = file.readlines()

            # Obtener la descripción del gesto
            gesture_description = class_names[predicted_class].strip()

            # Obtener el usuario con ID 1
            try:
                usuario = Usuario.objects.get(id=1)  # Usa Usuario en lugar de User
            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuario con ID 1 no encontrado'}, status=404)

            # Guardar la traducción
            traduccion = Traduccion(
                textoTraducido=gesture_description,
                mostrar=gesture_description,
                usuario=usuario,  # Asignar el usuario con ID 1
                sistema=None,  # Ajusta esto si tienes un sistema específico
            )
            traduccion.save()

            return JsonResponse({'textoTraducido': gesture_description}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
