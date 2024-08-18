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
import os

# Importar las funciones personalizadas para cargar el modelo y las etiquetas
from .custom_model import load_model_custom, load_labels

@method_decorator(csrf_exempt, name='dispatch')
class SignLanguageTranslationView(View):
    def post(self, request, *args, **kwargs):
        try:
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

            print("Imagen procesada correctamente")
            
            # Cargar el modelo y las etiquetas
            model = load_model_custom()
            class_names = load_labels()

            # Realizar la predicción
            prediction = model.predict(image_array)
            predicted_class = np.argmax(prediction[0])
            confidence_score = prediction[0][predicted_class]

            print(f"Predicción: {predicted_class}, Confianza: {confidence_score}")

            # Obtener el gesto correspondiente de la base de datos
            gesto = Gestos.objects.filter(id=predicted_class).first()

            # Verificar la confianza antes de devolver el resultado
            if confidence_score >= 0.99 and gesto:
                return JsonResponse({
                    'predicted_class': int(predicted_class),  # Convertir a int de Python
                    'confidence_score': float(confidence_score),
                    'letra': gesto.descripcion
                })
            else:
                return JsonResponse({'error': 'Gesto no reconocido'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)