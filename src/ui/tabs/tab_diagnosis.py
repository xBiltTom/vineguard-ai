"""
Pestaña de Diagnóstico Individual — VineGuard AI.
Maneja la subida de imágenes, predicciones y generación del reporte PDF de diagnóstico.
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from datetime import datetime

from src.locales.i18n import t
from src.core.inference import predict_disease, get_disease_name, get_treatment_recommendations
from src.utils.config import DISEASE_CLASSES, MODEL_PATHS
from src.utils.pdf_generator import generate_diagnosis_pdf
from src.core.model_manager import load_single_model

def render():
    """Renderiza la pestaña de Diagnóstico Individual."""
    st.header(f"🔍 {t('diagnosis.title')}")
    
    # ======= GESTIÓN DE MODELOS (Carga Bajo Demanda) =======
    if not st.session_state.get('models_loaded', False):
        st.warning("⚠️ Para realizar diagnósticos, primero debes cargar los modelos entrenados en memoria.")
        
        # Permitir cargar desde carpeta por defecto (models/)
        if st.button("🚀 Cargar Modelos desde directorio local", type="primary"):
            model_names = list(MODEL_PATHS.keys())
            total = len(model_names)
            loaded = {}
            errors = []

            st.markdown("**Cargando modelos en memoria...**")
            progress_bar = st.progress(0)
            status_text  = st.empty()

            for i, name in enumerate(model_names):
                status_text.markdown(f"⏳ `{name}` ({i+1}/{total})")
                model = load_single_model(name)
                if model is not None:
                    loaded[name] = model
                else:
                    errors.append(name)
                progress_bar.progress((i + 1) / total)

            status_text.empty()

            if loaded:
                st.session_state.models = loaded
                st.session_state.models_loaded = True
                st.success(f"✅ {len(loaded)}/{total} modelos cargados exitosamente.")
                st.rerun()
            else:
                st.error("❌ No se pudo cargar ningún modelo.")
        
        st.markdown("---")
        return  # Detiene el renderizado hasta que los modelos estén cargados
    else:
        st.success("✅ Modelos cargados y listos para inferencia.")
        
    st.markdown("---")

    # Opciones de entrada
    col1, col2 = st.columns([2, 1])
    with col1:
        input_method = st.radio(
            t('diagnosis.input_method'),
            [f"📷 {t('diagnosis.upload_image')}", f"📸 {t('diagnosis.use_camera')}"],
            horizontal=True
        )

    # Subir imagen
    if input_method == f"📷 {t('diagnosis.upload_image')}":
        uploaded_file = st.file_uploader(
            t('diagnosis.file_uploader'),
            type=['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG', 'webp', 'bmp'],
            help=t('diagnosis.formats_help')
        )

        if uploaded_file is not None:
            # Cargar y mostrar imagen
            image = Image.open(uploaded_file).convert('RGB')
            st.session_state.current_image = image

            # Mostrar imagen
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(image, caption=t('diagnosis.image_loaded'), use_column_width=True)

            # Botón de análisis
            if st.button(f"🔬 {t('diagnosis.analyze_button')}", type="primary"):
                with st.spinner(t('diagnosis.analyzing')):
                    # Realizar predicciones con todos los modelos
                    results = []
                    for model_name, model in st.session_state.models.items():
                        result = predict_disease(image, model, model_name)
                        results.append(result)

                    st.session_state.predictions = results

            # Mostrar resultados si existen
            if st.session_state.predictions:
                # Mostrar resultados por modelo
                st.subheader(f"📋 {t('diagnosis.results_title')}")

                # Crear columnas para cada modelo (Cuadrícula de 3 por fila para evitar cortes)
                num_models = len(st.session_state.predictions)
                cols_per_row = 3
                
                for i in range(0, num_models, cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j in range(cols_per_row):
                        if i + j < num_models:
                            result = st.session_state.predictions[i + j]
                            with cols[j]:
                                # Tarjeta personalizada para permitir salto de línea
                                st.markdown(f"""
                                <div style="background-color: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.2); border-radius: 5px; padding: 15px; margin-bottom: 15px; min-height: 110px;">
                                    <p style="font-size: 0.75rem; opacity: 0.7; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">{result['model_name']}</p>
                                    <p style="font-size: 1.15rem; font-weight: bold; margin: 5px 0; font-family: 'Lora', serif; line-height: 1.2;">{result['predicted_class_es']}</p>
                                    <p style="font-size: 0.85rem; margin: 0; font-weight: 500; color: {'#415D48' if result['confidence'] > 0.85 else '#C49A45'};">
                                        ▲ {result['confidence']:.1%} conf. | ⏱️ {result['inference_time']:.0f} ms
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)

                # Consenso de modelos
                st.subheader(f"🤝 {t('diagnosis.consensus_title')}")

                # Calcular diagnóstico más frecuente
                predictions = [r['predicted_class'] for r in st.session_state.predictions]
                consensus = max(set(predictions), key=predictions.count)
                consensus_count = predictions.count(consensus)

                # Calcular confianza promedio para el consenso
                consensus_confidence = np.mean([
                    r['confidence'] for r in st.session_state.predictions
                    if r['predicted_class'] == consensus
                ])

                # Mostrar consenso (Estilo Botánico/Laboratorio)
                disease_name = get_disease_name(consensus)
                is_disease = consensus != 2  # 2 es 'Healthy' en DISEASE_CLASSES
                disease_class = "disease" if is_disease else ""
                
                ticket_html = f"""
                <div class="lab-ticket {disease_class}">
                    <span class="lab-ticket-eyebrow">{t('diagnosis.final_diagnosis')}</span>
                    <h2 class="lab-ticket-title">{disease_name}</h2>
                    <div style="display: flex; gap: 1rem; align-items: center; margin-top: 1rem;">
                        <span class="lab-ticket-confidence">
                            <strong>{consensus_confidence:.1%}</strong> {t('diagnosis.confidence').lower()}
                        </span>
                        <span style="font-family: 'Inter', sans-serif; color: #6C7A70; font-size: 0.9rem;">
                            {t('diagnosis.agreement')}: {consensus_count}/{len(predictions)}
                        </span>
                    </div>
                </div>
                """
                st.markdown(ticket_html, unsafe_allow_html=True)

                # Gráfico de probabilidades MODERNO
                st.subheader(f"📊 {t('diagnosis.probability_distribution')}")

                # Usar plotly para gráficos más modernos
                try:
                    import plotly.graph_objects as go
                    from plotly.subplots import make_subplots

                    # Crear subplots
                    num_models = len(st.session_state.predictions)
                    cols_plotly = min(3, num_models)
                    rows_plotly = (num_models + cols_plotly - 1) // cols_plotly

                    fig = make_subplots(
                        rows=rows_plotly,
                        cols=cols_plotly,
                        subplot_titles=[r['model_name'] for r in st.session_state.predictions],
                        specs=[[{"type": "bar"}] * cols_plotly for _ in range(rows_plotly)]
                    )

                    disease_names_short = [get_disease_name(cls) for cls in DISEASE_CLASSES]

                    for i, result in enumerate(st.session_state.predictions):
                        row = (i // cols_plotly) + 1
                        col = (i % cols_plotly) + 1

                        # Colores botánicos: Black Rot (Rojo), Esca (Marrón), Sano (Verde), Blight (Mostaza)
                        colors = ['#8C4545', '#A67C52', '#415D48', '#C49A45']
                        
                        probs = result['all_predictions']

                        fig.add_trace(
                            go.Bar(
                                y=disease_names_short,
                                x=probs,
                                orientation='h',
                                marker=dict(
                                    color=colors,
                                    line=dict(color='white', width=2)
                                ),
                                text=[f'{p:.1%}' for p in probs],
                                textposition='auto',
                                showlegend=False
                            ),
                            row=row, col=col
                        )

                    # Actualizar layout
                    fig.update_layout(
                        height=300 * rows_plotly,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Arial, sans-serif", size=12),
                        title=dict(
                            text="📊 Distribución de Probabilidades por Modelo",
                            x=0.5,
                            font=dict(size=16, color='#2c3e50')
                        )
                    )

                    # Actualizar ejes
                    fig.update_xaxes(
                        range=[0, 1],
                        title_text="Probabilidad",
                        gridcolor='lightgray',
                        gridwidth=1
                    )
                    fig.update_yaxes(
                        title_text="Enfermedades",
                        gridcolor='lightgray',
                        gridwidth=1
                    )

                    st.plotly_chart(fig, use_container_width=True)

                except ImportError:
                    # Fallback a matplotlib con mejor diseño
                    fig, axes = plt.subplots(1, len(st.session_state.predictions), figsize=(18, 6))
                    if len(st.session_state.predictions) == 1:
                        axes = [axes]

                    # Configurar estilo
                    plt.style.use('seaborn-v0_8-whitegrid')

                    for i, (ax, result) in enumerate(zip(axes, st.session_state.predictions)):
                        probs = result['all_predictions']
                        disease_names_translated = [get_disease_name(cls) for cls in DISEASE_CLASSES]

                        # Colores botánicos: Black Rot (Rojo), Esca (Marrón), Sano (Verde), Blight (Mostaza)
                        colors = ['#8C4545', '#A67C52', '#415D48', '#C49A45']
                        
                        if "Hybrid" in result['model_name']:
                            title = f"🌟 {result['model_name']}"
                        else:
                            title = f"🤖 {result['model_name']}"

                        # Crear barras con gradiente
                        bars = ax.barh(disease_names_translated, probs, color=colors,
                                       edgecolor='white', linewidth=2, alpha=0.8)

                        # Añadir sombra
                        for bar in bars:
                            bar.set_zorder(2)

                        ax.set_xlim(0, 1)
                        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
                        ax.set_xlabel('Probabilidad', fontweight='bold')
                        ax.grid(True, alpha=0.3, axis='x')
                        ax.set_facecolor('#f8f9fa')

                        # Añadir valores elegantes
                        for j, (clase, prob) in enumerate(zip(disease_names_translated, probs)):
                            if prob > 0.01:
                                ax.text(prob + 0.02, j, f'{prob:.1%}',
                                        va='center', fontsize=10, fontweight='bold',
                                        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

                    plt.tight_layout()
                    st.pyplot(fig)

                # Recomendaciones
                st.subheader(f"💡 {t('diagnosis.treatment_recommendations')}")
                recommendations = get_treatment_recommendations(consensus, st.session_state.language)

                if recommendations:
                    # Título y gravedad
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {recommendations['titulo']}")
                    with col2:
                        if recommendations['gravedad'] in ["Alta", "High", "高", "Alto"]:
                            st.error(f"{t('diagnosis.severity')} {recommendations['gravedad']}")
                        elif recommendations['gravedad'] in ["Muy Alta", "Very High", "很高", "Muito Alta"]:
                            st.error(f"{t('diagnosis.severity')} {recommendations['gravedad']}")
                        elif recommendations['gravedad'] in ["Moderada", "Moderate", "中等", "Moderada"]:
                            st.warning(f"{t('diagnosis.severity')} {recommendations['gravedad']}")
                        else:
                            st.success(f"{t('diagnosis.severity')} {recommendations['gravedad']}")

                    # Tratamiento
                    with st.expander(f"🏥 {t('diagnosis.recommended_treatment')}", expanded=True):
                        for item in recommendations['tratamiento']:
                            st.write(f"• {item}")

                    # Prevención
                    with st.expander(f"🛡️ {t('diagnosis.preventive_measures')}"):
                        for item in recommendations['prevencion']:
                            st.write(f"• {item}")

                # Botón para generar reporte
                st.subheader(f"📄 {t('diagnosis.generate_report')}")
                if st.button(f"📥 {t('diagnosis.download_pdf')}"):
                    with st.spinner(t('diagnosis.generating_report')):
                        pdf_bytes = generate_diagnosis_pdf(
                            image,
                            st.session_state.predictions,
                            recommendations,
                            current_language=st.session_state.language
                        )

                        st.download_button(
                            label=f"💾 {t('diagnosis.download_pdf_button')}",
                            data=pdf_bytes,
                            file_name=f"diagnostico_vineguard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )

    else:  # Usar cámara
        st.info(f"📸 {t('diagnosis.camera_info')}")
        st.warning(t('diagnosis.camera_warning'))
