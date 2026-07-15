"""
Módulo de configuración global de VineGuard AI.
Centraliza rutas, constantes y configuración inicial de la página Streamlit.
"""

import streamlit as st

# ======= RUTAS DE MODELOS =======
MODEL_PATHS = {
    "CNN Simple":      "models/cnn_simple.h5",         # .h5 — compatible con patch
    "MobileNetV2":     "models/mobilenetv2.keras",      # .keras — re-exportado desde Colab
    "EfficientNet":    "models/efficientnetb0.keras",   # .keras — re-exportado desde Colab
    "DenseNet":        "models/densenet121.keras",      # .keras — re-exportado desde Colab
    # ===== MODELOS HÍBRIDOS =====
    "Hybrid MobileNet": "models/Hybrid_MobileNet_Final.h5",
    "Hybrid DenseNet":  "models/Hybrid_DenseNet_Final.h5"
}

# ======= CLASES DE ENFERMEDADES =======
DISEASE_CLASSES = ["Black_rot", "Esca", "Healthy", "Leaf_blight"]

# ======= CSS PERSONALIZADO =======
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600&display=swap');

    /* Global */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px; /* Ampliado para aprovechar mejor las pantallas grandes */
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Lora', serif !important;
    }
    
    p, span, div {
        font-family: 'Inter', sans-serif;
    }

    /* === SIGNATURE ELEMENT: The Lab Ticket === */
    .lab-ticket {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-top: 4px solid #415D48; /* default healthy green */
        padding: 2rem;
        border-radius: 4px;
        margin: 2rem 0;
    }
    
    .lab-ticket.disease {
        border-top-color: #8C4545; /* Rust red for disease */
    }
    
    .lab-ticket-eyebrow {
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        color: var(--text-color);
        opacity: 0.7;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .lab-ticket-title {
        font-family: 'Lora', serif;
        font-size: 2.25rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        line-height: 1.2;
    }
    
    .lab-ticket-confidence {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        color: white;
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background-color: #415D48;
        border-radius: 20px;
    }
    .lab-ticket.disease .lab-ticket-confidence {
        background-color: #8C4545;
    }

    /* === DATA BOXES (Theory, Information, Warnings) === */
    .tech-box {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .tech-box h4 {
        margin-top: 0;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.8;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .tech-box p {
        line-height: 1.6;
        font-size: 0.95rem;
        margin-bottom: 0;
    }
    
    /* Clean up Streamlit defaults */
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 1rem;
        border-radius: 4px;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.75rem;
        opacity: 0.7;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Lora', serif !important;
    }

    /* Buttons */
    .stButton button {
        border-radius: 4px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: opacity 0.2s ease;
    }
    
    /* Image container */
    [data-testid="stImage"] {
        border-radius: 4px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        overflow: hidden;
    }

    /* Hide elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""


def setup_page():
    """Configura la página principal de Streamlit y aplica el CSS personalizado."""
    st.set_page_config(
        page_title="VineGuard AI",
        page_icon="🍇",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_session_state():
    """Inicializa las variables del estado de sesión de Streamlit si no existen."""
    if 'language' not in st.session_state:
        st.session_state.language = 'es'

    if 'models_loaded' not in st.session_state:
        st.session_state.models_loaded = False
        st.session_state.models = {}
        st.session_state.current_image = None
        st.session_state.predictions = None
        st.session_state.statistical_analysis = None
        st.session_state.mcnemar_validation = None
        st.session_state.mcnemar_analysis = None
        
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
