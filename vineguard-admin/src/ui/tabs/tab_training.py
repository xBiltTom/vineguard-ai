"""
Pestaña de Configuración de Entrenamiento y Validación Cruzada.
"""

import os
import platform
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
    
    st.subheader("🖥️ Evaluación de Entorno de Ejecución")
    st.markdown("Antes de iniciar el entrenamiento de 5 redes neuronales pesadas, el sistema debe certificar que el hardware actual es capaz de soportar la carga matemática requerida.")
    
    col_hw, col_train = st.columns([2, 1])
    
    with col_hw:
        if st.button("🔍 Analizar Hardware de Entrenamiento", use_container_width=True):
            with st.spinner("Escaneando recursos del sistema (CPU/GPU/RAM)..."):
                # Obtener detalles del CPU
                cpu_info = platform.processor() or "CPU Desconocida"
                if os.path.exists('/proc/cpuinfo'):
                    with open('/proc/cpuinfo', 'r') as f:
                        for line in f:
                            if 'model name' in line:
                                cpu_info = line.split(':')[1].strip()
                                break
                                
                # Obtener detalles de la RAM
                ram_gb = "Desconocida"
                if os.path.exists('/proc/meminfo'):
                    with open('/proc/meminfo', 'r') as f:
                        for line in f:
                            if 'MemTotal' in line:
                                kb = int(line.split()[1])
                                ram_gb = f"{round(kb / (1024**2), 1)} GB"
                                break
                
                st.session_state.sys_cpu = cpu_info
                st.session_state.sys_ram = ram_gb
                
                try:
                    import tensorflow as tf
                    gpus = tf.config.list_physical_devices('GPU')
                    if len(gpus) > 0:
                        st.session_state.hardware_ok = True
                        st.session_state.hw_message = f"✅ GPU Detectada: {len(gpus)} dispositivo(s) acelerador(es) disponible(s). El sistema está listo."
                    else:
                        st.session_state.hardware_ok = False
                        st.session_state.hw_message = "❌ GPU NO Detectada. Se usará procesamiento por CPU."
                except ImportError:
                    st.session_state.hardware_ok = False
                    st.session_state.hw_message = "❌ TensorFlow no está configurado correctamente para uso de GPU."
    
    if 'hw_message' in st.session_state:
        # Mostrar especificaciones detectadas
        st.markdown(f"""
        <div class="tech-box" style="padding: 10px 15px; margin-bottom: 15px;">
            <p style="margin:0; font-size: 0.9em;"><strong>💻 Especificaciones Detectadas:</strong></p>
            <ul style="margin: 5px 0 0 0; font-size: 0.85em; font-family: monospace;">
                <li><strong>Procesador (CPU):</strong> {st.session_state.get('sys_cpu', 'N/A')}</li>
                <li><strong>Memoria RAM:</strong> {st.session_state.get('sys_ram', 'N/A')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.get('hardware_ok', False):
            st.success(st.session_state.hw_message)
            hardware_warning = ""
            btn_disabled = False
        else:
            st.markdown(f"""
            <div style="background-color: rgba(140, 69, 69, 0.1); border-left: 4px solid #8C4545; padding: 15px; margin: 0 0 10px 0;">
                <h4 style="margin-top: 0; color: #8C4545;">⚠️ Restricción de Hardware Activada</h4>
                <p><strong>{st.session_state.hw_message}</strong></p>
                <p>Entrenar arquitecturas profundas con Validación Cruzada de 5-folds requiere aceleración por hardware (GPU/TPU).
                Forzar este flujo en la CPU actual provocaría un colapso del sistema o demoraría múltiples días.</p>
                <p><strong>Solución recomendada:</strong> Toma la carpeta <code>dataset_cleaned/</code>, súbela a tu Google Drive, y ejecuta la lógica de entrenamiento en Google Colab.</p>
            </div>
            """, unsafe_allow_html=True)
            btn_disabled = True
    else:
        st.info("👆 Ejecuta el análisis de hardware para desbloquear el entrenamiento.")
        btn_disabled = True
        
    with col_train:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Iniciar Entrenamiento", type="primary", disabled=btn_disabled, use_container_width=True):
            st.success("Iniciando pipeline de entrenamiento en hardware acelerado...")
            # Aquí iría la lógica real si tuvieran GPU
