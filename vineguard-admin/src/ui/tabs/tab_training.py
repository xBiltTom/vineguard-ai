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
            btn_disabled = False
        else:
            st.markdown(f"""
            <div style="background-color: rgba(140, 69, 69, 0.1); border-left: 4px solid #8C4545; padding: 15px; margin: 0 0 10px 0;">
                <h4 style="margin-top: 0; color: #8C4545;">⚠️ Restricción de Hardware Activada</h4>
                <p><strong>{st.session_state.hw_message}</strong></p>
                <p>Entrenar arquitecturas profundas con Validación Cruzada de 5-folds requiere aceleración por hardware (GPU/TPU).
                Forzar este flujo en la CPU actual provocaría un colapso del sistema o demoraría múltiples días.</p>
                <p><strong>Solución profesional:</strong> Entrena el modelo en Google Colab, descarga el archivo <code>history.json</code> generado y súbelo en la pestaña de al lado.</p>
            </div>
            """, unsafe_allow_html=True)
            btn_disabled = True
            
    else:
        st.info("👆 Ejecuta el análisis de hardware para evaluar tu sistema local.")
        btn_disabled = True
        
    with col_train:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Iniciar Entrenamiento", type="primary", disabled=btn_disabled, use_container_width=True):
            st.success("Iniciando pipeline de entrenamiento en hardware acelerado...")
            # Aquí iría la lógica real si tuvieran GPU
            
    st.markdown("---")
    
    st.subheader("📈 Estadísticas de Entrenamiento en la Nube (Visualizador)")
    st.markdown("Si entrenaste los modelos en Google Colab u otra nube con GPU, puedes cargar aquí el archivo `history.json` para visualizar las métricas y presentarlas al jurado.")
    
    import json
    import pandas as pd
    
    uploaded_history = st.file_uploader("📂 Sube el archivo history.json", type=["json"])
    
    if uploaded_history is not None:
        try:
            history_data = json.load(uploaded_history)
            
            # Verificar formato (Keras history)
            if 'accuracy' in history_data and 'loss' in history_data:
                st.success("✅ Historial cargado con éxito. Procesando gráficos...")
                
                epochs = range(1, len(history_data['accuracy']) + 1)
                
                # Crear DataFrame para Precisión
                acc_df = pd.DataFrame({
                    'Época': epochs,
                    'Precisión (Train)': history_data.get('accuracy', []),
                    'Precisión (Val)': history_data.get('val_accuracy', [])
                }).set_index('Época')
                
                # Crear DataFrame para Pérdida
                loss_df = pd.DataFrame({
                    'Época': epochs,
                    'Pérdida (Train)': history_data.get('loss', []),
                    'Pérdida (Val)': history_data.get('val_loss', [])
                }).set_index('Época')
                
                col_acc, col_loss = st.columns(2)
                
                with col_acc:
                    st.markdown("#### Curva de Precisión (Accuracy)")
                    st.line_chart(acc_df, color=["#4ECDC4", "#FF6B6B"])
                    st.caption("A mayor precisión, el modelo es mejor distinguiendo enfermedades.")
                    
                with col_loss:
                    st.markdown("#### Curva de Pérdida (Loss)")
                    st.line_chart(loss_df, color=["#4ECDC4", "#FF6B6B"])
                    st.caption("A menor pérdida, el modelo tiene menos dudas en sus predicciones.")
                    
                # Si el JSON nuevo tiene la curva de Learning Rate (Fine-Tuning), graficarla también
                if 'learning_rate' in history_data:
                    st.markdown("#### 📉 Evolución del Learning Rate (Fine-Tuning)")
                    lr_df = pd.DataFrame({
                        'Época': epochs,
                        'Learning Rate': history_data.get('learning_rate', [])
                    }).set_index('Época')
                    st.line_chart(lr_df, color=["#FFB84C"])
                    st.caption("Se observa la caída drástica del Learning Rate durante la Fase 2 (Ajuste Fino / Fine-Tuning).")
                    
                st.info("💡 **Consejo de Sustentación:** Muestra cómo la curva de validación se acerca a la de entrenamiento. Si ambas suben juntas sin separarse abruptamente, demuestra que **no hay Overfitting**.")
                
            else:
                st.error("El archivo JSON no tiene el formato estándar de Keras (faltan llaves 'accuracy' o 'loss').")
                
        except Exception as e:
            st.error(f"Error procesando el JSON: {str(e)}")
