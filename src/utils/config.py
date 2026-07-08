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
    /* Diseño responsive */
    .main .block-container {
        padding: 1rem;
        max-width: 800px;
    }
    
    /* Botones grandes para móviles */
    .stButton button {
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
        background-color: #6a0dad;
        color: white;
        border-radius: 10px;
    }
    
    /* Mejoras visuales */
    .stAlert {
        padding: 1rem;
        border-radius: 10px;
    }
    
    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Estilo para métricas */
    [data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #e0e2e6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    
    /* Estilo para estadísticas */
    .statistical-box {
        background-color: #e8f4f8;
        border: 2px solid #2e86ab;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Estilo para cajas de teoría */
    .theory-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .theory-box h4 {
        color: white !important;
        margin-bottom: 10px;
    }
    
    .theory-box p {
        color: #f0f0f0 !important;
        line-height: 1.6;
    }
    
    /* Estilo para carpetas de enfermedades */
    .disease-folder {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #ff6b6b;
    }
    
    .disease-folder.black-rot {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
        border-color: #dc3545;
    }
    
    .disease-folder.esca {
        background: linear-gradient(135deg, #8B4513 0%, #CD853F 100%);
        border-color: #8B4513;
    }
    
    .disease-folder.healthy {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        border-color: #28a745;
    }
    
    .disease-folder.leaf-blight {
        background: linear-gradient(135deg, #ffc107 0%, #ffeb3b 100%);
        border-color: #ffc107;
    }
    
    /* Resultados destacados */
    .result-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 15px 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .interpretation-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .interpretation-box h3 {
        color: white !important;
        margin-bottom: 15px;
    }
    
    .interpretation-box p {
        color: #f0f0f0 !important;
        font-size: 1.1em;
        line-height: 1.7;
    }
    
    /* Nuevos estilos para gráficos mejorados */
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Estilo para selector de idioma */
    .language-selector {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
</style>
"""


def setup_page():
    """Configura la página principal de Streamlit y aplica el CSS personalizado."""
    st.set_page_config(
        page_title="VineGuard AI",
        page_icon="🍇",
        layout="centered",
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
