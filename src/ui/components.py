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
        st.subheader(f"ℹ️ {t('sidebar.info_title')}")
        st.info(t('sidebar.info_text'))
