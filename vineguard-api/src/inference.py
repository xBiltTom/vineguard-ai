import os
import time
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf

# Definición de clases (las mismas del entrenamiento)
DISEASE_CLASSES = ['Black_rot', 'Esca', 'Healthy', 'Leaf_blight']

# Caché del modelo cargado en RAM
MODEL_CACHE = None

def get_model_path():
    # El archivo exportado por el Admin Streamlit
    return os.path.join(os.path.dirname(__file__), '..', 'best_model', 'best_model.h5')

def load_production_model():
    global MODEL_CACHE
    if MODEL_CACHE is not None:
        return True
        
    model_path = get_model_path()
    if not os.path.exists(model_path):
        print(f"Error: Modelo de producción no encontrado en {model_path}")
        return False
        
    try:
        print(f"Cargando modelo de producción: {model_path}")
        # Custom objects por si se exportó un modelo Híbrido con Capa de Atención
        from tensorflow.keras.layers import Layer
        import tensorflow.keras.backend as K
        
        class AttentionLayer(Layer):
            def __init__(self, **kwargs):
                super(AttentionLayer, self).__init__(**kwargs)
            def build(self, input_shape):
                self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
                self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
                super(AttentionLayer, self).build(input_shape)
            def call(self, x):
                e = K.tanh(K.dot(x, self.W) + self.b)
                a = K.softmax(e, axis=1)
                output = x * a
                return K.sum(output, axis=1)
                
        custom_objects = {'AttentionLayer': AttentionLayer}
        MODEL_CACHE = tf.keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)
        print("Modelo cargado exitosamente en RAM.")
        return True
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return False

def preprocess_image_for_api(img_bytes, target_size=(224, 224)):
    try:
        # Abrir bytes a imagen PIL
        img = Image.open(BytesIO(img_bytes))
        
        # Convertir a RGB (manejar PNGs con alpha)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Resize estricto
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convertir a numpy array y normalizar (MobileNet / VGG / Inception standard)
        img_array = np.array(img, dtype=np.float32)
        # Algunos modelos requieren /255.0, pero asumiendo preprocess_input estándar de tf.keras.applications
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        
        # Añadir dimension batch (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise ValueError(f"Error procesando la imagen: {str(e)}")

def predict_from_bytes(img_bytes):
    if not load_production_model():
        raise RuntimeError("El modelo de producción no está disponible. Entrena y exporta un modelo desde el Panel Admin.")
        
    start_time = time.time()
    
    # Preprocesar
    tensor = preprocess_image_for_api(img_bytes)
    
    # Predecir
    predictions = MODEL_CACHE.predict(tensor, verbose=0)
    inference_time_ms = (time.time() - start_time) * 1000
    
    # Decodificar salida
    probs = predictions[0].tolist()
    class_idx = int(np.argmax(probs))
    confidence = float(probs[class_idx])
    predicted_class = DISEASE_CLASSES[class_idx]
    
    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "inference_time_ms": round(inference_time_ms, 2),
        "probabilities": dict(zip(DISEASE_CLASSES, probs))
    }
