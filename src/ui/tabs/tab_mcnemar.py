"""
Pestaña de Validación McNemar — VineGuard AI.
Maneja la carga de imágenes por carpetas, procesamiento estadístico,
visualizaciones y generación del reporte estadístico PDF.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.locales.i18n import t
from src.core.inference import get_disease_folder_info
from src.utils.config import DISEASE_CLASSES
from src.core.statistics_core import (
    perform_mcnemar_analysis,
    create_validation_results_display,
    generate_interpretation_for_professor,
    process_multiple_images_by_folders,
    create_beautiful_validation_charts
)
from src.utils.pdf_generator import generate_statistical_report_pdf
from datetime import datetime


def get_disease_folders_dynamic():
    """Configuración de carpetas de enfermedades (actualizada dinámicamente según el idioma)."""
    return {
        get_disease_folder_info("Black_rot")['name']: {
            "key": "Black_rot",
            "icon": "🔴",
            "description": get_disease_folder_info("Black_rot")['description'],
            "css_class": "black-rot"
        },
        get_disease_folder_info("Esca")['name']: {
            "key": "Esca",
            "icon": "🟤",
            "description": get_disease_folder_info("Esca")['description'],
            "css_class": "esca"
        },
        get_disease_folder_info("Healthy")['name']: {
            "key": "Healthy",
            "icon": "✅",
            "description": get_disease_folder_info("Healthy")['description'],
            "css_class": "healthy"
        },
        get_disease_folder_info("Leaf_blight")['name']: {
            "key": "Leaf_blight",
            "icon": "🟡",
            "description": get_disease_folder_info("Leaf_blight")['description'],
            "css_class": "leaf-blight"
        }
    }


def render():
    """Renderiza la pestaña de Validación McNemar."""
    st.header(f"🔬 {t('mcnemar.title')}")

    if not st.session_state.models_loaded:
        st.warning(f"👈 {t('sidebar.load_models_warning')}")
    else:
        # ====== TEORÍA AL INICIO ======
        st.markdown(f"### 📚 {t('mcnemar.theoretical_foundations')}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="tech-box">
            <h4>{t('mcnemar.mcc_theory_title')}</h4>
            <p><strong>{t('mcnemar.mcc_theory_formula')}</strong></p>
            <p><strong>{t('mcnemar.mcc_theory_purpose')}</strong></p>
            <p><strong>{t('mcnemar.mcc_theory_advantages')}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="tech-box">
            <h4>{t('mcnemar.mcnemar_theory_title')}</h4>
            <p><strong>{t('mcnemar.mcnemar_theory_formula')}</strong></p>
            <p><strong>{t('mcnemar.mcnemar_theory_purpose')}</strong></p>
            <p><strong>{t('mcnemar.mcnemar_theory_application')}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ====== INTERFAZ DINÁMICA CON CARPETAS ======
        st.markdown(f"""
        **📁 {t('mcnemar.smart_folder_system')}**
        
        📋 **{t('mcnemar.instructions_title')}**
        """)

        for instruction in t('mcnemar.instructions'):
            st.markdown(f"- {instruction}")

        st.subheader(f"🗂️ {t('mcnemar.disease_folders')}")

        # Crear las 4 carpetas dinámicas
        disease_files = {}

        # Layout en grid 2x2
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        columns = [row1_col1, row1_col2, row2_col1, row2_col2]

        # Obtener carpetas de enfermedades dinámicamente
        DISEASE_FOLDERS = get_disease_folders_dynamic()
        disease_names = list(DISEASE_FOLDERS.keys())

        for i, (disease_name, col) in enumerate(zip(disease_names, columns)):
            with col:
                folder_info = DISEASE_FOLDERS[disease_name]

                st.markdown(f"""
                <div class="tech-box">
                <h4 style="text-align: center; margin-bottom: 10px;">
                {folder_info['icon']} {disease_name}
                </h4>
                <p style="text-align: center; font-size: 0.9em; margin-bottom: 0;">
                {folder_info['description']}
                </p>
                </div>
                """, unsafe_allow_html=True)

                # File uploader para cada enfermedad
                uploaded_files = st.file_uploader(
                    f"{t('mcnemar.upload_images')} {disease_name}",
                    type=['jpg', 'jpeg', 'png'],
                    accept_multiple_files=True,
                    key=f"files_{disease_name}",
                    help=f"Arrastra aquí las imágenes de {disease_name}"
                )

                if uploaded_files:
                    disease_files[disease_name] = uploaded_files
                    st.success(f"✅ {len(uploaded_files)} {t('mcnemar.images_loaded')}")
                else:
                    disease_files[disease_name] = []

        # ====== RESUMEN DEL DATASET ======
        total_images = sum(len(files) for files in disease_files.values())

        if total_images > 0:
            st.markdown("---")
            st.subheader(f"📊 {t('mcnemar.dataset_summary')}")

            # Mostrar distribución
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(f"**{t('mcnemar.distribution_by_disease')}**")
                for disease_name, files in disease_files.items():
                    if len(files) > 0:
                        icon = DISEASE_FOLDERS[disease_name]["icon"]
                        st.write(f"{icon} **{disease_name}:** {len(files)} {t('mcnemar.images')}")

                st.markdown(f"**📈 {t('mcnemar.total')}** {total_images} {t('mcnemar.images')}")

                # Recomendaciones
                if total_images < 30:
                    st.warning(f"⚠️ {t('mcnemar.minimum_recommendation')}")
                else:
                    st.success(f"✅ {t('mcnemar.sufficient_dataset')}")

            with col2:
                # Gráfico de distribución
                if total_images > 0:
                    labels = []
                    sizes = []
                    colors = []

                    color_map = {
                        get_disease_folder_info("Black_rot")['name']: "#8C4545",
                        get_disease_folder_info("Esca")['name']: "#A67C52",
                        get_disease_folder_info("Healthy")['name']: "#415D48",
                        get_disease_folder_info("Leaf_blight")['name']: "#C49A45"
                    }

                    for disease_name, files in disease_files.items():
                        if len(files) > 0:
                            labels.append(disease_name.replace(" ", "\n"))
                            sizes.append(len(files))
                            colors.append(color_map[disease_name])

                    if sizes:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.0f%%',
                                                          colors=colors, startangle=90)
                        ax.set_title(f'{t("mcnemar.dataset_summary")}', fontweight='bold')

                        # Mejorar legibilidad
                        for autotext in autotexts:
                            autotext.set_color('white')
                            autotext.set_fontweight('bold')

                        plt.tight_layout()
                        st.pyplot(fig)

            # ====== BOTÓN DE PROCESAMIENTO ======
            st.markdown("---")

            col1, col2, col3 = st.columns([0.1, 8, 0.1])

            with col2:
                if st.button(f"🚀 {t('mcnemar.process_button')}", type="primary", use_container_width=True):
                    with st.spinner(f"🔄 {t('mcnemar.processing')}"):

                        # Procesar imágenes por carpetas
                        validation_data, error = process_multiple_images_by_folders(
                            disease_files, st.session_state.models
                        )

                        if error:
                            st.error(f"❌ Error: {error}")
                        else:
                            # Calcular estadísticas con datos reales
                            mcnemar_analysis = perform_mcnemar_analysis(validation_data)

                            # Guardar en session_state para uso posterior
                            st.session_state.mcnemar_validation = validation_data
                            st.session_state.mcnemar_analysis = mcnemar_analysis

                            # ====== MOSTRAR RESULTADOS DESTACADOS ======
                            st.markdown(f"""
                            <div class="tech-box" style="text-align: center; border-top: 4px solid #415D48;">
                            <span class="lab-ticket-eyebrow" style="margin-bottom: 10px;">ESTADO DEL PROCESO</span>
                            <h2 style="margin-bottom: 10px;">✅ {t('mcnemar.analysis_completed')}</h2>
                            <p style="font-size: 1.1em;">{t('mcnemar.analysis_success')}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            # ====== GRÁFICOS BONITOS Y ELEGANTES ======
                            st.subheader(f"📊 {t('mcnemar.complete_visualization')}")

                            # Crear y mostrar los gráficos bonitos
                            fig_beautiful = create_beautiful_validation_charts(validation_data, mcnemar_analysis)
                            st.pyplot(fig_beautiful)

                            # === RESUMEN DE PRECISIÓN COMPACTO Y ELEGANTE ===
                            st.subheader(f"📊 {t('mcnemar.precision_summary')}")

                            results_df = create_validation_results_display(validation_data, mcnemar_analysis)

                            # Crear filas de 3 columnas máximo
                            rows_needed = (len(results_df) + 2) // 3
                            for row_idx in range(rows_needed):
                                cols = st.columns(3)

                                for col_idx in range(3):
                                    model_idx = row_idx * 3 + col_idx
                                    if model_idx < len(results_df):
                                        _, row = list(results_df.iterrows())[model_idx]

                                        with cols[col_idx]:
                                            modelo = row['Modelo']
                                            precision = row['Precisión']
                                            muestras = row['Muestras Correctas']

                                            # Extraer número de precisión
                                            precision_num = float(precision.replace('%', ''))

                                            # Emoji según tipo
                                            prefix = "🌟" if "Hybrid" in modelo else "🤖"

                                            # Color según rendimiento
                                            if precision_num >= 95:
                                                st.success(f"{prefix} **{modelo}**\n\n🏆 **{precision}**\n\n📊 {muestras}")
                                            elif precision_num >= 90:
                                                st.info(f"{prefix} **{modelo}**\n\n🎯 **{precision}**\n\n📊 {muestras}")
                                            elif precision_num >= 85:
                                                st.warning(f"{prefix} **{modelo}**\n\n⚡ **{precision}**\n\n📊 {muestras}")
                                            else:
                                                st.error(f"{prefix} **{modelo}**\n\n⚠️ **{precision}**\n\n📊 {muestras}")

                            # ====== MCC CON VISUALIZACIÓN MEJORADA ======
                            st.subheader(f"📈 {t('mcnemar.mcc_analysis')}")

                            matthews_coefficients = mcnemar_analysis['matthews_coefficients']
                            best_model = mcnemar_analysis.get('best_model', 'N/A')

                            # Destacar el mejor modelo
                            st.markdown(f"""
                            <div class="tech-box" style="text-align: center;">
                            <h4>🏆 {t('mcnemar.best_model_identified')}</h4>
                            <h2 style="margin: 10px 0;">{best_model}</h2>
                            <p>{t('mcnemar.based_on_mcc')}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            # Tabla detallada de MCC
                            col1, col2 = st.columns([3, 2])
                            with col1:
                                mcc_data = []
                                for mcc_result in matthews_coefficients:
                                    mcc_data.append({
                                        'Modelo': mcc_result['model'],
                                        'MCC': f"{mcc_result['mcc']:.3f}",
                                        'Interpretación': mcc_result['interpretation']
                                    })
                                mcc_df = pd.DataFrame(mcc_data)
                                st.dataframe(mcc_df, use_container_width=True)

                            with col2:
                                # Ranking visual
                                mcc_sorted = sorted(matthews_coefficients, key=lambda x: x['mcc'], reverse=True)
                                st.markdown(f"**🏆 {t('mcnemar.mcc_ranking')}**")
                                for i, model_result in enumerate(mcc_sorted):
                                    if i == 0:
                                        st.success(f"🥇 {model_result['model']} ({model_result['mcc']:.3f})")
                                    elif i == 1:
                                        st.info(f"🥈 {model_result['model']} ({model_result['mcc']:.3f})")
                                    elif i == 2:
                                        st.warning(f"🥉 {model_result['model']} ({model_result['mcc']:.3f})")
                                    else:
                                        st.write(f"**{i+1}º** {model_result['model']} ({model_result['mcc']:.3f})")

                            # ====== RESULTADOS DE MCNEMAR ELEGANTES ======
                            st.subheader(f"🔬 {t('mcnemar.mcnemar_comparisons')}")

                            # Información del mejor modelo
                            st.info(f"**🏆 {t('mcnemar.reference_model')}** {best_model} {t('mcnemar.best_according_mcc')}")
                            st.write(t('mcnemar.comparing_models').format(model=best_model))

                            # Resumen ejecutivo de McNemar
                            mcnemar_results = mcnemar_analysis['mcnemar_results']
                            significant_count = len([r for r in mcnemar_results if r['p_value'] < 0.05])

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(t('mcnemar.total_comparisons'), len(mcnemar_results))
                            with col2:
                                st.metric(t('mcnemar.significant_differences'), significant_count,
                                          delta=f"{(significant_count/len(mcnemar_results)*100):.0f}%" if len(mcnemar_results) > 0 else "0%")
                            with col3:
                                st.metric(t('mcnemar.confidence_level'), "95%", delta="α = 0.05")

                            # Mostrar comparaciones en formato elegante
                            for i, mcnemar_result in enumerate(mcnemar_results):
                                with st.expander(f"📊 {t('mcnemar.comparison')} {i+1}: {mcnemar_result['model1']} vs {mcnemar_result['model2']}", expanded=True):
                                    col1, col2, col3, col4 = st.columns(4)

                                    with col1:
                                        st.metric(t('mcnemar.chi_square_statistic'), f"{mcnemar_result['statistic']:.3f}")
                                    with col2:
                                        st.metric(t('mcnemar.p_value'), f"{mcnemar_result['p_value']:.4f}")
                                    with col3:
                                        significance = "SÍ" if mcnemar_result['p_value'] < 0.05 else "NO"
                                        st.metric(t('mcnemar.significant_question'), significance)
                                    with col4:
                                        if mcnemar_result['p_value'] < 0.05:
                                            st.error(f"**{t('mcnemar.significant_difference')}**")
                                        else:
                                            st.success(f"**{t('mcnemar.no_difference')}**")

                                    # Interpretación específica
                                    st.write(f"**{t('mcnemar.interpretation')}** {mcnemar_result['interpretation']}")

                            # ====== INTERPRETACIÓN PARA EL PROFESOR ======
                            interpretation = generate_interpretation_for_professor(mcnemar_analysis, validation_data)

                            st.markdown(f"""
                            <div class="tech-box">
                            <h4>🎓 {t('mcnemar.academic_interpretation')}</h4>
                            <p>{interpretation.replace(chr(10), '<br>')}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            # ====== BOTÓN PARA GENERAR REPORTE PDF ESTADÍSTICO ======
                            st.subheader(f"📄 {t('mcnemar.generate_statistical_report')}")

                            # Generar PDF automáticamente (SIN botón intermedio)
                            try:
                                with st.spinner(f"🔄 {t('mcnemar.preparing_report')}"):
                                    statistical_pdf_bytes = generate_statistical_report_pdf(validation_data, mcnemar_analysis)

                                # Solo mostrar el download button
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col2:
                                    st.download_button(
                                        label=f"💾 {t('mcnemar.download_statistical_pdf')}",
                                        data=statistical_pdf_bytes,
                                        file_name=f"reporte_estadistico_vineguard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                        mime="application/pdf",
                                        type="primary",
                                        use_container_width=True
                                    )
                                    st.success(f"✅ {t('mcnemar.report_ready')}")

                            except Exception as e:
                                st.error(f"❌ Error generando reporte: {str(e)}")

                            # ====== ENLACE A ANÁLISIS COMPLETO ======
                            st.info(f"""
                            ✅ **{t('mcnemar.complete_results_available')}**
                            
                            {t('mcnemar.explore_detailed_visualizations')}
                            """)

        else:
            st.info(f"📁 {t('mcnemar.load_images_message')}")
