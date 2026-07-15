"""
Pestaña de Información — VineGuard AI.
Muestra información sobre enfermedades, buenas prácticas,
pruebas estadísticas y calendario fitosanitario.
"""

import pandas as pd
import streamlit as st

from src.locales.i18n import t


def render():
    """Renderiza la pestaña de Información."""
    st.header(f"📚 {t('info.title')}")

    # Información detallada de cada enfermedad
    disease_info_keys = ['black_rot', 'esca', 'leaf_blight']
    disease_icons = ['🔴', '🟤', '🟡']

    for disease_key, icon in zip(disease_info_keys, disease_icons):
        disease_info = t(f'info.diseases_info.{disease_key}')
        with st.expander(f"{icon} {disease_info['name']}"):
            st.write(f"**{t('info.description')}** {disease_info['description']}")

            st.write(f"**{t('info.symptoms')}**")
            for symptom in disease_info['symptoms']:
                st.write(f"• {symptom}")

            st.write(f"**{t('info.favorable_conditions')}** {disease_info['conditions']}")

    # Buenas prácticas
    st.subheader(f"✅ {t('info.best_practices')}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**{t('info.prevention')}**")
        for item in t('info.prevention_items'):
            st.markdown(f"- {item}")

    with col2:
        st.markdown(f"**{t('info.integrated_management')}**")
        for item in t('info.integrated_items'):
            st.markdown(f"- {item}")

    # Información sobre pruebas estadísticas
    st.subheader(f"📊 {t('info.statistical_tests')}")

    with st.expander(f"🧮 {t('info.mcc_technical')}"):
        st.markdown(f"""
        **{t('info.mcc_formula_title')}**
        
        {t('info.mcc_formula')}
        
        Donde:
        """)
        for variable in t('info.mcc_variables'):
            st.markdown(f"- {variable}")

        st.markdown(f"**{t('info.mcc_advantages_title')}**")
        for advantage in t('info.mcc_advantages'):
            st.markdown(f"- {advantage}")

    with st.expander(f"🔬 {t('info.mcnemar_technical')}"):
        st.markdown(f"""
        **{t('info.mcnemar_procedure')}**
        
        1. **{t('info.mcnemar_hypothesis')}**
           - {t('info.mcnemar_h0')}
           - {t('info.mcnemar_h1')}
        
        2. **{t('info.mcnemar_statistic')}**
           {t('info.mcnemar_statistic_formula')}
           
           {t('info.mcnemar_variables')}
        
        3. **{t('info.mcnemar_decision')}**
           - {t('info.mcnemar_reject')}
           - {t('info.mcnemar_not_reject')}
        
        **{t('info.mcnemar_application')}**
        """)
        for application in t('info.mcnemar_applications'):
            st.markdown(f"- {application}")

    # Calendario de aplicaciones
    st.subheader(f"📅 {t('info.protection_calendar')}")

    calendar_data = t('info.calendar_data')
    calendar_df = pd.DataFrame({
        t('info.phenological_stage'): calendar_data['stages'],
        t('info.main_risk'): calendar_data['risks'],
        t('info.recommended_action'): calendar_data['actions']
    })
    st.table(calendar_df)
