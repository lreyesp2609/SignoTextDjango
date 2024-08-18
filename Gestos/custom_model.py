import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D

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

def load_model_custom():
    current_directory = os.getcwd()
    model_path = os.path.join(current_directory, 'Gestos', 'Data', 'keras_model.h5')
    try:
        model = load_model(model_path, custom_objects=objetos_personalizados, compile=False)
        print("Modelo cargado exitosamente.")
        return model
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        raise

def load_labels():
    current_directory = os.getcwd()
    labels_path = os.path.join(current_directory, 'Gestos', 'Data', 'labels.txt')
    try:
        with open(labels_path, "r") as file:
            class_names = file.readlines()
        print("Etiquetas cargadas exitosamente.")
        return class_names
    except Exception as e:
        print(f"Error al cargar las etiquetas: {e}")
        raise
