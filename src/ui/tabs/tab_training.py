"""
Pestaña de Configuración de Entrenamiento y Validación Cruzada.
"""

import streamlit as st
from src.locales.i18n import t

def render():
    st.header("⚙️ Configuración de Entrenamiento y Tuning")
    
    # 1. Verificar si el dataset fue cargado en la Pestaña 1
    if 'dataset_stats' not in st.session_state or st.session_state.dataset_stats is None:
        st.warning("⚠️ No se ha detectado ningún dataset.")
        st.info("👉 Ve a la sección **1. EDA & Dashboard** para cargar y analizar la carpeta de imágenes antes de intentar configurar el entrenamiento.")
        return
        
    st.markdown(f"**Dataset detectado:** {st.session_state.dataset_path} ({st.session_state.dataset_stats['total']:,} imágenes en {len(st.session_state.dataset_stats['classes'])} clases)")
    st.markdown("---")
    
    st.markdown("""
    En esta sección se configuran los parámetros para el entrenamiento de los 5 modelos (3 clásicos, 2 híbridos).
    """)
    
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
        <p><strong>Solución:</strong> Se recomienda exportar la configuración de hiperparámetros y ejecutar los scripts de entrenamiento en un entorno con GPUs como Google Colab.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("🚫 Iniciar Entrenamiento", type="primary", disabled=True, help="Deshabilitado por falta de GPU.")
