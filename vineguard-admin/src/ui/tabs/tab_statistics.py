"""
Pestaña de Análisis Estadístico — VineGuard AI.
Muestra MCC real (cuando hay datos de validación) o análisis de velocidad de inferencia.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.locales.i18n import t


def render():
    """Renderiza la pestaña de Análisis Estadístico."""
    st.header(f"📊 {t('statistical.title')}")

    # Verificar si hay análisis de validación real disponible
    if st.session_state.mcnemar_analysis and st.session_state.mcnemar_analysis.get('real_data', False):
        # Mostrar análisis real de múltiples imágenes
        analysis = st.session_state.mcnemar_analysis

        st.success(f"✅ **{t('statistical.real_data_available')}** (de validación McNemar)")

        # Coeficiente de Matthews REAL
        st.subheader(f"📈 {t('statistical.mcc_title')}")

        st.markdown(f"""
        <div class="tech-box">
            <h4>🧮 ¿Qué es el Coeficiente de Matthews?</h4>
            <p>{t('statistical.mcc_description')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar MCC para cada modelo
        col1, col2 = st.columns([2, 1])

        with col1:
            # Tabla de MCC
            mcc_data = []
            for mcc_result in analysis['matthews_coefficients']:
                mcc_data.append({
                    'Modelo': mcc_result['model'],
                    'MCC': f"{mcc_result['mcc']:.3f}",
                    'Interpretación': mcc_result['interpretation']
                })

            mcc_df = pd.DataFrame(mcc_data)
            st.table(mcc_df)

        with col2:
            # Gráfico de MCC
            fig, ax = plt.subplots(figsize=(6, 4))
            models = [m['model'] for m in analysis['matthews_coefficients']]
            mccs = [m['mcc'] for m in analysis['matthews_coefficients']]

            bars = ax.bar(models, mccs, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
            ax.set_ylabel('Coeficiente de Matthews')
            ax.set_title('MCC por Modelo (Datos Reales)')
            ax.set_ylim(-1, 1)
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)

            # Añadir valores en las barras
            for bar, mcc in zip(bars, mccs):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{mcc:.3f}', ha='center', va='bottom')

            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        # Comparación general
        st.subheader(f"🏆 {t('statistical.model_ranking')}")

        # Ordenar modelos por MCC
        mcc_sorted = sorted(analysis['matthews_coefficients'], key=lambda x: x['mcc'], reverse=True)

        st.write(f"**{t('statistical.model_ranking')} basado en Coeficiente de Matthews (Datos Reales):**")
        for i, model_result in enumerate(mcc_sorted):
            if i == 0:
                st.success(f"🥇 **1º lugar:** {model_result['model']} (MCC: {model_result['mcc']:.3f})")
            elif i == 1:
                st.info(f"🥈 **2º lugar:** {model_result['model']} (MCC: {model_result['mcc']:.3f})")
            elif i == 2:
                st.warning(f"🥉 **3º lugar:** {model_result['model']} (MCC: {model_result['mcc']:.3f})")
            else:
                st.write(f"**{i+1}º lugar:** {model_result['model']} (MCC: {model_result['mcc']:.3f})")

        # Información del dataset usado
        st.info(f"**Tamaño de muestra:** {analysis['sample_size']} imágenes reales")

    # Si tenemos predicciones de una imagen, mostrar solo análisis de velocidad
    elif st.session_state.predictions:
        st.subheader(f"⚡ {t('statistical.speed_analysis')}")

        # Obtener datos de velocidad
        model_names = [result['model_name'] for result in st.session_state.predictions]
        inference_times = [result['inference_time'] for result in st.session_state.predictions]

        # Crear gráfico circular
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Gráfico circular de distribución de tiempos
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12'][:len(model_names)]
        wedges, texts, autotexts = ax1.pie(inference_times,
                                           labels=model_names,
                                           autopct='%1.1f ms',
                                           colors=colors,
                                           startangle=90)
        ax1.set_title(t('statistical.inference_time_distribution'))

        # Hacer el texto más legible
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # Gráfico de barras comparativo
        bars = ax2.bar(range(len(model_names)), inference_times, color=colors)
        ax2.set_xlabel('Modelos')
        ax2.set_ylabel('Tiempo (ms)')
        ax2.set_title(t('statistical.speed_comparison'))
        ax2.set_xticks(range(len(model_names)))
        ax2.set_xticklabels([name.replace(' ', '\n') for name in model_names], rotation=0)

        # Añadir valores en las barras
        for bar, time_val in zip(bars, inference_times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                     f'{time_val:.1f}ms', ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig)

        # Métricas de velocidad
        col1, col2, col3 = st.columns(3)

        with col1:
            fastest_idx = np.argmin(inference_times)
            st.success(f"**🚀 {t('statistical.fastest')}**\n{model_names[fastest_idx]}\n{inference_times[fastest_idx]:.1f} ms")

        with col2:
            slowest_idx = np.argmax(inference_times)
            st.error(f"**🐌 {t('statistical.slowest')}**\n{model_names[slowest_idx]}\n{inference_times[slowest_idx]:.1f} ms")

        with col3:
            avg_time = np.mean(inference_times)
            st.info(f"**⏱️ {t('statistical.average')}**\nTodos los modelos\n{avg_time:.1f} ms")

        # Estadísticas adicionales de velocidad
        st.markdown(f"**📈 {t('statistical.speed_stats')}:**")
        speed_stats = pd.DataFrame({
            'Modelo': model_names,
            'Tiempo (ms)': [f"{t_val:.1f}" for t_val in inference_times],
            'Velocidad Relativa': [f"{(min(inference_times)/t_val)*100:.1f}%" for t_val in inference_times],
            'Diferencia vs Más Rápido': [f"+{t_val-min(inference_times):.1f} ms" if t_val != min(inference_times) else "Baseline" for t_val in inference_times]
        })
        st.table(speed_stats)

        # Nota sobre análisis estadístico
        st.warning(f"""
        ⚠️ **{t('statistical.no_statistical_analysis')}**
        
        {t('statistical.statistical_info')}
        
        {t('statistical.why_multiple_images')}
        """)

    else:
        # No hay datos disponibles
        st.info(f"👆 {t('statistical.perform_analysis')}")

        # Mostrar información sobre las pruebas estadísticas
        st.subheader(f"📚 {t('info.statistical_tests')}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            **🧮 {t('info.mcc_technical')}**
            
            {t('statistical.technical_info.mcc_description')}
            """)

        with col2:
            st.markdown(f"""
            **🔬 {t('info.mcnemar_technical')}**
            
            {t('statistical.technical_info.mcnemar_description')}
            """)
