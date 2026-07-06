"""
Módulo de gestión de modelos de Machine Learning para VineGuard AI.
Responsable de cargar los modelos .h5 con caché de Streamlit.
"""

import os
import streamlit as st
import tensorflow as tf

from src.utils.config import MODEL_PATHS


@st.cache_resource
def load_models():
    """Carga todos los modelos pre-entrenados con caché de Streamlit."""
    models = {}
    for name, path in MODEL_PATHS.items():
        if os.path.exists(path):
            try:
                models[name] = tf.keras.models.load_model(path)
                print(f"✓ Modelo {name} cargado exitosamente")
            except Exception as e:
                st.error(f"Error al cargar {name}: {str(e)}")
        else:
            st.warning(f"No se encontró el modelo {name} en {path}")
    return models
