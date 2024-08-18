import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D
import os
import time

# Desactivar la notación científica para mayor claridad
np.set_printoptions(suppress=True)

# Función para eliminar el parámetro 'groups' de la configuración
def eliminar_groups(config):
    if 'groups' in config:
        del config['groups']
    return config

# Función para crear una capa DepthwiseConv2D personalizada
def custom_depthwise_conv2d(**kwargs):
    kwargs = eliminar_groups(kwargs)
    return DepthwiseConv2D(**kwargs)

# Definir objetos personalizados para cargar el modelo
objetos_personalizados = {
    'DepthwiseConv2D': custom_depthwise_conv2d
}

# Cargar el modelo desde la carpeta 'data'
def load_model():
    modelo_path = os.path.join('Data', 'keras_model.h5')
    try:
        modelo = load_model(modelo_path, custom_objects=objetos_personalizados, compile=False)
        print("Modelo cargado exitosamente.")
        return modelo
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        raise

# Cargar las etiquetas
def load_labels():
    labels_path = os.path.join('Data', 'labels.txt')
    try:
        with open(labels_path, "r") as file:
            nombres_clases = file.readlines()
        print("Etiquetas cargadas exitosamente.")
        return nombres_clases
    except Exception as e:
        print(f"Error al cargar las etiquetas: {e}")
        raise

# Función para evaluar el modelo con imágenes de la cámara
def evaluate_model(model, class_names):
    camara = cv2.VideoCapture(0)
    time.sleep(2)

    if not camara.isOpened():
        print("No se pudo abrir la cámara.")
        exit()

    while True:
        ret, imagen = camara.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        try:
            # Preprocesar la imagen
            imagen_resized = cv2.resize(imagen, (224, 224), interpolation=cv2.INTER_AREA)
            imagen_array = np.asarray(imagen_resized, dtype=np.float32).reshape(1, 224, 224, 3)
            imagen_array = (imagen_array / 127.5) - 1

            # Realizar la predicción
            prediccion = model.predict(imagen_array)
            indice = np.argmax(prediccion)
            nombre_clase = class_names[indice].strip()
            puntuacion_confianza = prediccion[0][indice]

            # Imprimir y mostrar la predicción
            print(f"Clase: {nombre_clase}, Puntuación de Confianza: {puntuacion_confianza:.2f}")
            cv2.putText(imagen, f"{nombre_clase} ({puntuacion_confianza:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Imagen de la Webcam", imagen)

        except Exception as e:
            print(f"Error al procesar la imagen: {e}")

        if cv2.waitKey(1) == 27:  # Presionar 'Esc' para salir
            break

    camara.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    model = load_model()
    class_names = load_labels()
    evaluate_model(model, class_names)
