"""
Pestaña de Dashboard y Análisis Exploratorio de Datos (EDA).
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from src.locales.i18n import t

def load_dataset_stats(dataset_path):
    """Cuenta el número de imágenes por cada subcarpeta en el dataset."""
    if not os.path.exists(dataset_path):
        return None
    
    classes = {}
    total_images = 0
    # Asumimos estructura: dataset_path / clase / imagenes.jpg
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

def render():
    st.header("📈 Dashboard & Análisis Exploratorio (EDA)")
    
    # Input para la ruta del dataset
    st.markdown("### 📁 Cargar Dataset")
    col_path, col_btn = st.columns([3, 1])
    with col_path:
        dataset_path = st.text_input("Ruta del dataset en el proyecto:", value="dataset/", help="Ruta relativa o absoluta a la carpeta que contiene las clases.")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True) # Espaciado alineado
        if st.button("📊 Analizar Dataset", use_container_width=True):
            with st.spinner("Analizando directorios..."):
                stats = load_dataset_stats(dataset_path)
                if stats:
                    st.session_state.dataset_stats = stats
                    st.session_state.dataset_path = dataset_path
                    st.success("Dataset cargado y analizado exitosamente.")
                else:
                    st.error(f"No se encontraron imágenes válidas en la ruta: {dataset_path}")

    # Si hay datos cargados, mostramos el EDA
    if 'dataset_stats' in st.session_state and st.session_state.dataset_stats is not None:
        stats = st.session_state.dataset_stats
        
        st.markdown("---")
        st.subheader("🔍 Resultados del Análisis Exploratorio")
        
        # KPIs Rápidos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Imágenes", f"{stats['total']:,}")
        with col2:
            st.metric("Clases Detectadas", len(stats['classes']))
        with col3:
            # Detectar balanceo simple
            min_class = min(stats['classes'].values())
            max_class = max(stats['classes'].values())
            desbalance = "Alto" if (max_class / min_class) > 2 else "Aceptable"
            st.metric("Desbalanceo de Clases", desbalance)
            
        # Gráficos EDA reales
        df = pd.DataFrame(list(stats['classes'].items()), columns=['Clase', 'Cantidad'])
        
        col_plot1, col_plot2 = st.columns(2)
        
        with col_plot1:
            st.markdown("**Distribución de Imágenes por Clase**")
            fig = px.bar(df, x='Clase', y='Cantidad', color='Clase', 
                         color_discrete_sequence=['#8C4545', '#A67C52', '#C49A45', '#415D48', '#5D6D7E', '#1ABC9C'])
            fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
        with col_plot2:
            st.markdown("**Proporción del Dataset**")
            fig2 = px.pie(df, values='Cantidad', names='Clase', hole=0.4,
                          color='Clase', color_discrete_sequence=['#8C4545', '#A67C52', '#C49A45', '#415D48', '#5D6D7E', '#1ABC9C'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("""
        <div class="tech-box">
        <h4>🧹 Nota sobre Limpieza de Datos</h4>
        <p>Al tratarse de un dataset pre-curado de imágenes (PlantVillage), la limpieza tradicional de datos tabulares (outliers, valores nulos) no aplica directamente. 
        El <strong>Análisis Exploratorio de Datos (EDA)</strong> en este contexto se centra en la distribución de clases, la resolución geométrica unificada (típicamente 256x256) 
        y la validación de integridad de los formatos de archivo.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("👆 Por favor, ingresa la ruta de la carpeta de imágenes y presiona 'Analizar Dataset' para visualizar el EDA.")
