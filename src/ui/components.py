"""
Módulo de componentes de UI reutilizables para VineGuard AI.
Contiene la barra lateral y widgets genéricos de Streamlit.
"""

import streamlit as st

from src.locales.i18n import t
from src.core.model_manager import load_single_model
from src.utils.config import MODEL_PATHS


def render_sidebar():
    """Renderiza la barra lateral completa con selector de idioma y carga de modelos."""
    with st.sidebar:
        # ======= SELECTOR DE IDIOMA =======
        st.markdown("""
        <div class="language-selector">
        <h4 style="color: white; text-align: center; margin: 0;">🌐 Language / Idioma</h4>
        </div>
        """, unsafe_allow_html=True)

        language_options = {
            'es': '🇪🇸 Español',
            'en': '🇺🇸 English',
            'pt': '🇧🇷 Português',
            'zh': '🇨🇳 中文'
        }

        selected_language = st.selectbox(
            label="Seleccionar idioma",
            label_visibility="collapsed",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(st.session_state.language),
            key="language_selector"
        )

        # Actualizar idioma si cambió
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()

        st.markdown("---")

        st.header(f"⚙️ {t('sidebar.config')}")

        # Cargar modelos si no están cargados
        if not st.session_state.models_loaded:
            if st.button(f"🚀 {t('sidebar.load_models')}", type="primary"):
                model_names = list(MODEL_PATHS.keys())
                total = len(model_names)
                loaded = {}
                errors = []

                st.markdown("**Cargando modelos...**")
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
                    st.session_state.models       = loaded
                    st.session_state.models_loaded = True
                    st.success(f"✅ {len(loaded)}/{total} modelos cargados")
                    if errors:
                        st.warning(f"⚠️ No se cargaron: {', '.join(errors)}")
                else:
                    st.error("❌ No se pudo cargar ningún modelo")

        else:
            st.success(f"✅ {t('sidebar.models_loaded')}")

            # Mostrar modelos disponibles
            st.subheader(f"📊 {t('sidebar.available_models')}")

            # Modelos estándar
            st.write("**Modelos Estándar:**")
            for model_name in st.session_state.models.keys():
                if "Hybrid" not in model_name:
                    st.write(f"• {model_name}")

            # Modelos híbridos con estilo especial
            hybrid_models = [name for name in st.session_state.models.keys() if "Hybrid" in name]
            if hybrid_models:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; color: white; margin: 10px 0; text-align: center;">
                <h4 style="color: white !important;">🧠 MODELOS HÍBRIDOS NUEVOS</h4>
                <p>Con CLAHE + Atención Espacial</p>
                <p>Con CLAHE + Procesamiento multi-escala</p>
                </div>
                """, unsafe_allow_html=True)

                for model_name in hybrid_models:
                    st.write(f"🌟 **{model_name}** (Híbrido)")

        # Información
        st.markdown("---")
        st.subheader(f"ℹ️ {t('sidebar.info_title')}")
        st.info(t('sidebar.info_text'))
