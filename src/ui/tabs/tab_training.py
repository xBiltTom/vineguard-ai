"""
Pestaña de Configuración de Entrenamiento y Validación Cruzada.
"""

import streamlit as st
import time
from src.locales.i18n import t

def render():
    st.header("⚙️ Configuración de Entrenamiento y Tuning")
    
    st.markdown("""
    En esta sección se configuran los parámetros para el entrenamiento de los 5 modelos (3 clásicos, 2 híbridos).
    Debido a restricciones computacionales, la ejecución real del entrenamiento está optimizada para Google Colab,
    pero aquí se define el flujo (Pipeline) requerido.
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
        <h4>Modelos a Entrenar</h4>
        <ul>
            <li>MobileNetV2 (Clásico - Transfer Learning)</li>
            <li>EfficientNetB0 (Clásico - Transfer Learning)</li>
            <li>DenseNet121 (Clásico - Transfer Learning)</li>
            <li>MobileNet+SVM (Híbrido)</li>
            <li>DenseNet+RF (Híbrido)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    if st.button("🚀 Iniciar Entrenamiento (Simulación)", type="primary"):
        with st.status("Ejecutando Pipeline de Entrenamiento (Simulado)...", expanded=True) as status:
            st.write(f"Iniciando Validacion Cruzada con {cv_folds} folds...")
            time.sleep(1)
            
            progress_bar = st.progress(0)
            
            models = ["MobileNetV2", "EfficientNetB0", "DenseNet121", "Hybrid_SVM", "Hybrid_RF"]
            for i, model in enumerate(models):
                st.write(f"Entrenando {model} con LR={learning_rate}, Dropout={dropout_rate}...")
                for fold in range(1, cv_folds + 1):
                    time.sleep(0.3)
                    progress_bar.progress((i * cv_folds + fold) / (len(models) * cv_folds))
                st.write(f"✅ {model} completado. Guardando como `{model}_best.h5`")
                
            status.update(label="Entrenamiento Finalizado.", state="complete", expanded=False)
            
        st.success("¡El mejor modelo (MobileNetV2) ha sido grabado como `.h5` para inferencia!")
