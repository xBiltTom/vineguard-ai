"""
Módulo de gestión de modelos de Machine Learning para VineGuard AI.
Responsable de cargar los modelos con caché de Streamlit.
"""

import os
import gc
import json
import h5py
import streamlit as st
import keras

from src.utils.config import MODEL_PATHS


# ============================================================
#  COMPATIBILIDAD: DTypePolicy shim
#  Keras 3.0–3.4 serializaba dtype como un objeto DTypePolicy.
#  Keras 3.5+ lo espera como string simple ('float32').
#  Registramos un shim para que Keras 3.15 pueda leer los
#  archivos guardados con versiones anteriores sin errores.
# ============================================================

class _DTypePolicyShim:
    """Clase de compatibilidad para deserializar DTypePolicy de Keras antiguo."""
    def __init__(self, name='float32', **kwargs):
        self.name = name

    def get_config(self):
        return {'name': self.name}

    @classmethod
    def from_config(cls, config):
        return cls(**config)


_CUSTOM_OBJECTS = {'DTypePolicy': _DTypePolicyShim}


# ============================================================
#  PARCHE MÍNIMO PARA ARCHIVOS .h5 LEGACY
#  Solo arregla batch_shape → batch_input_shape (Keras 2).
#  DTypePolicy se maneja via custom_object_scope al cargar.
# ============================================================

def _patch_batch_shape(filepath: str):
    """
    Arregla en disco el parámetro batch_shape → batch_input_shape
    que Keras 2 usaba en InputLayer y Keras 3 ya no reconoce.
    Solo aplica a archivos .h5; los .keras no necesitan este parche.
    """
    if not filepath.endswith('.h5'):
        return
    try:
        with h5py.File(filepath, 'r+') as f:
            raw = f.attrs.get('model_config')
            if raw is None:
                return
            config_str = raw.decode('utf-8') if isinstance(raw, bytes) else raw
            if '"batch_shape"' in config_str:
                fixed = config_str.replace('"batch_shape"', '"batch_input_shape"')
                f.attrs['model_config'] = fixed.encode('utf-8')
                print(f"  🔧 {filepath} — batch_shape parcheado.")
    except Exception as exc:
        print(f"  ⚠️  No se pudo parchear {filepath}: {exc}")


# Aplicar parche mínimo al importar el módulo (solo afecta .h5)
print("🩺 VineGuard — Verificando compatibilidad de modelos…")
for _name, _path in MODEL_PATHS.items():
    if os.path.exists(_path):
        _patch_batch_shape(_path)
print("✅ Verificación completada.")


# ============================================================
#  CARGA CON CACHÉ INDIVIDUAL
# ============================================================

@st.cache_resource
def load_single_model(name: str):
    """
    Carga UN modelo por nombre con caché de Streamlit.
    Usa custom_object_scope para manejar DTypePolicy de versiones
    antiguas de Keras sin modificar los archivos en disco.
    """
    path = MODEL_PATHS.get(name)
    if path is None or not os.path.exists(path):
        return None

    try:
        with keras.utils.custom_object_scope(_CUSTOM_OBJECTS):
            model = keras.models.load_model(path, compile=False)
        gc.collect()
        print(f"  ✓ {name} cargado correctamente.")
        return model
    except Exception as e:
        print(f"  ❌ Error cargando {name}: {type(e).__name__}: {str(e)[:200]}")
        return None


def load_models():
    """Wrapper de compatibilidad: carga todos los modelos."""
    return {name: load_single_model(name) for name in MODEL_PATHS}
