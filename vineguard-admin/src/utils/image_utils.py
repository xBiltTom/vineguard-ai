"""
Módulo de utilidades para procesamiento de imágenes.
Contiene funciones de preprocesamiento CLAHE y preparación de imágenes para inferencia.
"""

import numpy as np
import cv2
from PIL import Image
import tensorflow as tf

from tensorflow.keras.preprocessing.image import img_to_array

from src.utils.config import DISEASE_CLASSES


def apply_gentle_clahe(image):
    """Aplicar CLAHE conservador para modelos híbridos"""
    if image.dtype == np.float32:
        image = (image * 255.0).astype(np.uint8)
    elif image.max() <= 1.0:
        image = (image * 255.0).astype(np.uint8)

    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l_channel)

    lab_enhanced = cv2.merge([l_enhanced, a_channel, b_channel])
    rgb_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2RGB)

    return rgb_enhanced


def preprocess_image(image, target_size=(224, 224), model_name=None):
    """Preprocesa la imagen para los modelos"""

    # ===== PREPROCESAMIENTO ESPECIAL PARA MODELOS HÍBRIDOS =====
    if model_name and "Hybrid" in model_name:
        # Aplicar CLAHE conservador para modelos híbridos
        img_array = np.array(image)
        img_enhanced = apply_gentle_clahe(img_array)
        img = Image.fromarray(img_enhanced)
        img = img.resize(target_size)
        img_array = img_to_array(img)
        # Normalizar
        img_array = img_array.astype(np.float32) / 255.0
    else:
        # Preprocesamiento estándar para modelos originales
        img = image.resize(target_size)
        img_array = img_to_array(img)

        if model_name == "EfficientNet":
            img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
        else:
            img_array = img_array / 255.0

    # Expandir dimensiones
    img_array = np.expand_dims(img_array, axis=0)
    return img_array
