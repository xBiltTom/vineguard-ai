"""
Pestaña de Dashboard y Análisis Exploratorio de Datos (EDA).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.locales.i18n import t

def render():
    st.header("📈 Dashboard & Análisis Exploratorio (EDA)")
    
    st.markdown("""
    <div class="tech-box">
    <h4>📋 Resumen Ejecutivo</h4>
    <p>Bienvenido al Panel de Administración de VineGuard AI. Este dashboard presenta un análisis descriptivo del conjunto de datos utilizado para el entrenamiento de los modelos y métricas globales del sistema.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Rápidos
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Imágenes", "4,062", "PlantVillage Grape")
    with col2:
        st.metric("Clases Detectadas", "4", "Enfermedades + Sano")
    with col3:
        st.metric("Precisión Media", "96.5%", "5 Modelos")
    with col4:
        st.metric("Validación", "5-Folds", "Cross Validation")
        
    st.markdown("---")
    
    st.subheader("🔍 1. Análisis Exploratorio de Datos (EDA)")
    
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        st.markdown("**Distribución de Clases en el Dataset**")
        # Datos simulados basados en PlantVillage Grape
        data = {
            'Clase': ['Black Rot', 'Esca (Black Measles)', 'Leaf Blight', 'Healthy'],
            'Cantidad': [1180, 1383, 1076, 423]
        }
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Clase', y='Cantidad', color='Clase', 
                     color_discrete_sequence=['#8C4545', '#A67C52', '#C49A45', '#415D48'])
        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_plot2:
        st.markdown("**Composición del Dataset**")
        fig2 = px.pie(df, values='Cantidad', names='Clase', hole=0.4,
                      color='Clase', color_discrete_sequence=['#8C4545', '#A67C52', '#C49A45', '#415D48'])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("""
    <div class="tech-box">
    <h4>Estadísticos Descriptivos (Resolución y Canales)</h4>
    <ul>
        <li><strong>Resolución original:</strong> 256x256 píxeles</li>
        <li><strong>Canales de color:</strong> 3 (RGB)</li>
        <li><strong>Preprocesamiento:</strong> Reescalado a [0, 1], aumento de datos (rotación 20°, zoom 15%, volteo horizontal).</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
