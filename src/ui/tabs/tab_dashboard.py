"""
Pestaña de Dashboard y Análisis Exploratorio de Datos (EDA).
"""

import os
import hashlib
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from src.locales.i18n import t

def get_image_hash(image_path):
    """Calcula el hash MD5 para detectar duplicados."""
    hash_md5 = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_dataset_stats(dataset_path):
    """Cuenta el número de imágenes por cada subcarpeta en el dataset."""
    if not os.path.exists(dataset_path):
        return None
    
    classes = {}
    total_images = 0
    for class_name in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_name)
        if os.path.isdir(class_path):
            images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            count = len(images)
            classes[class_name] = count
            total_images += count
            
    if total_images == 0:
        return None
        
    return {
        'total': total_images,
        'classes': classes
    }

def clean_dataset_ui(input_dir, output_dir, target_size=(224, 224)):
    """Lógica de limpieza ejecutada desde la UI con feedback descriptivo e interactivo."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    classes = [d for d in os.listdir(input_path) if os.path.isdir(input_path / d)]
    if not classes:
        st.error("No se encontraron clases en el directorio original.")
        return
        
    stats = {"procesadas": 0, "corruptas": 0, "duplicadas": 0, "exportadas": 0}
    seen_hashes = set()
    
    # Calcular total para la barra de progreso
    total_files = sum([len([f for f in os.listdir(input_path / c) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]) for c in classes])
    
    if total_files == 0:
        st.error("No hay imágenes válidas para limpiar.")
        return

    # Usar st.status para un panel interactivo que muestra los pasos
    with st.status("🛠️ Ejecutando Pipeline de Limpieza...", expanded=True) as status_panel:
        st.write(f"Iniciando escaneo en: `{input_dir}`")
        st.write(f"Se detectaron {total_files} imágenes repartidas en {len(classes)} clases.")
        
        progress_bar = st.progress(0)
        
        for class_name in classes:
            st.write(f"🔍 **Analizando clase:** `{class_name}`...")
            class_input_dir = input_path / class_name
            class_output_dir = output_path / class_name
            class_output_dir.mkdir(parents=True, exist_ok=True)
            
            images = [f for f in os.listdir(class_input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            
            for img_name in images:
                stats["procesadas"] += 1
                img_path = class_input_dir / img_name
                
                # Actualizar progreso
                if stats["procesadas"] % 20 == 0 or stats["procesadas"] == total_files:
                    progress_bar.progress(stats["procesadas"] / total_files)
                
                # 1. Filtro de integridad (0 KB)
                if os.path.getsize(img_path) == 0:
                    stats["corruptas"] += 1
                    continue
                    
                # 2. Duplicados (Hash MD5)
                img_hash = get_image_hash(img_path)
                if img_hash in seen_hashes:
                    stats["duplicadas"] += 1
                    continue
                    
                # 3. Calidad y Resize
                try:
                    with Image.open(img_path) as img:
                        img.verify() # Comprobar que no esté rota a nivel binario
                    
                    with Image.open(img_path) as img:
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                        
                        new_name = f"{img_hash[:8]}_{img_name}"
                        if not new_name.lower().endswith('.jpg'):
                            new_name = new_name.rsplit('.', 1)[0] + '.jpg'
                            
                        export_path = class_output_dir / new_name
                        img_resized.save(export_path, 'JPEG', quality=95)
                        
                        seen_hashes.add(img_hash)
                        stats["exportadas"] += 1
                except Exception:
                    stats["corruptas"] += 1
                    continue
                    
        status_panel.update(label="✅ Limpieza Finalizada", state="complete", expanded=False)

    # Reporte Final super legible
    st.markdown("### 📋 Reporte de Curación de Datos")
    
    st.markdown(f"""
    <div class="tech-box" style="border-left: 5px solid #415D48;">
        <h4>Resumen de Ejecución</h4>
        <p>El pipeline finalizó el análisis estructural y criptográfico del dataset. A continuación se detallan los resultados:</p>
        <ul>
            <li><strong>Imágenes Totales Escaneadas:</strong> {stats['procesadas']:,}</li>
            <li><strong style="color: #8C4545;">⚠️ Duplicados Eliminados:</strong> {stats['duplicadas']:,} <em>(Detectados vía Hash MD5)</em></li>
            <li><strong style="color: #8C4545;">❌ Archivos Corruptos/Rotos:</strong> {stats['corruptas']:,} <em>(0 KB o falla binaria)</em></li>
            <li><strong style="color: #415D48;">✅ Imágenes Limpias y Normalizadas:</strong> {stats['exportadas']:,} <em>(Exportadas a 224x224 px)</em></li>
        </ul>
        <p><strong>Destino:</strong> <code>{output_dir}</code></p>
    </div>
    """, unsafe_allow_html=True)


def render():
    st.header("📈 Dashboard & Análisis Exploratorio (EDA)")
    
    # Input para la ruta del dataset
    st.markdown("### 📁 1. Cargar Dataset Original")
    col_path, col_btn = st.columns([3, 1])
    with col_path:
        dataset_path = st.text_input("Ruta del dataset sucio:", value="dataset/", key="dataset_path_input")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 Analizar Dataset", use_container_width=True):
            with st.spinner("Analizando directorios..."):
                stats = load_dataset_stats(dataset_path)
                if stats:
                    st.session_state.dataset_stats = stats
                    st.session_state.dataset_path = dataset_path
                    st.success("Dataset cargado exitosamente.")
                else:
                    st.error(f"No se encontraron imágenes válidas en la ruta: {dataset_path}")

    # Si hay datos cargados, mostramos el EDA y la opción de limpiar
    if 'dataset_stats' in st.session_state and st.session_state.dataset_stats is not None:
        stats = st.session_state.dataset_stats
        
        st.markdown("---")
        st.subheader("🔍 2. Análisis Exploratorio (EDA)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Imágenes", f"{stats['total']:,}")
        with col2:
            st.metric("Clases Detectadas", len(stats['classes']))
        with col3:
            min_class = min(stats['classes'].values())
            max_class = max(stats['classes'].values())
            desbalance = "Alto" if (max_class / min_class) > 2 else "Aceptable"
            st.metric("Desbalanceo de Clases", desbalance)
            
        df = pd.DataFrame(list(stats['classes'].items()), columns=['Clase', 'Cantidad'])
        
        col_plot1, col_plot2 = st.columns(2)
        with col_plot1:
            fig = px.bar(df, x='Clase', y='Cantidad', color='Clase', 
                         color_discrete_sequence=['#8C4545', '#A67C52', '#C49A45', '#415D48'])
            fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
        with col_plot2:
            fig2 = px.pie(df, values='Cantidad', names='Clase', hole=0.4,
                          color='Clase', color_discrete_sequence=['#8C4545', '#A67C52', '#C49A45', '#415D48'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("---")
        st.subheader("🧹 3. Pipeline de Limpieza de Datos")
        st.markdown("""
        El pipeline aplicará los siguientes pasos directamente desde esta interfaz, leyendo el dataset original y escribiendo los resultados en la ruta de exportación, evitando saturar la memoria RAM:
        1. **Filtro de Integridad:** Descarte de archivos de 0 KB y corruptos.
        2. **Deduplicación:** Uso de Hash MD5 para eliminar imágenes repetidas.
        3. **Normalización Geométrica:** Redimensionamiento estricto a 224x224 píxeles (formato `.jpg`).
        """)
        
        col_out, col_clean = st.columns([3, 1])
        with col_out:
            output_dir = st.text_input("Ruta de exportación (Dataset Limpio):", value="dataset_cleaned/")
        with col_clean:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🧼 Iniciar Limpieza", type="primary", use_container_width=True):
                clean_dataset_ui(st.session_state.dataset_path, output_dir)
                
    else:
        st.info("👆 Por favor, ingresa la ruta del dataset y presiona 'Analizar Dataset' para visualizar el EDA.")
