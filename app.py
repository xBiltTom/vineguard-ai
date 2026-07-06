"""
VineGuard AI — Punto de entrada principal de la aplicación.

Este archivo es el orquestador minimal que:
1. Configura la página y el estado de sesión.
2. Renderiza la barra lateral.
3. Muestra las pestañas principales.

Toda la lógica de negocio está desacoplada en módulos bajo src/.
"""

import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import streamlit as st

# Configuración de página y CSS (debe ser la primera llamada a Streamlit)
from src.utils.config import setup_page, init_session_state

setup_page()
init_session_state()

# Módulos de UI
from src.ui.components import render_sidebar
from src.locales.i18n import t

# Tabs
from src.ui.tabs import tab_diagnosis, tab_statistics, tab_mcnemar, tab_info


def main():
    """Función principal: renderiza la aplicación completa."""
    # Encabezado principal
    st.title(f"🍇 {t('app_title')}")
    st.markdown(f"**{t('app_subtitle')}**")
    st.markdown(f"*{t('app_description')}*")

    # Sidebar
    render_sidebar()

    # Contenido principal: guardia si no hay modelos cargados
    if not st.session_state.models_loaded:
        st.warning(f"👈 {t('sidebar.load_models_warning')}")
        return

    # Pestañas principales
    tab1, tab2, tab3, tab4 = st.tabs([
        f"🔍 {t('tabs.diagnosis')}",
        f"📊 {t('tabs.statistical')}",
        f"🔬 {t('tabs.mcnemar')}",
        f"📚 {t('tabs.info')}"
    ])

    with tab1:
        tab_diagnosis.render()

    with tab2:
        tab_statistics.render()

    with tab3:
        tab_mcnemar.render()

    with tab4:
        tab_info.render()


if __name__ == "__main__":
    main()