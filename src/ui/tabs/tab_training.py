"""
Pestaña de Configuración de Entrenamiento y Validación Cruzada.
"""

import os
import streamlit as st
from src.locales.i18n import t

def render():
    st.header("⚙️ Configuración de Entrenamiento y Tuning")
    
    st.markdown("""
    En esta sección se configuran los parámetros para el entrenamiento de los 5 modelos (3 clásicos, 2 híbridos).
    Para comenzar, selecciona el dataset sobre el cual se entrenarán los modelos.
    """)
    
    # 1. Selección del Dataset para Entrenar
    st.markdown("### 📁 Selección de Dataset")
    col_path, col_btn = st.columns([3, 1])
    with col_path:
        # Por defecto sugiere la ruta del dataset limpiado si existe
        default_path = "dataset_cleaned/" if os.path.exists("dataset_cleaned/") else "dataset/"
        train_dataset_path = st.text_input("Ruta del dataset para entrenar:", value=default_path, help="Ruta relativa de las imágenes (idealmente el dataset limpiado).")
    
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✔️ Validar Ruta", use_container_width=True):
            if os.path.exists(train_dataset_path):
                classes = [d for d in os.listdir(train_dataset_path) if os.path.isdir(os.path.join(train_dataset_path, d))]
                if classes:
                    st.success(f"Dataset válido con {len(classes)} clases detectadas.")
                    st.session_state.train_dataset_valid = True
                else:
                    st.error("Ruta válida, pero no contiene subcarpetas de clases.")
                    st.session_state.train_dataset_valid = False
            else:
                st.error("La ruta especificada no existe.")
                st.session_state.train_dataset_valid = False

    st.markdown("---")
    
    # Si la ruta no está validada, bloqueamos el resto visualmente
    if not st.session_state.get('train_dataset_valid', False):
        st.info("👆 Por favor, ingresa la ruta del dataset (crudo o limpio) y presiona 'Validar Ruta' para habilitar el panel de entrenamiento.")
        return
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛠️ Hiperparámetros (Tuning)")
        learning_rate = st.selectbox("Tasa de Aprendizaje (Learning Rate)", [0.001, 0.0005, 0.0001])
        dropout_rate = st.slider("Tasa de Dropout (Regularización)", 0.1, 0.6, 0.3, 0.1)
        batch_size = st.selectbox("Tamaño de Lote (Batch Size)", [16, 32, 64])
        epochs = st.number_input("Épocas (Epochs)", min_value=5, max_value=100, value=25)
        
    with col2:
        st.subheader("🔄 Validación Cruzada (CV)")
        cv_folds = st.number_input("Número de Folds (K)", min_value=2, max_value=10, value=5)
        
        st.markdown("""
        <div class="tech-box">
        <h4>Modelos en el Pipeline</h4>
        <ul>
            <li>MobileNetV2 (Transfer Learning)</li>
            <li>EfficientNetB0 (Transfer Learning)</li>
            <li>DenseNet121 (Transfer Learning)</li>
            <li>CNN + SVM (Arquitectura Híbrida)</li>
            <li>CNN + RF (Arquitectura Híbrida)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Restricción de Hardware (Honestidad)
    st.markdown("""
    <div style="background-color: rgba(140, 69, 69, 0.1); border-left: 4px solid #8C4545; padding: 15px; margin: 10px 0;">
        <h4 style="margin-top: 0; color: #8C4545;">⚠️ Entrenamiento Deshabilitado (Restricción de Hardware)</h4>
        <p>Entrenar 5 arquitecturas profundas con Validación Cruzada de 5-folds sobre miles de imágenes requiere de aceleración por hardware (GPU/TPU).
        Ejecutar este flujo en la CPU local provocaría un colapso del sistema o demoraría múltiples días.</p>
        <p><strong>Solución para escalar:</strong> Toma tu carpeta <code>dataset_cleaned/</code>, súbela a Google Drive, y ejecuta la lógica de entrenamiento en Google Colab con hardware gratuito acelerado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("🚫 Iniciar Entrenamiento", type="primary", disabled=True, help="Deshabilitado por falta de GPU.")
