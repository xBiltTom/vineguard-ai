"""
Módulo de inferencia para VineGuard AI.
Contiene las funciones de predicción, helpers de nombres de enfermedades
y recomendaciones de tratamiento.
"""

import numpy as np
import time
import streamlit as st

from src.utils.config import DISEASE_CLASSES
from src.utils.image_utils import preprocess_image
from src.locales.i18n import t


def get_disease_name(disease_key, lang=None):
    """Función helper para obtener nombres de enfermedades traducidos."""
    if lang is None:
        lang = st.session_state.get('language', 'es')
    return t(f'diseases.{disease_key}', lang)


def get_disease_folder_info(disease_key, lang=None):
    """Función helper para obtener información de carpetas de enfermedades."""
    if lang is None:
        lang = st.session_state.get('language', 'es')
    return {
        'name': t(f'disease_folders.{disease_key}.name', lang),
        'description': t(f'disease_folders.{disease_key}.description', lang)
    }


def predict_disease(image, model, model_name):
    """Realiza predicción con un modelo específico."""
    # Preprocesar imagen con el modelo específico
    processed_img = preprocess_image(image, model_name=model_name)

    # Predicción
    start_time = time.time()
    predictions = model.predict(processed_img, verbose=0)
    inference_time = (time.time() - start_time) * 1000  # ms

    # Obtener clase predicha
    if "Hybrid" in model_name:
        pred_sum = np.sum(predictions[0])
        if pred_sum < 0.1 or pred_sum > 10.0:
            # Las predicciones están mal, usar distribución uniforme
            predictions[0] = np.ones(len(DISEASE_CLASSES)) / len(DISEASE_CLASSES)
            print(f"⚠️ Predicciones corregidas para {model_name}")

    predicted_class_idx = np.argmax(predictions[0])
    predicted_class = DISEASE_CLASSES[predicted_class_idx]
    confidence = predictions[0][predicted_class_idx]

    return {
        'model_name': model_name,
        'predicted_class': predicted_class,
        'predicted_class_es': get_disease_name(predicted_class),
        'confidence': confidence,
        'all_predictions': predictions[0],
        'inference_time': inference_time,
        'predicted_class_idx': predicted_class_idx  # Añadido para análisis estadístico
    }


def get_treatment_recommendations(disease, lang=None):
    """Obtiene recomendaciones de tratamiento según la enfermedad."""
    if lang is None:
        lang = st.session_state.get('language', 'es')

    treatment_data = t(f'treatments.{disease}', lang)

    if treatment_data and not isinstance(treatment_data, str):  # Si no es un string de error
        return {
            "titulo": treatment_data['title'],
            "gravedad": treatment_data['severity'],
            "tratamiento": treatment_data['treatment'],
            "prevencion": treatment_data['prevention']
        }
    else:
        # Fallback si no se encuentra la traducción
        return {
            "titulo": f"Información no disponible para {disease}",
            "gravedad": "N/A",
            "tratamiento": ["Consulte con un especialista"],
            "prevencion": ["Consulte con un especialista"]
        }
