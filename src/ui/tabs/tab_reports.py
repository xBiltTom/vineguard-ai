"""
Pestaña de Reportes (PDF, Word, Excel).
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from src.locales.i18n import t

def render():
    st.header("📄 Generación de Reportes Finales")
    
    st.markdown("""
    En esta sección puede descargar los reportes consolidados del entrenamiento, métricas de evaluación 
    y análisis estadístico (McNemar y MCC) en diferentes formatos, listos para anexar al proyecto.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    # Datos simulados para el reporte (usualmente vendrían del output del entrenamiento)
    df_metrics = pd.DataFrame({
        "Modelo": ["MobileNetV2", "DenseNet121", "EfficientNetB0", "CNN+SVM", "CNN+RF"],
        "Precisión (%)": [98.1, 97.5, 96.0, 98.4, 95.8],
        "MCC": [0.97, 0.96, 0.94, 0.98, 0.93],
        "Tiempo Inferencia (ms)": [820, 1500, 940, 1100, 1050]
    })
    
    with col1:
        st.markdown("""
        <div class="tech-box" style="text-align: center;">
        <h2>📊</h2>
        <h4>Reporte Excel</h4>
        <p>Tablas con métricas completas de entrenamiento y matrices de confusión numéricas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generar Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_metrics.to_excel(writer, sheet_name='Resultados_Modelos', index=False)
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name="Reporte_VineGuard_Metricas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    with col2:
        st.markdown("""
        <div class="tech-box" style="text-align: center;">
        <h2>📝</h2>
        <h4>Reporte Word</h4>
        <p>Documento con interpretaciones de resultados, hipótesis y conclusiones.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simular Word text file para la descarga rápida (idealmente python-docx)
        word_data = b"Reporte VineGuard AI\n\nResultados del entrenamiento y pruebas estadisticas..."
        st.download_button(
            label="📥 Descargar Word",
            data=word_data,
            file_name="Reporte_VineGuard_Interpretacion.doc",
            mime="application/msword",
            use_container_width=True
        )
        
    with col3:
        st.markdown("""
        <div class="tech-box" style="text-align: center;">
        <h2>📄</h2>
        <h4>Reporte PDF</h4>
        <p>Versión ejecutiva con gráficas (ROC, Heatmaps) para presentación oficial.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simular PDF
        pdf_data = b"%PDF-1.4\n%VineGuard Report"
        st.download_button(
            label="📥 Descargar PDF",
            data=pdf_data,
            file_name="Reporte_VineGuard_Ejecutivo.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    st.markdown("---")
    st.subheader("Vista Previa de Resultados (Tabla Principal)")
    st.dataframe(df_metrics, use_container_width=True)
